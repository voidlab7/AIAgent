"""
数据库迁移脚本
更新 hotspots 表结构以支持小红书详细数据
"""
import sqlite3
from pathlib import Path
import sys

# 添加项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from common.config import DATABASE_PATH


def migrate():
    """执行数据库迁移"""
    print("="*60)
    print("数据库迁移：hotspots 表扩展")
    print("="*60)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 1. 备份现有数据
    print("\n1. 备份现有数据...")
    cursor.execute("SELECT COUNT(*) FROM hotspots")
    old_count = cursor.fetchone()[0]
    print(f"   现有记录数: {old_count}")
    
    if old_count > 0:
        cursor.execute("""
            CREATE TABLE hotspots_backup AS SELECT * FROM hotspots
        """)
        print("   ✓ 已备份到 hotspots_backup")
    
    # 2. 删除旧表
    print("\n2. 重建 hotspots 表...")
    cursor.execute("DROP TABLE IF EXISTS hotspots")
    
    # 3. 创建新表
    cursor.execute("""
        CREATE TABLE hotspots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,           -- 来源平台（xiaohongshu/weibo/zhihu）
            keyword TEXT NOT NULL,            -- 搜索关键词
            title TEXT,                       -- 笔记/热点标题
            url TEXT,                         -- 链接
            
            -- 小红书详细互动数据
            likes INTEGER DEFAULT 0,          -- 点赞数
            collects INTEGER DEFAULT 0,       -- 收藏数
            comments INTEGER DEFAULT 0,       -- 评论数
            shares INTEGER DEFAULT 0,         -- 分享数
            hot_score REAL DEFAULT 0,         -- 热度分数
            
            -- 其他平台通用字段
            rank INTEGER,                     -- 排名
            heat_value INTEGER,               -- 原始热度值
            description TEXT,                 -- 描述
            
            -- 元数据
            author TEXT,                      -- 作者
            publish_time TEXT,                -- 发布时间
            fetched_at TEXT,                  -- 抓取时间
            raw_data TEXT,                    -- 原始 JSON 数据
            
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            UNIQUE(platform, keyword, title, date(fetched_at))
        )
    """)
    print("   ✓ 新表创建成功")
    
    # 4. 恢复数据（如果有的话）
    if old_count > 0:
        print("\n3. 恢复数据...")
        try:
            cursor.execute("""
                INSERT INTO hotspots 
                (platform, keyword, title, url, rank, heat_value, description, created_at)
                SELECT 
                    source as platform,
                    keyword,
                    keyword as title,
                    url,
                    rank,
                    heat_value,
                    description,
                    created_at
                FROM hotspots_backup
            """)
            print(f"   ✓ 已恢复 {cursor.rowcount} 条记录")
        except Exception as e:
            print(f"   ⚠️  恢复失败: {e}")
            print("   备份数据保留在 hotspots_backup 表中")
    
    # 5. 创建索引
    print("\n4. 创建索引...")
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_hotspots_platform 
        ON hotspots(platform)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_hotspots_keyword 
        ON hotspots(keyword)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_hotspots_score 
        ON hotspots(hot_score DESC)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_hotspots_fetched 
        ON hotspots(fetched_at)
    """)
    print("   ✓ 索引创建成功")
    
    # 6. 验证
    print("\n5. 验证迁移...")
    cursor.execute("SELECT COUNT(*) FROM hotspots")
    new_count = cursor.fetchone()[0]
    print(f"   新表记录数: {new_count}")
    
    cursor.execute("PRAGMA table_info(hotspots)")
    columns = cursor.fetchall()
    print(f"   表字段数: {len(columns)}")
    print("\n   字段列表:")
    for col in columns:
        print(f"     - {col[1]} ({col[2]})")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ 迁移完成！")
    print("="*60)


if __name__ == "__main__":
    migrate()
