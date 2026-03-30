"""
完整的小红书热门文章抓取演示
包含：模拟数据 + 数据库存储 + 报告生成
"""
import sys
import json
from pathlib import Path
from datetime import datetime
import importlib.util

# 添加项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载模块
spec = importlib.util.spec_from_file_location(
    "xiaohongshu_fetcher",
    project_root / "1_热点监控/fetchers/xiaohongshu_fetcher.py"
)
fetcher_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetcher_module)


def demo_with_mock_data():
    """使用模拟数据的完整演示"""
    print("="*80)
    print("🚀 小红书热门文章抓取演示")
    print("="*80)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    # 1. 初始化
    print("\n【步骤 1】初始化抓取器")
    print("-"*80)
    fetcher = fetcher_module.XiaohongshuHotFetcher(use_mcp='rednote')
    print(f"✓ MCP 状态: {'已连接' if fetcher.mcp_available else '未连接（使用模拟数据）'}")

    # 2. 抓取多个关键词
    print("\n【步骤 2】抓取热门文章")
    print("-"*80)
    keywords = ['AI', 'ChatGPT', 'AIGC']
    print(f"监控关键词: {', '.join(keywords)}\n")

    all_notes = []
    for keyword in keywords:
        print(f"\n关键词: {keyword}")
        print("  正在抓取...")

        # 使用模拟数据
        notes = fetcher._get_mock_data(keyword, 5)

        # 计算热度
        for note in notes:
            note['hot_score'] = fetcher.calculate_hot_score(note)

        # 筛选热门
        threshold = fetcher.get_threshold(keyword)
        hot_notes = [n for n in notes if n['hot_score'] >= threshold]

        print(f"  ✓ 获取: {len(notes)} 条")
        print(f"  ✓ 热门: {len(hot_notes)} 条（阈值: {threshold}）")

        all_notes.extend(hot_notes)

    # 3. 排序
    print("\n【步骤 3】热度排序")
    print("-"*80)
    all_notes.sort(key=lambda x: x['hot_score'], reverse=True)
    print(f"✓ 总计: {len(all_notes)} 条热门笔记")

    # 4. 显示 Top 10
    print("\n【步骤 4】热门 Top 10")
    print("-"*80)
    for i, note in enumerate(all_notes[:10], 1):
        print(f"\n{i}. {note['title']}")
        print(f"   热度分数: {note['hot_score']:.2f}")
        print(f"   互动数据: 👍 {note['likes']} | ⭐ {note['collects']} | 💬 {note['comments']} | 🔄 {note['shares']}")
        print(f"   作者: {note['author']}")
        print(f"   链接: {note['url']}")

    # 5. 保存到数据库（演示）
    print("\n【步骤 5】保存到数据库")
    print("-"*80)
    try:
        from common.database import Database
        db = Database()

        saved = 0
        for note in all_notes[:5]:  # 演示只保存前 5 条
            try:
                db.cursor.execute("""
                    INSERT OR REPLACE INTO hotspots
                    (platform, keyword, title, url, hot_score,
                     likes, collects, comments, shares,
                     author, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    'xiaohongshu',
                    'AI',
                    note['title'],
                    note['url'],
                    note['hot_score'],
                    note['likes'],
                    note['collects'],
                    note['comments'],
                    note['shares'],
                    note['author'],
                    datetime.now().isoformat()
                ))
                saved += 1
            except Exception as e:
                print(f"  ⚠️ 保存失败: {e}")

        db.conn.commit()
        print(f"✓ 已保存 {saved} 条热点到数据库")

        # 验证
        db.cursor.execute("""
            SELECT COUNT(*) FROM hotspots
            WHERE platform = 'xiaohongshu'
        """)
        count = db.cursor.fetchone()[0]
        print(f"✓ 数据库中共有 {count} 条小红书热点")

    except Exception as e:
        print(f"⚠️ 数据库操作失败: {e}")

    # 6. 生成报告
    print("\n【步骤 6】生成报告")
    print("-"*80)
    report_dir = project_root / "reports" / "xiaohongshu"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"hot_{datetime.now().strftime('%Y-%m-%d')}.md"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# 小红书热门日报 - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"**抓取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**关键词**: {', '.join(keywords)}\n")
        f.write(f"**热门笔记**: {len(all_notes)} 条\n\n")

        f.write("## 📊 热门 Top 10\n\n")

        for i, note in enumerate(all_notes[:10], 1):
            f.write(f"### {i}. {note['title']}\n\n")
            f.write(f"**热度**: {note['hot_score']:.2f}\n\n")
            f.write(f"**互动**:\n")
            f.write(f"- 点赞: {note['likes']}\n")
            f.write(f"- 收藏: {note['collects']}\n")
            f.write(f"- 评论: {note['comments']}\n")
            f.write(f"- 分享: {note['shares']}\n\n")
            f.write(f"**作者**: {note['author']}\n\n")
            f.write(f"**链接**: [{note['url']}]({note['url']})\n\n")
            f.write("---\n\n")

    print(f"✓ 报告已生成: {report_file}")

    # 完成
    print("\n" + "="*80)
    print("✅ 演示完成！")
    print("="*80)

    print("\n📋 总结:")
    print(f"  - 抓取关键词: {len(keywords)} 个")
    print(f"  - 获取笔记: {len(all_notes)} 条")
    print(f"  - 热门笔记: {len([n for n in all_notes if n['hot_score'] >= 300])} 条")
    print(f"  - 平均热度: {sum(n['hot_score'] for n in all_notes) / len(all_notes):.2f}")

    print("\n💡 使用真实数据:")
    print("  方式 1: 连接 RedNote MCP")
    print("    1. 运行: rednote-mcp init（登录小红书）")
    print("    2. 启动 MCP Server")
    print("    3. 通过 MCP 客户端调用 search_notes 工具")
    print()
    print("  方式 2: 使用 xiaohongshu-mcp (Go 版本)")
    print(f"    1. cd {project_root.parent}/xiaohongshu-mcp")
    print("    2. docker-compose up -d")
    print("    3. 通过 HTTP API 调用")

    print("\n" + "="*80)

    return all_notes


if __name__ == "__main__":
    demo_with_mock_data()
