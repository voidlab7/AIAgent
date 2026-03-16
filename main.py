#!/usr/bin/env python3
"""AI 自媒体创作助手 - 主入口"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List, Dict

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from common.config import ACCOUNT_PROFILE, PUBLISH_SCHEDULE
from common.database import db


def init_project():
    """初始化项目"""
    print("🚀 初始化 AI 自媒体创作助手...")
    
    # 1. 创建必要目录
    print("  ✓ 创建数据目录")
    
    # 2. 初始化数据库
    print("  ✓ 初始化数据库")
    db._init_tables()
    
    # 3. 检查配置
    print(f"\n📋 账号配置：")
    print(f"  - 名称：{ACCOUNT_PROFILE['name']}")
    print(f"  - 垂直领域：{', '.join(ACCOUNT_PROFILE['vertical'])}")
    print(f"  - 目标受众：{ACCOUNT_PROFILE['target_audience']}")
    
    print(f"\n⏰ 发布计划：")
    for platform, time in PUBLISH_SCHEDULE.items():
        print(f"  - {platform}: {time}")
    
    print("\n✅ 初始化完成！")
    print("\n下一步：")
    print("  1. 复制 .env.example 为 .env，填写 API Keys")
    print("  2. 运行热搜监控：python main.py hotspot")
    print("  3. 运行趣味测试分析：python main.py funtest --demo")
    print("  4. 查看完整工作流：python main.py --help")


# ============ 关键词触发功能 ============

def check_keyword_trigger(text: str) -> Optional[str]:
    """
    检查用户输入是否触发关键词
    
    Args:
        text: 用户输入文本
        
    Returns:
        触发的命令类型，如果没有触发则返回None
    """
    try:
        # 使用选题筛选模块的触发器
        sys.path.insert(0, str(PROJECT_ROOT / "2_选题筛选"))
        from keyword_trigger import FunTestTrigger
        
        trigger = FunTestTrigger()
        if trigger.should_trigger(text):
            return "funtest"
    except ImportError:
        pass
    
    return None


def run_funtest_analysis(demo: bool = False, data_file: Optional[str] = None):
    """
    运行趣味测试分析
    
    Args:
        demo: 是否使用示例数据演示
        data_file: JSON数据文件路径
    """
    sys.path.insert(0, str(PROJECT_ROOT / "2_选题筛选"))
    
    from quick_start import run_with_mcp_data, demo_with_sample_data
    
    if demo:
        demo_with_sample_data()
    elif data_file:
        import json
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        run_with_mcp_data(data)
    else:
        # 显示使用说明
        print("""
🎯 趣味测试爆款选题分析

使用方式：
  python main.py funtest --demo           # 使用示例数据演示
  python main.py funtest --data xxx.json  # 使用指定JSON数据

或者通过聊天框触发：
  输入包含以下关键词的消息即可触发：
  - 趣味测试、心理测试、性格测试
  - 测试分析、测试报告、爆款选题
  - 小红书测试、MBTI测试

