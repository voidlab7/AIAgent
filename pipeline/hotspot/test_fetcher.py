"""
测试小红书热门文章抓取
"""
import sys
from pathlib import Path
import importlib.util

# 添加项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载抓取器模块
spec = importlib.util.spec_from_file_location(
    "xiaohongshu_fetcher",
    project_root / "1_热点监控/fetchers/xiaohongshu_fetcher.py"
)
fetcher_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetcher_module)


def main():
    print("="*60)
    print("测试小红书热门文章抓取")
    print("="*60)

    # 1. 初始化
    print("\n1. 初始化抓取器...")
    fetcher = fetcher_module.XiaohongshuHotFetcher(use_mcp='rednote')
    print(f"   MCP 可用: {fetcher.mcp_available}")

    # 2. 模拟数据测试
    print("\n2. 使用模拟数据测试...")
    notes = fetcher._get_mock_data('AI', 5)

    for i, note in enumerate(notes, 1):
        score = fetcher.calculate_hot_score(note)
        note['hot_score'] = score
        print(f"\n   {i}. {note['title']}")
        print(f"      热度: {score:.2f}")
        print(f"      点赞: {note['likes']} | 收藏: {note['collects']}")
        print(f"      评论: {note['comments']} | 分享: {note['shares']}")

    # 3. 热门阈值
    print(f"\n3. 热门阈值配置...")
    print(f"   AI 类目: {fetcher.get_threshold('AI')}")
    print(f"   默认: {fetcher.get_threshold('other')}")

    # 4. 多关键词测试
    print("\n4. 多关键词搜索测试...")
    keywords = ['AI', 'ChatGPT']
    all_notes = fetcher.fetch_multiple_keywords(keywords, max_count_per_keyword=3)
    print(f"   获取笔记数: {len(all_notes)}")

    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)

    print("\n📋 使用真实数据步骤:")
    print("  1. 确保 RedNote MCP 已安装: which rednote-mcp")
    print("  2. 登录小红书: rednote-mcp init")
    print("  3. 重新运行抓取")


if __name__ == "__main__":
    main()
