# 模块7：发布模块集成指南

## 📦 已集成的 Skills

### post-to-xhs Skill
- **路径**: `/skills/post-to-xhs/`
- **功能**: 小红书内容自动发布
- **技术**: Chrome DevTools Protocol (CDP)
- **模式**: 
  - 图文模式（默认）：图片 + 短文
  - 长文模式：长篇文章 + 排版模板

---

## 🏗️ 架构设计

```
7_内容发布/                       # 发布模块
├── main.py                        # 主入口
├── platforms/                     # 平台发布器
│   ├── base.py                   # 发布器基类
│   ├── xiaohongshu.py           # 小红书（集成 post-to-xhs）
│   ├── weixin.py                # 微信公众号（待实现）
│   └── zhihu.py                 # 知乎（待实现）
├── scheduler.py                  # 定时发布（待实现）
├── tracker.py                    # 效果追踪（待实现）
└── INTEGRATION_GUIDE.md          # 本文档

../skills/post-to-xhs/            # 小红书发布 Skill
├── SKILL.md                      # Skill 定义
├── scripts/                      # 核心脚本
│   ├── publish_pipeline.py      # 主发布流程
│   ├── cdp_publish.py           # CDP 核心操作
│   ├── chrome_launcher.py       # Chrome 启动管理
│   ├── account_manager.py       # 多账号管理
│   └── image_downloader.py      # 图片下载
├── config/                       # 配置文件
│   └── accounts.json            # 账号配置
└── references/                   # 参考文档
    └── publish-workflow.md      # 发布流程技术文档
```

---

## 🚀 快速开始

### 1. 准备工作

#### 安装 Python 依赖
```bash
cd AIAgent
pip install websockets requests
```

#### 验证 Chrome 浏览器
```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# 确保版本 >= 90
```

#### 初次登录小红书
```bash
cd 7_内容发布
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('..').resolve()))
from platforms.xiaohongshu import XiaohongshuPublisher

publisher = XiaohongshuPublisher()
print('检查登录状态...')
if not publisher.check_login():
    print('请在浏览器中登录小红书')
    # 手动运行登录命令
"
```

或直接运行：
```bash
cd ../skills/post-to-xhs/scripts
python cdp_publish.py login
```

### 2. 基本使用

#### 发布文章到小红书（图文模式）

```bash
cd 7_内容发布

# 发布 ID=1 的文章到小红书（无头模式，推荐）
python main.py --article-id 1 --platform xiaohongshu

# 显示浏览器窗口（可预览）
python main.py --article-id 1 --platform xiaohongshu --with-window

# 使用指定账号
python main.py --article-id 1 --platform xiaohongshu --account myaccount
```

#### 批量发布到多个平台

```bash
# 同时发布到小红书和微信公众号
python main.py --article-id 1 --platforms xiaohongshu,weixin
```

#### 查看发布记录

```bash
# 查看最近 20 条发布记录
python main.py --list

# 查看指定文章的发布记录
python main.py --article-id 1 --list
```

---

## 💻 Python API 使用

### 方式 1：使用 PublisherManager

```python
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from 7_内容发布.main import PublisherManager

# 创建管理器
manager = PublisherManager()

# 发布到小红书
result = manager.publish_to_platform(
    article_id=1,
    platform="xiaohongshu",
    account="default",
    headless=True
)

print(f"发布结果: {result}")
```

### 方式 2：直接使用 Publisher

```python
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from 7_内容发布.platforms.xiaohongshu import XiaohongshuPublisher

# 创建发布器
publisher = XiaohongshuPublisher(account="default")

# 检查登录
if not publisher.check_login():
    print("请先登录小红书")
    exit(1)

# 发布内容
result = publisher.publish(
    title="我的标题",
    content="这是正文内容\n\n第二段",
    images=[
        "https://example.com/image1.jpg",
        "/path/to/local/image2.jpg"
    ],
    mode="image",      # 图文模式
    headless=True      # 无头模式
)

print(f"发布结果: {result}")
```

### 方式 3：快速发布（便捷函数）

```python
from 7_内容发布.platforms.xiaohongshu import quick_publish

result = quick_publish(
    title="我的标题",
    content="这是正文",
    images=["https://example.com/image.jpg"],
    account="default",
    headless=True
)
```

---

## 🔧 高级功能

### 多账号管理

```bash
cd ../skills/post-to-xhs/scripts

# 列出所有账号
python cdp_publish.py list-accounts

# 添加新账号
python cdp_publish.py add-account myaccount --alias "我的账号"

# 登录指定账号
python cdp_publish.py --account myaccount login

# 切换账号
python cdp_publish.py --account myaccount switch-account

# 设置默认账号
python cdp_publish.py set-default-account myaccount
```

在发布时使用指定账号：
```bash
python main.py --article-id 1 --platform xiaohongshu --account myaccount
```

### 长文模式（待完善）

```bash
# 使用长文模式发布
python main.py --article-id 1 --platform xiaohongshu --mode long-article
```

**注意**：长文模式需要用户选择排版模板，目前需要手动交互。

---

## 📊 数据库集成

发布记录会自动保存到 `publish_records` 表：

