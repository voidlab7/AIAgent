"""
趣味测试热点分析器
支持小红书MCP数据爬取、热度分析、爆款选题报告生成
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
import re

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from common.config import REPORTS_DIR
from common.database import db


@dataclass
class NoteData:
    """小红书笔记数据结构"""
    note_id: str
    title: str
    author: str
    likes: int = 0
    collects: int = 0
    comments: int = 0
    shares: int = 0
    url: str = ""
    cover_image: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    publish_time: str = ""
    note_type: str = "图文"  # 图文 or 视频
    
    @property
    def total_engagement(self) -> int:
        """总互动数"""
        return self.likes + self.collects + self.comments + self.shares
    
    @property
    def hot_score(self) -> float:
        """热度分数（加权计算）"""
        # 权重：点赞1.0, 收藏1.5, 评论2.0, 分享3.0
        return (
            self.likes * 1.0 +
            self.collects * 1.5 +
            self.comments * 2.0 +
            self.shares * 3.0
        )
    
    @property
    def collect_rate(self) -> float:
        """收藏率（收藏/点赞）"""
        return self.collects / self.likes * 100 if self.likes > 0 else 0
    
    @property
    def comment_rate(self) -> float:
        """评论率（评论/点赞）"""
        return self.comments / self.likes * 100 if self.likes > 0 else 0
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        data = asdict(self)
        data['total_engagement'] = self.total_engagement
        data['hot_score'] = self.hot_score
        data['collect_rate'] = round(self.collect_rate, 1)
        data['comment_rate'] = round(self.comment_rate, 1)
        return data


class FunTestAnalyzer:
    """趣味测试热点分析器"""
    
    # 搜索关键词配置
    SEARCH_KEYWORDS = [
        "趣味测试",
        "心理测试",
        "性格测试",
        "MBTI测试",
        "情感测试",
    ]
    
    # 测试类型分类规则
    TEST_TYPE_RULES = {
        "性格分析类": ["性格", "内向", "外向", "MBTI", "人格", "脾气", "情绪"],
        "情感预测类": ["情感", "恋爱", "爱情", "吸引", "缘分", "另一半", "异性"],
        "未来预测类": ["未来", "事业", "命运", "城市", "运势", "发展", "生活"],
        "互动挑战类": ["挑战", "测试", "关卡", "反应", "游戏", "通关", "第几关"],
        "MBTI相关": ["MBTI", "mbti", "E人", "I人", "INFP", "ENFP", "INTJ"],
        "趣味娱乐类": ["有趣", "好玩", "笑", "神秘", "实验"],
    }
    
    def __init__(self, mcp_client=None):
        """
        初始化分析器
        
        Args:
            mcp_client: MCP客户端（可选，用于外部注入）
        """
        self.mcp_client = mcp_client
        self.notes: List[NoteData] = []
        self.analysis_result: Dict = {}
        self.report_path: Optional[Path] = None
        
    def fetch_notes_from_mcp(self, keyword: str, limit: int = 20) -> List[Dict]:
        """
        从MCP获取笔记数据（抽象方法，由外部实现）
        
        Args:
            keyword: 搜索关键词
            limit: 最大数量
            
        Returns:
            笔记数据列表
        """
        # 这个方法会被外部MCP调用覆盖
        # 返回空列表表示需要外部提供数据
        return []
    
    def load_notes_from_data(self, raw_notes: List[Dict]) -> None:
        """
        从原始数据加载笔记
        
        Args:
            raw_notes: MCP返回的原始笔记数据
        """
        for raw in raw_notes:
            # 解析MCP返回的数据格式
            note = NoteData(
                note_id=raw.get('note_id', raw.get('id', '')),
                title=raw.get('title', raw.get('display_title', '')),
                author=raw.get('author', raw.get('user', {}).get('nickname', '')),
                likes=self._parse_int(raw.get('likes', raw.get('liked_count', 0))),
                collects=self._parse_int(raw.get('collects', raw.get('collected_count', 0))),
                comments=self._parse_int(raw.get('comments', raw.get('comment_count', 0))),
                shares=self._parse_int(raw.get('shares', raw.get('share_count', 0))),
                url=raw.get('url', f"https://www.xiaohongshu.com/explore/{raw.get('note_id', raw.get('id', ''))}"),
                cover_image=raw.get('cover_image', raw.get('cover', {}).get('url', '')),
                content=raw.get('content', raw.get('desc', '')),
                tags=raw.get('tags', []),
                publish_time=raw.get('publish_time', raw.get('time', '')),
                note_type=raw.get('type', '图文')
            )
            
            # 去重
            if not any(n.note_id == note.note_id for n in self.notes):
                self.notes.append(note)
    
    def _parse_int(self, value) -> int:
        """解析整数，处理字符串格式如 '1.2万'"""
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            value = value.strip()
            if '万' in value:
                return int(float(value.replace('万', '')) * 10000)
            if '千' in value:
                return int(float(value.replace('千', '')) * 1000)
            try:
                return int(value.replace(',', ''))
            except:
                return 0
        return 0
    
    def classify_note_type(self, note: NoteData) -> str:
        """
        分类笔记类型
        
        Args:
            note: 笔记数据
            
        Returns:
            测试类型
        """
        title = note.title.lower()
        content = note.content.lower() if note.content else ""
        text = title + " " + content
        
        for test_type, keywords in self.TEST_TYPE_RULES.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    return test_type
        
        return "其他趣味类"
    
    def analyze(self) -> Dict:
        """
        分析热点数据
        
        Returns:
            分析结果
        """
        if not self.notes:
            return {"error": "没有可分析的数据"}
        
        # 按热度排序
        sorted_notes = sorted(self.notes, key=lambda x: x.hot_score, reverse=True)
        
        # 分类统计
        type_stats = {}
        for note in sorted_notes:
            note_type = self.classify_note_type(note)
            if note_type not in type_stats:
                type_stats[note_type] = {
                    "count": 0,
                    "total_likes": 0,
                    "total_collects": 0,
                    "total_comments": 0,
                    "notes": []
                }
            type_stats[note_type]["count"] += 1
            type_stats[note_type]["total_likes"] += note.likes
            type_stats[note_type]["total_collects"] += note.collects
            type_stats[note_type]["total_comments"] += note.comments
            type_stats[note_type]["notes"].append(note.to_dict())
        
        # 计算各类型平均值
        for t in type_stats:
            count = type_stats[t]["count"]
            if count > 0:
                type_stats[t]["avg_likes"] = round(type_stats[t]["total_likes"] / count)
                type_stats[t]["avg_collects"] = round(type_stats[t]["total_collects"] / count)
                type_stats[t]["avg_comments"] = round(type_stats[t]["total_comments"] / count)
        
        # 整体统计
        total_notes = len(self.notes)
        total_likes = sum(n.likes for n in self.notes)
        total_collects = sum(n.collects for n in self.notes)
        total_comments = sum(n.comments for n in self.notes)
        
        # 找出高互动笔记（评论率>100%）
        high_engagement_notes = [
            n.to_dict() for n in sorted_notes 
            if n.comment_rate > 100
        ]
        
        # 找出高收藏笔记（收藏率>30%）
        high_collect_notes = [
            n.to_dict() for n in sorted_notes 
            if n.collect_rate > 30
        ]
        
        self.analysis_result = {
            "summary": {
                "total_notes": total_notes,
                "total_likes": total_likes,
                "total_collects": total_collects,
                "total_comments": total_comments,
                "avg_likes": round(total_likes / total_notes) if total_notes > 0 else 0,
                "avg_collects": round(total_collects / total_notes) if total_notes > 0 else 0,
                "avg_comments": round(total_comments / total_notes) if total_notes > 0 else 0,
                "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            "top_10": [n.to_dict() for n in sorted_notes[:10]],
            "type_analysis": type_stats,
            "high_engagement_notes": high_engagement_notes[:10],
            "high_collect_notes": high_collect_notes[:10],
            "all_notes": [n.to_dict() for n in sorted_notes],
        }
        
        return self.analysis_result
    
    def generate_topic_suggestions(self) -> List[Dict]:
        """
        生成爆款选题建议
        
        Returns:
            选题建议列表
        """
        if not self.analysis_result:
            self.analyze()
        
        suggestions = []
        
        # 基于热门类型生成建议
        type_stats = self.analysis_result.get("type_analysis", {})
        
        # 按平均点赞排序类型
        sorted_types = sorted(
            type_stats.items(),
            key=lambda x: x[1].get("avg_likes", 0),
            reverse=True
        )
        
        for i, (test_type, stats) in enumerate(sorted_types[:5], 1):
            top_note = stats["notes"][0] if stats["notes"] else None
            
            suggestion = {
                "priority": i,
                "category": test_type,
                "reason": f"该类型平均点赞{stats.get('avg_likes', 0)}，共{stats['count']}条热门笔记",
                "reference_title": top_note["title"] if top_note else "",
                "reference_url": top_note["url"] if top_note else "",
                "suggested_titles": self._generate_title_suggestions(test_type, top_note),
                "content_tips": self._get_content_tips(test_type),
                "estimated_engagement": self._estimate_engagement(stats),
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_title_suggestions(self, test_type: str, reference_note: Optional[Dict]) -> List[str]:
        """生成标题建议"""
        templates = {
            "性格分析类": [
                "测一测｜你的{X}程度是第几级？",
                "{X}测试题｜看看你是哪种类型",
                "3道题测出你的真实{X}",
            ],
            "情感预测类": [
                "测一测｜你最吸引哪类{X}？",
                "心理测试｜你的{X}会是什么样？",
                "快来测｜你的{X}藏着什么秘密",
            ],
            "未来预测类": [
                "心理测试｜你未来的{X}会怎么样？",
                "测一测｜适合你发展的{X}",
                "选一个｜测测你的{X}运势",
            ],
            "互动挑战类": [
                "别笑！你也过不了第{X}关",
                "{X}挑战｜能过3关算你赢",
                "测测你的{X}反应力",
            ],
            "MBTI相关": [
                "不同MBTI会怎么选{X}",
                "E人I人的{X}测试",
                "你的MBTI决定了你的{X}",
            ],
        }
        
        return templates.get(test_type, [
            "趣味测试｜测测你的{X}",
            "小测试｜你是哪种{X}类型",
        ])
    
    def _get_content_tips(self, test_type: str) -> List[str]:
        """获取内容创作建议"""
        tips = {
            "性格分析类": [
                "设计3-5个简短的选择题",
                "每个结果都要有正面描述",
                "评论区引导：'你是哪一种？'",
            ],
            "情感预测类": [
                "结果要有期待感和正面暗示",
                "可以加入'艾特你想测的人'",
                "设置多个有差异的结果",
            ],
            "未来预测类": [
                "结果要积极向上",
                "可以结合实际建议",
                "引导收藏'以后对照'",
            ],
            "互动挑战类": [
                "前3秒要抓眼球",
                "难度递进设计",
                "鼓励评论'你过了第几关'",
            ],
            "MBTI相关": [
                "蹭MBTI热度",
                "设计有共鸣的选项",
                "引导分享给同类型朋友",
            ],
        }
        
        return tips.get(test_type, [
            "封面要醒目",
            "测试题不宜过长",
            "结果要有分享价值",
        ])
    
    def _estimate_engagement(self, stats: Dict) -> str:
        """预估互动效果"""
        avg_likes = stats.get("avg_likes", 0)
        
        if avg_likes >= 5000:
            return "🔥🔥🔥🔥🔥 极高（预估5000+点赞）"
        elif avg_likes >= 2000:
            return "🔥🔥🔥🔥 很高（预估2000-5000点赞）"
        elif avg_likes >= 1000:
            return "🔥🔥🔥 高（预估1000-2000点赞）"
        elif avg_likes >= 500:
            return "🔥🔥 中等（预估500-1000点赞）"
        else:
            return "🔥 普通（预估500以下点赞）"
    
    def generate_report(self, output_path: Optional[Path] = None) -> Path:
        """
        生成爆款选题报告
        
        Args:
            output_path: 输出路径（可选）
            
        Returns:
            报告文件路径
        """
        if not self.analysis_result:
            self.analyze()
        
        # 生成选题建议
        suggestions = self.generate_topic_suggestions()
        
        # 确定输出路径
        if output_path is None:
            today = datetime.now().strftime("%Y%m%d")
            output_path = REPORTS_DIR / f"趣味测试爆款选题报告_{today}.md"
        
        self.report_path = output_path
        
        # 生成报告内容
        report_content = self._build_report_content(suggestions)
        
        # 写入文件
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # 保存到数据库
        self._save_to_database()
        
        return output_path
    
    def _build_report_content(self, suggestions: List[Dict]) -> str:
        """构建报告内容"""
        summary = self.analysis_result.get("summary", {})
        top_10 = self.analysis_result.get("top_10", [])
        type_analysis = self.analysis_result.get("type_analysis", {})
        
        report = f"""# 📊 小红书「趣味测试」爆款选题报告

