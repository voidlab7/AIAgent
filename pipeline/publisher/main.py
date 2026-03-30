"""
模块7：登后台发布 (Publisher) - 主程序
"""
import argparse
import sys
from pathlib import Path
from typing import List, Optional
from datetime import datetime

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from common.database import Database
from platforms.xiaohongshu import XiaohongshuPublisher


class PublisherManager:
    """发布管理器"""
    
    def __init__(self):
        self.db = Database()
        self.publishers = {
            "xiaohongshu": XiaohongshuPublisher,
            # "weixin": WeixinPublisher,  # 待实现
            # "zhihu": ZhihuPublisher,    # 待实现
        }
    
    def get_article(self, article_id: int):
        """从数据库获取文章"""
        self.db.cursor.execute("""
            SELECT id, topic_id, title, content, cover_image, status
            FROM articles
            WHERE id = ?
        """, (article_id,))
        
        row = self.db.cursor.fetchone()
        if not row:
            raise ValueError(f"文章 ID {article_id} 不存在")
        
        return {
            "id": row[0],
            "topic_id": row[1],
            "title": row[2],
            "content": row[3],
            "cover_image": row[4],
            "status": row[5]
        }
    
    def get_article_images(self, article_id: int) -> List[str]:
        """获取文章的配图"""
        self.db.cursor.execute("""
            SELECT image_url
            FROM article_images
            WHERE article_id = ?
            ORDER BY position
        """, (article_id,))
        
        return [row[0] for row in self.db.cursor.fetchall()]
    
    def publish_to_platform(self, article_id: int, platform: str, 
                           account: str = "default", 
                           headless: bool = True,
                           **kwargs) -> dict:
        """发布到指定平台"""
        
        # 1. 获取文章数据
        article = self.get_article(article_id)
        images = self.get_article_images(article_id)
        
        # 添加封面图
        if article["cover_image"]:
            images.insert(0, article["cover_image"])
        
        print(f"\n📝 准备发布文章到 {platform}")
        print(f"   标题: {article['title']}")
        print(f"   正文: {len(article['content'])} 字")
        print(f"   图片: {len(images)} 张")
        
        # 2. 获取对应平台的发布器
        if platform not in self.publishers:
            return {
                "success": False,
                "message": f"不支持的平台: {platform}"
            }
        
        publisher_class = self.publishers[platform]
        publisher = publisher_class(account=account)
        
        # 3. 检查登录状态
        print(f"\n🔐 检查 {platform} 登录状态...")
        if not publisher.check_login():
            print(f"⚠️  未登录 {platform}，请先登录")
            return {
                "success": False,
                "message": f"未登录 {platform}"
            }
        
        print("✓ 已登录")
        
        # 4. 执行发布
        print(f"\n🚀 开始发布到 {platform}...")
        result = publisher.publish(
            title=article["title"],
            content=article["content"],
            images=images,
            headless=headless,
            **kwargs
        )
        
        # 5. 记录发布结果
        if result["success"]:
            publisher.log_publish(article_id, result)
            print(f"\n✅ 发布成功！")
            if result.get("url"):
                print(f"   文章链接: {result['url']}")
        else:
            print(f"\n❌ 发布失败: {result['message']}")
        
        return result
    
    def publish_to_multiple_platforms(self, article_id: int, 
                                      platforms: List[str],
                                      account: str = "default",
                                      headless: bool = True) -> dict:
        """发布到多个平台"""
        results = {}
        
        for platform in platforms:
            print(f"\n{'='*60}")
            print(f"发布到平台: {platform}")
            print('='*60)
            
            result = self.publish_to_platform(
                article_id, platform, account, headless
            )
            results[platform] = result
        
        # 汇总结果
        success_count = sum(1 for r in results.values() if r["success"])
        total_count = len(platforms)
        
        print(f"\n\n📊 发布汇总")
        print(f"   成功: {success_count}/{total_count}")
        for platform, result in results.items():
            status = "✅" if result["success"] else "❌"
            print(f"   {status} {platform}: {result['message']}")
        
        return results
    
    def list_publish_records(self, article_id: Optional[int] = None):
        """列出发布记录"""
        if article_id:
            query = """
                SELECT pr.id, pr.article_id, a.title, pr.platform, 
                       pr.status, pr.published_at, pr.url
                FROM publish_records pr
                JOIN articles a ON pr.article_id = a.id
                WHERE pr.article_id = ?
                ORDER BY pr.published_at DESC
            """
            self.db.cursor.execute(query, (article_id,))
        else:
            query = """
                SELECT pr.id, pr.article_id, a.title, pr.platform, 
                       pr.status, pr.published_at, pr.url
                FROM publish_records pr
                JOIN articles a ON pr.article_id = a.id
                ORDER BY pr.published_at DESC
                LIMIT 20
            """
            self.db.cursor.execute(query)
        
        records = self.db.cursor.fetchall()
        
        if not records:
            print("暂无发布记录")
            return
        
        print(f"\n{'='*80}")
        print(f"{'ID':<6} {'文章ID':<8} {'标题':<30} {'平台':<12} {'状态':<8} {'发布时间':<20}")
        print('='*80)
        
        for record in records:
            record_id, art_id, title, platform, status, pub_at, url = record
            title = title[:28] + "..." if len(title) > 30 else title
            pub_time = pub_at[:19] if pub_at else ""
            
            print(f"{record_id:<6} {art_id:<8} {title:<30} {platform:<12} {status:<8} {pub_time:<20}")
        
        print('='*80)


def main():
    parser = argparse.ArgumentParser(description="模块7：登后台发布")
    
    parser.add_argument("--article-id", type=int, help="文章ID")
    parser.add_argument("--platform", type=str, 
                       choices=["xiaohongshu", "weixin", "zhihu"],
                       help="发布平台")
    parser.add_argument("--platforms", type=str, 
                       help="多个平台，逗号分隔（如: xiaohongshu,weixin）")
    parser.add_argument("--account", type=str, default="default",
                       help="账号名称（默认: default）")
    parser.add_argument("--headless", action="store_true", default=True,
                       help="无头模式（默认开启）")
    parser.add_argument("--with-window", action="store_true",
                       help="显示浏览器窗口")
    parser.add_argument("--mode", type=str, default="image",
                       choices=["image", "long-article"],
                       help="发布模式（小红书）：image=图文，long-article=长文")
    parser.add_argument("--list", action="store_true",
                       help="列出发布记录")
    parser.add_argument("--schedule", type=str,
                       help="定时发布（格式: 2026-03-11 08:00）")
    
    args = parser.parse_args()
    
    manager = PublisherManager()
    
    # 列出发布记录
    if args.list:
        manager.list_publish_records(args.article_id)
        return
    
    # 检查必要参数
    if not args.article_id:
        print("错误: 请指定 --article-id")
        parser.print_help()
        sys.exit(1)
    
    if not args.platform and not args.platforms:
        print("错误: 请指定 --platform 或 --platforms")
        parser.print_help()
        sys.exit(1)
    
    # 定时发布
    if args.schedule:
        # TODO: 实现定时发布
        print(f"⏰ 定时发布功能待实现: {args.schedule}")
        sys.exit(1)
    
    # 确定是否使用无头模式
    headless = not args.with_window
    
    # 发布到单个或多个平台
    if args.platforms:
        platforms = [p.strip() for p in args.platforms.split(",")]
        manager.publish_to_multiple_platforms(
            args.article_id, platforms, args.account, headless
        )
    else:
        manager.publish_to_platform(
            args.article_id, args.platform, args.account, headless,
            mode=args.mode
        )


if __name__ == "__main__":
    main()