```sql
-- 查询发布记录
SELECT 
    pr.id,
    pr.article_id,
    a.title,
    pr.platform,
    pr.status,
    pr.published_at,
    pr.url
FROM publish_records pr
JOIN articles a ON pr.article_id = a.id
ORDER BY pr.published_at DESC;
```

Python API：
```python
from common.database import Database

db = Database()
db.cursor.execute("""
    SELECT * FROM publish_records 
    WHERE article_id = ? AND platform = ?
""", (1, "xiaohongshu"))

records = db.cursor.fetchall()
```

---

## 🔄 与其他模块集成

### 完整工作流示例

```python
"""
完整的自媒体创作工作流
模块 1-7 串联使用
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 模块 1: 刷热搜
from 1_热点监控.main import HotspotMonitor
monitor = HotspotMonitor()
hotspots = monitor.fetch_all()
print(f"获取到 {len(hotspots)} 条热点")

# 模块 2: 找选题
from 2_选题筛选.main import TopicSelector
selector = TopicSelector()
topics = selector.generate_topics(hotspots)
selected_topic = topics[0]  # 选择第一个选题

# 模块 3: 搜资料
from 3_素材采集.main import MaterialCollector
collector = MaterialCollector()
materials = collector.collect(selected_topic['id'])

# 模块 4: 写稿
from 4_内容创作.main import ContentWriter
writer = ContentWriter()
article = writer.generate(selected_topic['id'], materials)

# 模块 5: 找配图
from 5_配图查找.main import ImageFinder
finder = ImageFinder()
images = finder.find(article['id'])

# 模块 6: 排版
from 6_格式优化.main import Formatter
formatter = Formatter()
formatted = formatter.format(article['id'], platform="xiaohongshu")

# 模块 7: 发布
from 7_内容发布.main import PublisherManager
publisher = PublisherManager()
result = publisher.publish_to_platform(
    article_id=article['id'],
    platform="xiaohongshu",
    headless=True
)

print(f"\n🎉 完整工作流执行完成！")
print(f"   文章ID: {article['id']}")
print(f"   发布状态: {result['message']}")
```

---

## ⚠️ 常见问题

### 1. Chrome 无法启动

**问题**：提示找不到 Chrome 可执行文件

**解决**：
```python
# 编辑 skills/post-to-xhs/scripts/chrome_launcher.py
# 修改 CHROME_PATH 为你的 Chrome 路径

# macOS
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Windows
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
```

### 2. 登录状态丢失

**问题**：每次都需要重新登录

**解决**：检查用户数据目录是否有写入权限
```bash
# macOS/Linux
ls -la ~/Library/Application\ Support/Google/Chrome/XiaohongshuProfile

# 如果不存在，手动创建
mkdir -p ~/Library/Application\ Support/Google/Chrome/XiaohongshuProfile
```

### 3. 标题过长

**问题**：提示标题长度超过 38

**解决**：
- 小红书标题限制：中文计2，英文计1，最大38
- 使用工具检查：
```python
from 7_内容发布.platforms.xiaohongshu import XiaohongshuPublisher

publisher = XiaohongshuPublisher()
title = "我的标题ABC"
length = publisher._calculate_title_length(title)
print(f"标题长度: {length}/38")
```

### 4. 图片上传失败

**问题**：图片 URL 无法访问或本地文件不存在

**解决**：
- 确保图片 URL 可公开访问
- 本地图片使用绝对路径
- 检查图片格式（支持 jpg, png, gif）

---

## 🛠️ 扩展开发

### 添加新的发布平台

1. **创建发布器类**
```python
# 7_内容发布/platforms/myplatform.py

from .base import PublisherBase

class MyPlatformPublisher(PublisherBase):
    def check_login(self) -> bool:
        # 实现登录检查逻辑
        pass
    
    def publish(self, title: str, content: str, 
                images=None, **kwargs) -> dict:
        # 实现发布逻辑
        pass
```

2. **注册到管理器**
```python
# 7_内容发布/main.py

class PublisherManager:
    def __init__(self):
        self.publishers = {
            "xiaohongshu": XiaohongshuPublisher,
            "myplatform": MyPlatformPublisher,  # 添加这行
        }
```

3. **使用新平台**
```bash
python main.py --article-id 1 --platform myplatform
```

---

## 📚 参考资料

- **post-to-xhs Skill 文档**: `../skills/post-to-xhs/SKILL.md`
- **发布流程技术文档**: `../skills/post-to-xhs/references/publish-workflow.md`
- **Chrome DevTools Protocol**: https://chromedevtools.github.io/devtools-protocol/

---

## 🚧 待开发功能

- [ ] 微信公众号发布器 (`platforms/weixin.py`)
- [ ] 知乎发布器 (`platforms/zhihu.py`)
- [ ] 定时发布功能 (`scheduler.py`)
- [ ] 效果追踪功能 (`tracker.py`)
- [ ] 长文模式完整实现
- [ ] 发布失败自动重试
- [ ] 发布前内容预览（Web UI）

---

## 💬 反馈与贡献

如有问题或建议，请在项目中提 Issue 或直接修改代码。
