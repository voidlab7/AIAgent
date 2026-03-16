"""
小红书热门文章抓取器
支持关键词搜索、话题热门、热度计算
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class XiaohongshuHotFetcher:
    """小红书热门抓取器"""
    
    # MCP 方式配置
    MCP_METHOD = "rednote"  # "rednote" 或 "xiaohongshu-mcp"
    
    # 热门阈值配置
    HOT_THRESHOLDS = {
        'default': 500,
        'AI': 300,              # AI 类目
        'tech': 400,            # 科技类
        'lifestyle': 800,       # 生活类
    }
    
    # 热度权重
    WEIGHT_LIKES = 1.0
    WEIGHT_COLLECTS = 1.5      # 收藏权重高（种草平台）
    WEIGHT_COMMENTS = 2.0
    WEIGHT_SHARES = 3.0        # 分享权重最高
    
    def __init__(self, use_mcp: str = "rednote"):
        """
        初始化抓取器
        
        Args:
            use_mcp: 使用的 MCP 类型
                - "rednote": RedNote MCP (npm 安装)
                - "xiaohongshu-mcp": xiaohongshu-mcp (Docker 部署)
        """
        self.use_mcp = use_mcp
        self.mcp_available = self._check_mcp_available()
    
    def _check_mcp_available(self) -> bool:
        """检查 MCP 是否可用"""
        if self.use_mcp == "rednote":
            # 检查 rednote-mcp 是否已安装
            result = subprocess.run(
                ["which", "rednote-mcp"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        else:
            # 检查 xiaohongshu-mcp 是否运行
            # TODO: 检查 Docker 容器状态
            return False
    
    def fetch_by_keyword(self, 
                        keyword: str,
                        max_count: int = 50,
                        sort_by: str = "hot") -> List[Dict]:
        """
        按关键词搜索热门文章
        
        Args:
            keyword: 搜索关键词
            max_count: 最大抓取数量
            sort_by: 排序方式 "hot"(热门) 或 "latest"(最新)
        
        Returns:
            热门文章列表
        """
        print(f"\n{'='*60}")
        print(f"搜索关键词: {keyword}")
        print(f"排序方式: {sort_by}")
        print('='*60)
        
        if not self.mcp_available:
            print("❌ MCP 不可用，使用模拟数据")
            return self._get_mock_data(keyword, max_count)
        
        # 使用 RedNote MCP 搜索
        notes = self._search_via_rednote_mcp(keyword, max_count, sort_by)
        
        # 计算热度分数
        notes_with_score = []
        for note in notes:
            score = self.calculate_hot_score(note)
            note['hot_score'] = score
            notes_with_score.append(note)
        
        # 按热度排序
        notes_with_score.sort(key=lambda x: x['hot_score'], reverse=True)
        
        # 筛选热门
        hot_notes = [n for n in notes_with_score 
                    if n['hot_score'] >= self.get_threshold(keyword)]
        
        print(f"✓ 获取到 {len(notes)} 条笔记")
        print(f"✓ 筛选出 {len(hot_notes)} 条热门笔记")
        
        return hot_notes
    
    def _search_via_rednote_mcp(self, 
                                keyword: str, 
                                max_count: int,
                                sort_by: str) -> List[Dict]:
        """
        使用 RedNote MCP 搜索
        
        MCP 工具列表：
        - search_notes: 搜索笔记
        - get_note_content: 获取笔记内容
        - get_note_comments: 获取笔记评论
        """
        try:
            # 调用 MCP 工具（通过 npx）
            # 注意：实际使用时需要 MCP server 运行
            
            # 模拟调用流程
            cmd = [
                "npx", "rednote-mcp",
                "search",
                "--keyword", keyword,
                "--limit", str(max_count),
                "--sort", sort_by
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # 解析返回的 JSON
                data = json.loads(result.stdout)
                return data.get('notes', [])
            else:
                print(f"MCP 搜索失败: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            print("MCP 搜索超时")
            return []
        except json.JSONDecodeError:
            print("MCP 返回数据解析失败")
            return []
        except Exception as e:
            print(f"MCP 调用异常: {e}")
            return []
    
    def fetch_by_topic(self, topic: str, max_count: int = 50) -> List[Dict]:
        """
        按话题抓取热门文章
        
        Args:
            topic: 话题名称（如 "AI"、"人工智能"）
            max_count: 最大抓取数量
        
        Returns:
            热门文章列表
        """
        # 话题通常是 # 开头
        topic_keyword = f"#{topic}" if not topic.startswith('#') else topic
        
        return self.fetch_by_keyword(topic_keyword, max_count, sort_by="hot")
    
    def fetch_multiple_keywords(self, 
                               keywords: List[str],
                               max_count_per_keyword: int = 20) -> List[Dict]:
        """
        多关键词抓取并去重
        
        Args:
            keywords: 关键词列表
            max_count_per_keyword: 每个关键词的最大抓取数
        
        Returns:
            合并去重后的热门文章列表
        """
        all_notes = []
        seen_ids = set()
        
        for keyword in keywords:
            notes = self.fetch_by_keyword(keyword, max_count_per_keyword)
            
            # 去重
            for note in notes:
                note_id = note.get('id')
                if note_id and note_id not in seen_ids:
                    seen_ids.add(note_id)
                    all_notes.append(note)
        
        # 按热度重新排序
        all_notes.sort(key=lambda x: x.get('hot_score', 0), reverse=True)
        
        print(f"\n✓ 总计获取 {len(all_notes)} 条不重复的热门笔记")
        
        return all_notes
    
    def calculate_hot_score(self, note: Dict) -> float:
        """
        计算笔记热度分数
        
        Args:
            note: 笔记数据
        
        Returns:
            热度分数
        """
        likes = note.get('likes', 0)
        collects = note.get('collects', 0)
        comments = note.get('comments', 0)
        shares = note.get('shares', 0)
        
        # 发布时间（小时）
        publish_time = note.get('publish_time')
        if publish_time:
            try:
                pub_dt = datetime.fromisoformat(publish_time)
                hours = (datetime.now() - pub_dt).total_seconds() / 3600
            except:
                hours = 24  # 默认 24 小时
        else:
            hours = 24
        
        # 热度公式
        score = (
            likes * self.WEIGHT_LIKES +
            collects * self.WEIGHT_COLLECTS +
            comments * self.WEIGHT_COMMENTS +
            shares * self.WEIGHT_SHARES
        ) / (hours + 1) ** 0.8
        
        return round(score, 2)
    
    def get_threshold(self, keyword: str) -> float:
        """
        获取热门阈值
        
        Args:
            keyword: 关键词
        
        Returns:
            热门阈值
        """
        # 匹配关键词对应的阈值
        for key, threshold in self.HOT_THRESHOLDS.items():
            if key.lower() in keyword.lower():
                return threshold
        
        return self.HOT_THRESHOLDS['default']
    
    def _get_mock_data(self, keyword: str, max_count: int) -> List[Dict]:
        """
        获取模拟数据（用于测试）
        """
        mock_notes = []
        
        for i in range(min(max_count, 10)):
            mock_notes.append({
                'id': f'mock_{keyword}_{i}',
                'title': f'{keyword}热门笔记{i+1}',
                'author': f'博主{i+1}',
                'likes': 1000 + i * 100,
                'collects': 500 + i * 50,
                'comments': 100 + i * 10,
                'shares': 50 + i * 5,
                'publish_time': (datetime.now() - timedelta(hours=i)).isoformat(),
                'url': f'https://xiaohongshu.com/note/mock_{i}',
                'images': [f'https://example.com/image_{i}.jpg'],
                'tags': [keyword, 'AI', '科技']
            })
        
        return mock_notes
    
    def save_to_database(self, notes: List[Dict], keyword: str):
        """
        保存到数据库
        
        Args:
            notes: 笔记列表
            keyword: 搜索关键词
        """
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(project_root))
        
        from common.database import Database
        
        db = Database()
        
        for note in notes:
            try:
                db.cursor.execute("""
                    INSERT OR REPLACE INTO hotspots
                    (platform, keyword, title, url, hot_score, 
                     likes, collects, comments, shares, 
                     author, publish_time, fetched_at, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    'xiaohongshu',
                    keyword,
                    note.get('title', ''),
                    note.get('url', ''),
                    note.get('hot_score', 0),
                    note.get('likes', 0),
                    note.get('collects', 0),
                    note.get('comments', 0),
                    note.get('shares', 0),
                    note.get('author', ''),
                    note.get('publish_time', ''),
                    datetime.now().isoformat(),
                    json.dumps(note, ensure_ascii=False)
                ))
            except Exception as e:
                print(f"保存失败: {e}")
        
        db.conn.commit()
        print(f"✓ 已保存 {len(notes)} 条热点到数据库")


