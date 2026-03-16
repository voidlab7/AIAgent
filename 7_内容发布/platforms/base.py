"""
发布器基类
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime


class PublisherBase(ABC):
    """发布器基类"""
    
    def __init__(self, account: str = "default"):
        self.account = account
        self.platform_name = self.__class__.__name__.replace("Publisher", "").lower()
    
    @abstractmethod
    def publish(self, 
                title: str, 
                content: str, 
                images: Optional[List[str]] = None,
                **kwargs) -> Dict:
        """
        发布内容到平台
        
        Args:
            title: 标题
            content: 正文
            images: 图片路径或URL列表
            **kwargs: 平台特定参数
            
        Returns:
            {
                "success": bool,
                "article_id": str,  # 平台文章ID
                "url": str,         # 文章URL
                "message": str      # 状态信息
            }
        """
        pass
    
    @abstractmethod
    def check_login(self) -> bool:
        """检查登录状态"""
        pass
    
    def validate_content(self, title: str, content: str) -> Dict:
        """验证内容格式"""
        errors = []
        
        if not title or not title.strip():
            errors.append("标题不能为空")
        
        if not content or not content.strip():
            errors.append("正文不能为空")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def log_publish(self, article_id: int, result: Dict):
        """记录发布结果到数据库"""
        from common.database import Database
        
        db = Database()
        db.cursor.execute("""
            INSERT INTO publish_records 
            (article_id, platform, platform_article_id, url, status, published_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            article_id,
            self.platform_name,
            result.get("article_id", ""),
            result.get("url", ""),
            "success" if result.get("success") else "failed",
            datetime.now().isoformat()
        ))
        db.conn.commit()