**生成时间**: {summary.get('analysis_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}  
**数据来源**: 小红书平台实时数据  
**分析笔记数**: {summary.get('total_notes', 0)} 篇

---

## 🔥 一、热度概览

### 1.1 核心数据

| 指标 | 数值 |
|------|------|
| 总笔记数 | {summary.get('total_notes', 0)} |
| 总点赞数 | {summary.get('total_likes', 0):,} |
| 总收藏数 | {summary.get('total_collects', 0):,} |
| 总评论数 | {summary.get('total_comments', 0):,} |
| 平均点赞 | {summary.get('avg_likes', 0):,} |
| 平均收藏 | {summary.get('avg_collects', 0):,} |
| 平均评论 | {summary.get('avg_comments', 0):,} |

---

## 📈 二、热门笔记 TOP 10

| 排名 | 标题 | 点赞 | 收藏 | 评论 | 分享 | 热度分 |
|------|------|------|------|------|------|--------|
"""
        
        for i, note in enumerate(top_10, 1):
            title = note.get('title', '')[:20] + ('...' if len(note.get('title', '')) > 20 else '')
            report += f"| {i} | [{title}]({note.get('url', '')}) | {note.get('likes', 0):,} | {note.get('collects', 0):,} | {note.get('comments', 0):,} | {note.get('shares', 0):,} | {note.get('hot_score', 0):,.0f} |\n"
        
        report += """
---

## 🎯 三、内容类型分析

"""
        
        # 按平均点赞排序
        sorted_types = sorted(
            type_analysis.items(),
            key=lambda x: x[1].get("avg_likes", 0),
            reverse=True
        )
        
        for test_type, stats in sorted_types:
            report += f"""### {test_type}

- **笔记数量**: {stats['count']} 篇
- **平均点赞**: {stats.get('avg_likes', 0):,}
- **平均收藏**: {stats.get('avg_collects', 0):,}
- **平均评论**: {stats.get('avg_comments', 0):,}

**代表作品**:
"""
            for note in stats['notes'][:3]:
                report += f"- [{note.get('title', '')[:30]}]({note.get('url', '')}) (👍{note.get('likes', 0):,})\n"
            report += "\n"
        
        report += """---

## 💡 四、爆款选题建议

基于数据分析，为您推荐以下选题方向：

"""
        
        for suggestion in suggestions:
            report += f"""### ⭐ 优先级 {suggestion['priority']}: {suggestion['category']}

**推荐理由**: {suggestion['reason']}

**参考爆款**: [{suggestion.get('reference_title', '')[:30]}]({suggestion.get('reference_url', '')})

**标题模板**:
"""
            for title in suggestion.get('suggested_titles', []):
                report += f"- {title}\n"
            
            report += f"""
**创作建议**:
"""
            for tip in suggestion.get('content_tips', []):
                report += f"- {tip}\n"
            
            report += f"""
**预估效果**: {suggestion.get('estimated_engagement', '')}

---

"""
        
        report += """## 🚀 五、快速行动指南

### 5.1 立即可做

1. ✅ 选择一个热门类型（推荐：性格分析类/互动挑战类）
2. ✅ 参考爆款标题公式
3. ✅ 制作3-5道测试题
4. ✅ 设计4-6个有差异的结果
5. ✅ 在评论区引导互动

### 5.2 发布建议

| 时段 | 推荐度 | 说明 |
|------|--------|------|
| 19:00-21:00 | ⭐⭐⭐⭐⭐ | 黄金时段，用户活跃度最高 |
| 12:00-14:00 | ⭐⭐⭐⭐ | 午休时间，适合轻松内容 |
| 07:00-09:00 | ⭐⭐⭐ | 通勤时间，碎片化阅读 |

### 5.3 注意事项

- ❌ 测试题不要超过10道
- ❌ 结果描述不要太负面
- ❌ 不要完全抄袭已有内容
- ✅ 结果要有分享价值
- ✅ 积极回复评论区

---

## 📊 六、数据附录

### 完整笔记列表

<details>
<summary>点击展开查看全部笔记</summary>

| 标题 | 作者 | 点赞 | 收藏 | 评论 | 链接 |
|------|------|------|------|------|------|
"""
        
        all_notes = self.analysis_result.get("all_notes", [])
        for note in all_notes:
            title = note.get('title', '')[:25] + ('...' if len(note.get('title', '')) > 25 else '')
            author = note.get('author', '')[:10]
            report += f"| {title} | {author} | {note.get('likes', 0):,} | {note.get('collects', 0):,} | {note.get('comments', 0):,} | [查看]({note.get('url', '')}) |\n"
        
        report += """
</details>

---

**报告生成**: AI自媒体创作助手  
**数据支持**: 小红书MCP实时数据  
**更新建议**: 每周生成新报告追踪热点变化
"""
        
        return report
    
    def _save_to_database(self) -> None:
        """保存分析结果到数据库"""
        try:
            for note in self.notes:
                db.execute("""
                    INSERT OR REPLACE INTO hotspots
                    (source, keyword, rank, heat_value, url, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    'xiaohongshu',
                    '趣味测试',
                    0,
                    int(note.hot_score),
                    note.url,
                    note.title
                ))
        except Exception as e:
            print(f"⚠️ 保存到数据库失败: {e}")


# 快捷函数
def run_analysis(notes_data: List[Dict], output_report: bool = True) -> Dict:
    """
    执行趣味测试分析
    
    Args:
        notes_data: MCP返回的笔记数据
        output_report: 是否输出报告
        
    Returns:
        分析结果
    """
    analyzer = FunTestAnalyzer()
    analyzer.load_notes_from_data(notes_data)
    result = analyzer.analyze()
    
    if output_report:
        report_path = analyzer.generate_report()
        result['report_path'] = str(report_path)
        print(f"✅ 报告已生成: {report_path}")
    
    return result


if __name__ == "__main__":
    # 测试用模拟数据
    mock_notes = [
        {
            "note_id": "test1",
            "title": "别笑，你也过不了第二关‼️",
            "author": "呼噜馆儿",
            "likes": 19183,
            "collects": 1376,
            "comments": 357,
            "shares": 916,
            "url": "https://www.xiaohongshu.com/explore/test1",
            "type": "视频"
        },
        {
            "note_id": "test2", 
            "title": "情侣小测试！蒙眼猜身高",
            "author": "冰镇成汁",
            "likes": 10642,
            "collects": 927,
            "comments": 228,
            "shares": 137,
            "url": "https://www.xiaohongshu.com/explore/test2",
            "type": "视频"
        },
        {
            "note_id": "test3",
            "title": "内向程度测试题",
            "author": "测试达人",
            "likes": 4030,
            "collects": 141,
            "comments": 276,
            "shares": 478,
            "url": "https://www.xiaohongshu.com/explore/test3",
            "type": "图文"
        },
    ]
    
    result = run_analysis(mock_notes)
    print(f"\n分析完成，共 {result.get('summary', {}).get('total_notes', 0)} 条笔记")
