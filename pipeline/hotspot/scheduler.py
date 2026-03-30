"""
定时任务调度器
每天自动抓取小红书热门文章
"""
import schedule
import time
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path
import sys

# 添加项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from 1_热点监控.fetchers.xiaohongshu_fetcher import XiaohongshuHotFetcher
from common.database import Database


class HotspotScheduler:
    """热点抓取调度器"""
    
    # 默认监控关键词
    DEFAULT_KEYWORDS = [
        "AI",
        "ChatGPT",
        "AIGC",
        "人工智能",
        "大模型",
        "机器学习",
    ]
    
    # 抓取配置
    CONFIG = {
        'fetch_time': '02:00',      # 凌晨 2 点抓取
        'max_notes_per_keyword': 20,
        'enable_notifications': True,
    }
    
    def __init__(self, keywords: List[str] = None):
        """
        初始化调度器
        
        Args:
            keywords: 监控关键词列表
        """
        self.keywords = keywords or self.DEFAULT_KEYWORDS
        self.fetcher = XiaohongshuHotFetcher(use_mcp="rednote")
        self.db = Database()
        
        print(f"✓ 调度器初始化完成")
        print(f"  监控关键词: {', '.join(self.keywords)}")
        print(f"  抓取时间: {self.CONFIG['fetch_time']}")
    
    def job_fetch_xiaohongshu(self):
        """
        定时任务：抓取小红书热门
        """
        print(f"\n{'='*80}")
        print(f"⏰ 开始定时抓取 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print('='*80)
        
        try:
            # 1. 多关键词抓取
            print(f"\n📋 关键词列表: {', '.join(self.keywords)}")
            
            all_notes = self.fetcher.fetch_multiple_keywords(
                self.keywords,
                max_count_per_keyword=self.CONFIG['max_notes_per_keyword']
            )
            
            # 2. 保存到数据库
            if all_notes:
                print(f"\n💾 保存到数据库...")
                for keyword in self.keywords:
                    keyword_notes = [n for n in all_notes 
                                   if keyword in n.get('tags', []) or 
                                   keyword in n.get('title', '')]
                    if keyword_notes:
                        self.fetcher.save_to_database(keyword_notes, keyword)
                
                # 3. 生成报告
                self._generate_daily_report(all_notes)
                
                # 4. 发送通知（可选）
                if self.CONFIG['enable_notifications']:
                    self._send_notification(all_notes)
            else:
                print("\n⚠️  未获取到任何笔记")
            
            print(f"\n✅ 抓取完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"\n❌ 抓取失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_daily_report(self, notes: List[Dict]):
        """
        生成每日报告
        
        Args:
            notes: 笔记列表
        """
        report_dir = project_root / "reports" / "xiaohongshu"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"hot_{datetime.now().strftime('%Y-%m-%d')}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# 小红书热门日报 - {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(f"**抓取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**监控关键词**: {', '.join(self.keywords)}\n")
            f.write(f"**热门笔记数**: {len(notes)}\n\n")
            
            f.write("## 📊 热门 Top 20\n\n")
            
            for i, note in enumerate(notes[:20], 1):
                f.write(f"### {i}. {note.get('title', 'N/A')}\n\n")
                f.write(f"**热度分数**: {note.get('hot_score', 0):.2f}\n\n")
                f.write(f"**互动数据**:\n")
                f.write(f"- 点赞: {note.get('likes', 0)}\n")
                f.write(f"- 收藏: {note.get('collects', 0)}\n")
                f.write(f"- 评论: {note.get('comments', 0)}\n")
                f.write(f"- 分享: {note.get('shares', 0)}\n\n")
                f.write(f"**作者**: {note.get('author', 'N/A')}\n\n")
                f.write(f"**链接**: [{note.get('url', 'N/A')}]({note.get('url', '#')})\n\n")
                f.write(f"---\n\n")
        
        print(f"✓ 报告已生成: {report_file}")
    
    def _send_notification(self, notes: List[Dict]):
        """
        发送通知（可选实现）
        
        Args:
            notes: 笔记列表
        """
        # TODO: 实现通知功能
        # - 企业微信机器人
        # - 钉钉机器人
        # - 邮件通知
        
        top_5 = notes[:5]
        
        message = f"""
【小红书热门日报】
时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
关键词: {', '.join(self.keywords)}

Top 5 热门笔记:
"""
        for i, note in enumerate(top_5, 1):
            message += f"\n{i}. {note.get('title', 'N/A')[:30]}"
            message += f"\n   热度: {note.get('hot_score', 0):.2f}\n"
        
        print(f"\n📢 通知内容:\n{message}")
    
    def start(self):
        """
        启动定时任务
        """
        print(f"\n{'='*80}")
        print("🚀 启动定时任务调度器")
        print('='*80)
        print(f"⏰ 每天抓取时间: {self.CONFIG['fetch_time']}")
        print(f"📋 监控关键词: {len(self.keywords)} 个")
        print("\n按 Ctrl+C 停止...\n")
        
        # 设置定时任务
        schedule.every().day.at(self.CONFIG['fetch_time']).do(
            self.job_fetch_xiaohongshu
        )
        
        # 可选：每小时抓取一次（测试用）
        # schedule.every().hour.do(self.job_fetch_xiaohongshu)
        
        # 启动时立即执行一次（可选）
        print("🔄 启动时执行一次抓取...")
        self.job_fetch_xiaohongshu()
        
        # 循环运行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    
    def run_once(self):
        """
        运行一次（测试用）
        """
        self.job_fetch_xiaohongshu()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书热点抓取调度器")
    parser.add_argument('--once', action='store_true', 
                       help='立即执行一次（不启动定时任务）')
    parser.add_argument('--keywords', type=str, 
                       help='关键词列表，逗号分隔（如: AI,ChatGPT,AIGC）')
    parser.add_argument('--time', type=str, default='02:00',
                       help='每天抓取时间（默认: 02:00）')
    
    args = parser.parse_args()
    
    # 解析关键词
    keywords = None
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]
    
    # 创建调度器
    scheduler = HotspotScheduler(keywords=keywords)
    
    # 设置抓取时间
    if args.time:
        scheduler.CONFIG['fetch_time'] = args.time
    
    # 运行
    if args.once:
        scheduler.run_once()
    else:
        scheduler.start()


if __name__ == "__main__":
    main()