def main():
    """主函数：演示使用"""
    fetcher = XiaohongshuHotFetcher(use_mcp="rednote")
    
    # 示例 1：搜索单个关键词
    print("\n" + "="*80)
    print("示例 1：搜索单个关键词 'AI'")
    print("="*80)
    
    ai_notes = fetcher.fetch_by_keyword("AI", max_count=20)
    
    print(f"\n前 5 条热门笔记：")
    for i, note in enumerate(ai_notes[:5], 1):
        print(f"\n{i}. {note.get('title', 'N/A')}")
        print(f"   热度: {note.get('hot_score', 0):.2f}")
        print(f"   点赞: {note.get('likes', 0)} | 收藏: {note.get('collects', 0)}")
        print(f"   评论: {note.get('comments', 0)} | 分享: {note.get('shares', 0)}")
    
    # 示例 2：多关键词搜索
    print("\n" + "="*80)
    print("示例 2：多关键词搜索")
    print("="*80)
    
    keywords = ["AI", "ChatGPT", "AIGC", "人工智能"]
    all_notes = fetcher.fetch_multiple_keywords(keywords, max_count_per_keyword=10)
    
    print(f"\n前 5 条最热门笔记：")
    for i, note in enumerate(all_notes[:5], 1):
        print(f"\n{i}. {note.get('title', 'N/A')}")
        print(f"   热度: {note.get('hot_score', 0):.2f}")
    
    # 示例 3：保存到数据库
    if ai_notes:
        print("\n" + "="*80)
        print("示例 3：保存到数据库")
        print("="*80)
        
        fetcher.save_to_database(ai_notes[:10], "AI")


if __name__ == "__main__":
    main()