示例触发语句：
  "帮我分析一下小红书趣味测试的热点"
  "抓取趣味测试数据并生成报告"
  "小红书上爬取和分析当下最热门的趣味测试话题"
        """)


def run_module(module_name: str, *args):
    """运行指定模块"""
    module_map = {
        "hotspot": "1_热点监控.main",
        "topic": "2_选题筛选.main",
        "material": "3_素材采集.main",
        "write": "4_内容创作.main",
        "image": "5_配图查找.main",
        "format": "6_格式优化.main",
        "publish": "7_内容发布.main",
        "workflow": "workflows.daily_creator",
    }
    
    if module_name not in module_map:
        print(f"❌ 未知模块：{module_name}")
        print(f"可用模块：{', '.join(module_map.keys())}")
        sys.exit(1)
    
    module_path = module_map[module_name]
    print(f"🔧 运行模块：{module_path}")
    
    # 动态导入并执行
    # TODO: 实现各模块的 main 函数后取消注释
    # module = __import__(module_path, fromlist=["main"])
    # module.main(*args)
    
    print(f"⚠️  模块 {module_name} 尚未实现，请先开发对应的 main.py")


def main():
    parser = argparse.ArgumentParser(
        description="AI 自媒体创作助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  # 初始化项目
  python main.py init
  
  # 运行单个模块
  python main.py hotspot           # 刷热搜
  python main.py topic             # 生成选题
  python main.py write             # AI 写稿
  python main.py funtest --demo    # 趣味测试分析（示例数据）
  
  # 运行完整工作流
  python main.py workflow --once   # 执行一次完整流程
  python main.py workflow --daily  # 启动每日定时任务
  
  # 查看数据
  python main.py status            # 查看各模块状态
  
  # 关键词触发（示例）
  python main.py trigger "分析小红书趣味测试热点"
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["init", "hotspot", "topic", "material", "write", 
                 "image", "format", "publish", "workflow", "status",
                 "funtest", "trigger"],
        help="要执行的命令"
    )
    
    parser.add_argument("--once", action="store_true", help="执行一次")
    parser.add_argument("--daily", action="store_true", help="启动每日定时任务")
    parser.add_argument("--demo", action="store_true", help="使用示例数据演示")
    parser.add_argument("--data", type=str, help="JSON数据文件路径")
    parser.add_argument("text", nargs="*", help="触发文本（用于trigger命令）")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    if args.command == "init":
        init_project()
    elif args.command == "status":
        show_status()
    elif args.command == "funtest":
        run_funtest_analysis(demo=args.demo, data_file=args.data)
    elif args.command == "trigger":
        # 关键词触发
        trigger_text = " ".join(args.text) if args.text else ""
        if not trigger_text:
            print("请提供触发文本，例如：python main.py trigger '分析趣味测试热点'")
            sys.exit(1)
        
        triggered = check_keyword_trigger(trigger_text)
        if triggered == "funtest":
            print("🎯 检测到触发词：趣味测试分析")
            run_funtest_analysis(demo=True)  # 默认使用示例数据
        else:
            print(f"未识别的触发词：{trigger_text}")
    else:
        run_module(args.command)


def show_status():
    """显示各模块状态"""
    print("📊 系统状态\n")
    
    # 统计数据库数据
    hotspot_count = db.fetchone("SELECT COUNT(*) as cnt FROM hotspots")
    topic_count = db.fetchone("SELECT COUNT(*) as cnt FROM topics")
    article_count = db.fetchone("SELECT COUNT(*) as cnt FROM articles")
    publish_count = db.fetchone("SELECT COUNT(*) as cnt FROM publish_records WHERE status='published'")
    
    print(f"📈 数据统计：")
    print(f"  - 热点数据：{hotspot_count['cnt'] if hotspot_count else 0} 条")
    print(f"  - 待选选题：{topic_count['cnt'] if topic_count else 0} 个")
    print(f"  - 文章草稿：{article_count['cnt'] if article_count else 0} 篇")
    print(f"  - 已发布：{publish_count['cnt'] if publish_count else 0} 篇")
    
    print(f"\n🔧 模块状态：")
    modules = [
        ("1️⃣  刷热搜", "1_热点监控", "🚧 待开发"),
        ("2️⃣  找选题", "2_选题筛选", "✅ 趣味测试分析已就绪"),
        ("3️⃣  搜资料", "3_素材采集", "📋 待开发"),
        ("4️⃣  写稿", "4_内容创作", "📋 待开发"),
        ("5️⃣  找配图", "5_配图查找", "📋 待开发"),
        ("6️⃣  排版", "6_格式优化", "📋 待开发"),
        ("7️⃣  发布", "7_内容发布", "📋 待开发"),
    ]
    
    for name, path, status in modules:
        print(f"  {name} ({path}): {status}")
    
    # 显示趣味测试功能状态
    print(f"\n🎯 趣味测试分析功能：")
    print(f"  - 关键词触发：✅ 已启用")
    print(f"  - 支持关键词：趣味测试、心理测试、性格测试、MBTI测试等")
    print(f"  - 使用示例：python main.py funtest --demo")
    print(f"  - 触发示例：python main.py trigger '分析趣味测试热点'")


if __name__ == "__main__":
    main()
