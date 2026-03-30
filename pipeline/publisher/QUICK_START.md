# 快速开始：小红书发布集成

## ✅ 集成已完成

post-to-xhs Skill 已成功集成到模块7（发布模块）！

## 📁 文件结构

```
AIAgent/
├── 7_内容发布/                  # 发布模块
│   ├── main.py                  # 主入口（CLI）
│   ├── platforms/               # 平台发布器
│   │   ├── base.py             # 基类
│   │   └── xiaohongshu.py      # 小红书发布器
│   ├── INTEGRATION_GUIDE.md    # 详细集成文档
│   ├── QUICK_START.md          # 本文档
│   └── test_integration.py     # 测试脚本
│
└── skills/post-to-xhs/          # 小红书发布 Skill（已复制）
    ├── SKILL.md                 # Skill 定义
    ├── scripts/                 # Python 脚本（CDP自动化）
    │   ├── publish_pipeline.py # 主流程
    │   ├── cdp_publish.py      # CDP 核心
    │   ├── chrome_launcher.py  # Chrome 管理
    │   └── ...
    └── config/                  # 配置文件
```

## 🚀 3 步开始使用

### 1. 安装依赖
```bash
cd AIAgent
pip install websockets requests
```

### 2. 登录小红书（首次）
```bash
cd skills/post-to-xhs/scripts
python cdp_publish.py login
# 会打开浏览器，扫码登录小红书
```

### 3. 发布文章
```bash
cd ../../7_内容发布

# 发布 ID=1 的文章（需要先在数据库中有文章记录）
python main.py --article-id 1 --platform xiaohongshu
```

## 💻 Python API 示例

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# 方法1：使用 subprocess 直接调用脚本
import subprocess

result = subprocess.run([
    "python",
    "skills/post-to-xhs/scripts/publish_pipeline.py",
    "--title-file", "title.txt",
    "--content-file", "content.txt",
    "--image-urls", "https://example.com/image.jpg",
    "--headless"
], capture_output=True, text=True)

print(result.stdout)
```

## 📚 更多信息

- **详细文档**: `INTEGRATION_GUIDE.md`
- **Skill 文档**: `../skills/post-to-xhs/SKILL.md`
- **技术实现**: `../skills/post-to-xhs/references/publish-workflow.md`
