"""全局配置中心"""

import os
from pathlib import Path

# ========== 项目路径 ==========
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
CACHE_DIR = PROJECT_ROOT / "cache"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# ========== 数据库配置 ==========
DATABASE_PATH = DATA_DIR / "creator_assistant.db"

# ========== API 配置 ==========
# AI 服务
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# 搜索服务
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")  # Google Search API

# 图片服务
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# ========== 平台账号配置 ==========
# 微信公众号
WECHAT_APP_ID = os.getenv("WECHAT_APP_ID", "")
WECHAT_APP_SECRET = os.getenv("WECHAT_APP_SECRET", "")

# 小红书（通过 MCP）
XIAOHONGSHU_COOKIE_PATH = os.getenv("XIAOHONGSHU_COOKIE_PATH", "~/.mcp/rednote/cookies.json")

# ========== 内容策略配置 ==========
# 账号定位
ACCOUNT_PROFILE = {
    "name": "AI科技观察",
    "vertical": ["AI", "科技", "产品"],  # 垂直领域
    "tone": "专业、易懂、有趣",  # 内容风格
    "target_audience": "AI从业者、科技爱好者",  # 目标受众
}

# 选题关键词（继承自 ai_daily_fetcher）
TOPIC_KEYWORDS = [
    "OpenClaw", "小龙虾", "ClawdBot",
    "AI Agent", "大模型", "Claude", "GPT",
    "LangChain", "AutoGPT", "智能体",
]

# 内容长度偏好（字数）
CONTENT_LENGTH = {
    "weixin": (1500, 3000),    # 微信公众号
    "xiaohongshu": (300, 800),  # 小红书
    "zhihu": (1000, 2500),      # 知乎
}

# ========== 定时任务配置 ==========
# 刷热搜频率（分钟）
HOTSPOT_MONITOR_INTERVAL = 60

# 每日发布时间
PUBLISH_SCHEDULE = {
    "weixin": "08:00",      # 微信公众号 8:00
    "xiaohongshu": "19:00", # 小红书 19:00
}

# ========== 网络请求配置 ==========
REQUEST_TIMEOUT = 30
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}
MAX_RETRIES = 3

# ========== 日志配置 ==========
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
