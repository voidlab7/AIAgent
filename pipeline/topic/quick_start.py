"""
趣味测试快速启动脚本
聊天框关键词触发，自动爬取小红书数据并生成爆款选题报告
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from common.config import REPORTS_DIR


def run_with_mcp_data(notes_data: List[Dict], 
                      output_path: Optional[Path] = None) -> Dict:
    """
    使用MCP获取的数据运行分析
    
    Args:
        notes_data: MCP返回的笔记数据列表
        output_path: 输出报告路径（可选）
        
    Returns:
        分析结果
    """
    from fun_test_analyzer import FunTestAnalyzer
    
    print("="*60)
    print("🚀 趣味测试爆款选题分析")
    print("="*60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"数据量: {len(notes_data)} 条笔记")
    print("="*60)
    
    # 初始化分析器
    analyzer = FunTestAnalyzer()
    
    # 加载数据
    print("\n📥 加载数据...")
    analyzer.load_notes_from_data(notes_data)
    print(f"✓ 成功加载 {len(analyzer.notes)} 条有效笔记")
    
    # 执行分析
    print("\n📊 分析热点数据...")
    result = analyzer.analyze()
    
    summary = result.get("summary", {})
    print(f"✓ 总点赞: {summary.get('total_likes', 0):,}")
    print(f"✓ 总收藏: {summary.get('total_collects', 0):,}")
    print(f"✓ 总评论: {summary.get('total_comments', 0):,}")
    
    # 生成报告
    print("\n📝 生成爆款选题报告...")
    report_path = analyzer.generate_report(output_path)
    print(f"✓ 报告已生成: {report_path}")
    
    # 显示TOP 5
    print("\n🔥 热门 TOP 5:")
    print("-"*60)
    for i, note in enumerate(result.get("top_10", [])[:5], 1):
        title = note.get('title', '')[:30]
        print(f"{i}. {title}")
        print(f"   👍 {note.get('likes', 0):,} | ⭐ {note.get('collects', 0):,} | 💬 {note.get('comments', 0):,}")
    
    # 显示选题建议
    print("\n💡 爆款选题建议:")
    print("-"*60)
    suggestions = analyzer.generate_topic_suggestions()
    for i, suggestion in enumerate(suggestions[:3], 1):
        print(f"\n{i}. {suggestion['category']}")
        print(f"   理由: {suggestion['reason']}")
        print(f"   预估: {suggestion['estimated_engagement']}")
    
    print("\n" + "="*60)
    print("✅ 分析完成！")
    print(f"📄 查看完整报告: {report_path}")
    print("="*60)
    
    return {
        "success": True,
        "report_path": str(report_path),
        "summary": summary,
        "top_10": result.get("top_10", []),
        "suggestions": suggestions,
    }


def demo_with_sample_data():
    """使用示例数据演示"""
    # 示例数据（基于之前的热点数据）
    sample_data = [
        {
            "note_id": "69aaa91f0000000022023457",
            "title": "别笑，你也过不了第二关‼️",
            "author": "呼噜馆儿",
            "likes": 19183,
            "collects": 1376,
            "comments": 357,
            "shares": 916,
            "url": "https://www.xiaohongshu.com/explore/69aaa91f0000000022023457",
            "type": "视频"
        },
        {
            "note_id": "69abf4fd0000000028008dd3",
            "title": "情侣小测试！蒙眼猜身高亲亲",
            "author": "冰镇成汁de日常",
            "likes": 10642,
            "collects": 927,
            "comments": 228,
            "shares": 137,
            "url": "https://www.xiaohongshu.com/explore/69abf4fd0000000028008dd3",
            "type": "视频"
        },
        {
            "note_id": "69b14e37000000002602dfff",
            "title": "内向程度测试题",
            "author": "测试达人",
            "likes": 4030,
            "collects": 141,
            "comments": 276,
            "shares": 478,
            "url": "https://www.xiaohongshu.com/explore/69b14e37000000002602dfff",
            "type": "图文"
        },
        {
            "note_id": "test4",
            "title": "神秘小实验",
            "author": "科学小达人",
            "likes": 3960,
            "collects": 1495,
            "comments": 31,
            "shares": 202,
            "url": "https://www.xiaohongshu.com/explore/test4",
            "type": "视频"
        },
        {
            "note_id": "test5",
            "title": "反应力测试",
            "author": "游戏博主",
            "likes": 1913,
            "collects": 145,
            "comments": 1304,
            "shares": 26,
            "url": "https://www.xiaohongshu.com/explore/test5",
            "type": "视频"
        },
        {
            "note_id": "test6",
            "title": "一个问题测试朋友性格",
            "author": "心理测试君",
            "likes": 1678,
            "collects": 249,
            "comments": 84,
            "shares": 729,
            "url": "https://www.xiaohongshu.com/explore/test6",
            "type": "图文"
        },
        {
            "note_id": "test7",
            "title": "心理测试｜你未来的事业会怎么样？",
            "author": "职场占卜",
            "likes": 1103,
            "collects": 204,
            "comments": 405,
            "shares": 79,
            "url": "https://www.xiaohongshu.com/explore/test7",
            "type": "图文"
        },
        {
            "note_id": "test8",
            "title": "（答案版）测测老天最想骂你什么",
            "author": "趣味测试屋",
            "likes": 1012,
            "collects": 189,
            "comments": 55,
            "shares": 17,
            "url": "https://www.xiaohongshu.com/explore/test8",
            "type": "图文"
        },
        {
            "note_id": "test9",
            "title": "你的情感冷漠症是第几级",
            "author": "心理分析师",
            "likes": 1816,
            "collects": 381,
            "comments": 19201,
            "shares": 143,
            "url": "https://www.xiaohongshu.com/explore/test9",
            "type": "图文"
        },
        {
            "note_id": "test10",
            "title": "MBTI不同类型会怎么选",
            "author": "MBTI研究所",
            "likes": 959,
            "collects": 492,
            "comments": 9808,
            "shares": 492,
            "url": "https://www.xiaohongshu.com/explore/test10",
            "type": "图文"
        },
    ]
    
    return run_with_mcp_data(sample_data)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="趣味测试爆款选题分析")
    parser.add_argument("--demo", action="store_true", help="使用示例数据演示")
    parser.add_argument("--data", type=str, help="JSON数据文件路径")
    
    args = parser.parse_args()
    
    if args.demo:
        demo_with_sample_data()
    elif args.data:
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
        run_with_mcp_data(data)
    else:
        print("使用方式:")
        print("  python quick_start.py --demo        # 使用示例数据演示")
        print("  python quick_start.py --data xxx.json  # 使用指定JSON数据")
        print("\n或者在代码中调用:")
        print("  from quick_start import run_with_mcp_data")
        print("  result = run_with_mcp_data(mcp_notes_data)")
