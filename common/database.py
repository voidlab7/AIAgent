"""统一数据库模型"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import DATABASE_PATH


class Database:
    """数据库操作基类"""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._init_tables()

    def _init_tables(self):
        """初始化所有表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 1. 热点表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hotspots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,           -- 来源平台
                keyword TEXT NOT NULL,          -- 热点关键词
                rank INTEGER,                   -- 排名
                heat_value INTEGER,             -- 热度值
                url TEXT,                       -- 链接
                description TEXT,               -- 描述
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source, keyword, created_at)
            )
        """)

        # 2. 选题表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,            -- 选题标题
                angle TEXT,                     -- 创作角度
                source_hotspot_id INTEGER,      -- 关联热点
                status TEXT DEFAULT 'pending',  -- pending/writing/published
                estimated_traffic INTEGER,      -- 预期流量
                priority INTEGER DEFAULT 5,     -- 优先级 1-10
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_hotspot_id) REFERENCES hotspots(id)
            )
        """)

        # 3. 素材表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER,               -- 关联选题
                type TEXT NOT NULL,             -- 类型: article/data/quote/image
                title TEXT,
                content TEXT,
                source_url TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            )
        """)

        # 4. 文章表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER,               -- 关联选题
                title TEXT NOT NULL,
                content TEXT NOT NULL,          -- Markdown 内容
                cover_image TEXT,               -- 封面图 URL
                status TEXT DEFAULT 'draft',    -- draft/formatted/published
                word_count INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            )
        """)

        # 5. 配图表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,             -- 关联文章
                url TEXT NOT NULL,
                local_path TEXT,                -- 本地缓存路径
                alt_text TEXT,                  -- 图片描述
                source TEXT,                    -- 来源: unsplash/pexels/ai
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES articles(id)
            )
        """)

        # 6. 发布记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publish_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                platform TEXT NOT NULL,         -- weixin/xiaohongshu/zhihu
                platform_article_id TEXT,       -- 平台文章 ID
                status TEXT DEFAULT 'pending',  -- pending/published/failed
                scheduled_time DATETIME,        -- 定时发布时间
                published_time DATETIME,
                view_count INTEGER DEFAULT 0,
                like_count INTEGER DEFAULT 0,
                comment_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES articles(id)
            )
        """)

        conn.commit()
        conn.close()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """执行 SQL 语句"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor

    def fetchall(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """查询多条记录"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def fetchone(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """查询单条记录"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


# 全局数据库实例
db = Database()
