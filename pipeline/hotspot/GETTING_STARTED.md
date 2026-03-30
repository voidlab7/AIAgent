# 小红书热门文章自动抓取 - 完整方案

## ✅ 已完成

我已经为你创建了完整的小红书热门文章自动抓取系统！

---

## 📂 项目结构

```
AIAgent/1_热点监控/
├── fetchers/
│   └── xiaohongshu_fetcher.py  # 小红书抓取器（支持 MCP）
├── docs/
│   └── xiaohongshu_hot_metrics.md  # 热度定义文档
├── scheduler.py              # 定时任务调度器
├── config.json               # 配置文件
├── HOW_TO_USE.md            # 详细使用指南
├── quick_start.sh           # 一键启动脚本
└── README.md                # 模块说明
```

---

## 🎯 "最热"的定义

### 热度计算公式
```
热度分数 = (点赞×1.0 + 收藏×1.5 + 评论×2.0 + 分享×3.0) 
          / (发布时间小时数 + 1)^0.8
```

### 核心指标
| 指标 | 权重 | 说明 |
|------|------|------|
| 分享 | 3.0 | 传播力，权重最高 |
| 评论 | 2.0 | 讨论热度 |
| 收藏 | 1.5 | 小红书特征（种草意向）|
| 点赞 | 1.0 | 基础认可度 |

### 热门阈值
- AI 类：≥ 300
- 科技类：≥ 400
- 生活类：≥ 800

---

## 🚀 快速开始（3 步）

### 第 1 步：安装依赖
```bash
cd /Users/voidzhang/Documents/workspace/AIAgent
pip install schedule
```

### 第 2 步：确保 MCP 可用
```bash
# 检查 RedNote MCP
which rednote-mcp

# 如果未安装
npm install -g rednote-mcp

# 首次登录小红书
rednote-mcp init
```

### 第 3 步：开始抓取
```bash
cd 1_热点监控

# 方式 A：一键启动（推荐）
./quick_start.sh

# 方式 B：立即执行一次
python scheduler.py --once

# 方式 C：启动定时任务（每天凌晨 2 点）
nohup python scheduler.py > ../logs/hotspot.log 2>&1 &
```

---

## 📋 使用示例

### 示例 1：搜索单个关键词
```python
from 1_热点监控.fetchers.xiaohongshu_fetcher import XiaohongshuHotFetcher

fetcher = XiaohongshuHotFetcher()
notes = fetcher.fetch_by_keyword("AI", max_count=20)

# 查看前 5 条
for note in notes[:5]:
    print(f"{note['title']}")
    print(f"热度: {note['hot_score']:.2f}")
    print(f"点赞: {note['likes']} | 收藏: {note['collects']}")
```

### 示例 2：多关键词监控
```python
keywords = ["AI", "ChatGPT", "AIGC", "人工智能"]
notes = fetcher.fetch_multiple_keywords(keywords)

# 保存到数据库
fetcher.save_to_database(notes, "AI")
```

### 示例 3：查看抓取结果
```bash
# 查看今日报告
cat reports/xiaohongshu/hot_$(date +%Y-%m-%d).md

# 查看数据库
sqlite3 data/ai_agent.db
sqlite> SELECT title, hot_score, likes 
        FROM hotspots 
        WHERE platform='xiaohongshu' 
        ORDER BY hot_score DESC 
        LIMIT 10;
```

---

## 🔧 自定义配置

编辑 `config.json`：
```json
{
  "keywords": [
    "AI",
    "ChatGPT",
    "AIGC",
    "人工智能",
    "大模型"
  ],
  "fetch_time": "02:00",
  "max_notes_per_keyword": 20,
  "hot_threshold": {
    "AI": 300,
    "default": 500
  }
}
```

---

## 📊 输出示例

### 命令行输出
```
================================================================================
⏰ 开始定时抓取 - 2026-03-10 02:00:00
================================================================================

📋 关键词列表: AI, ChatGPT, AIGC, 人工智能

搜索关键词: AI
排序方式: hot
------------------------------------------------------------
✓ 获取到 20 条笔记
✓ 筛选出 15 条热门笔记

搜索关键词: ChatGPT
------------------------------------------------------------
✓ 获取到 18 条笔记
✓ 筛选出 12 条热门笔记

✓ 总计获取 42 条不重复的热门笔记

💾 保存到数据库...
✓ 已保存 42 条热点到数据库

✓ 报告已生成: reports/xiaohongshu/hot_2026-03-10.md

✅ 抓取完成 - 2026-03-10 02:05:32
```

### Markdown 报告
```markdown
# 小红书热门日报 - 2026-03-10

**抓取时间**: 2026-03-10 02:00:00
**监控关键词**: AI, ChatGPT, AIGC, 人工智能
**热门笔记数**: 42

## 📊 热门 Top 20

### 1. AI工具推荐：ChatGPT 必备插件

**热度分数**: 1250.50

**互动数据**:
- 点赞: 5000
- 收藏: 3000
- 评论: 800
- 分享: 150

**作者**: 科技博主小王

**链接**: [https://xiaohongshu.com/note/...](...)
```

---

## 🔄 与 MCP 的集成方式

### 方式 1：RedNote MCP（已安装）
```python
# 通过 npx 调用
npx rednote-mcp search --keyword "AI" --limit 20 --sort hot

# 或通过 Python subprocess
import subprocess
result = subprocess.run([
    "npx", "rednote-mcp", "search",
    "--keyword", "AI",
    "--limit", "20",
    "--sort", "hot"
], capture_output=True, text=True)
```

### 方式 2：xiaohongshu-mcp（Go 版本）
```bash
# 需要 Docker 部署
cd /Users/voidzhang/Documents/workspace/xiaohongshu-mcp
docker-compose up -d

# 然后通过 HTTP API 调用
curl http://localhost:8080/search?keyword=AI&limit=20
```

---

## 📈 高级功能

### 1. 热度趋势分析
```python
import matplotlib.pyplot as plt
from common.database import Database

db = Database()
db.cursor.execute("""
    SELECT date(fetched_at), AVG(hot_score)
    FROM hotspots
    WHERE platform = 'xiaohongshu'
    AND fetched_at >= date('now', '-7 days')
    GROUP BY date(fetched_at)
""")

data = db.cursor.fetchall()
plt.plot([r[0] for r in data], [r[1] for r in data])
plt.savefig('trend.png')
```

### 2. 关键词对比
```python
keywords = ['AI', 'ChatGPT', 'AIGC']

for kw in keywords:
    db.cursor.execute("""
        SELECT AVG(hot_score)
        FROM hotspots
        WHERE keyword = ?
    """, (kw,))
    
    avg = db.cursor.fetchone()[0]
    print(f"{kw}: {avg:.2f}")
```

### 3. 自动通知
```python
# 企业微信机器人
import requests

webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..."

message = {
    "msgtype": "markdown",
    "markdown": {
        "content": f"## 小红书热门日报\n\nTop 5: ..."
    }
}

requests.post(webhook, json=message)
```

---

## ⚠️ 注意事项

1. **MCP 登录**：确保已执行 `rednote-mcp init`
2. **频率限制**：建议每天 1 次，避免频繁请求
3. **数据去重**：系统自动基于笔记 ID 去重
4. **隐私合规**：仅用于数据分析，不商用

---

## 📚 相关文档

| 文档 | 路径 |
|------|------|
| 详细使用指南 | `HOW_TO_USE.md` |
| 热度定义说明 | `docs/xiaohongshu_hot_metrics.md` |
| MCP 集成文档 | `../skills/post-to-xhs/SKILL.md` |
| 数据库设计 | `../common/database.py` |

---

## 🎯 下一步

1. ✅ **安装依赖**: `pip install schedule`
2. ✅ **登录 MCP**: `rednote-mcp init`
3. ✅ **测试抓取**: `python scheduler.py --once`
4. ✅ **查看报告**: `cat reports/xiaohongshu/hot_*.md`
5. ✅ **启动定时任务**: `nohup python scheduler.py &`

---

## 💡 推荐工作流

```
每天凌晨 2 点
    ↓
自动抓取小红书热门
    ↓
保存到数据库
    ↓
生成 Markdown 报告
    ↓
发送通知（可选）
    ↓
等待第二天
```

---

**🎉 完成！现在你可以开始使用自动抓取功能了！**

有问题随时问我！ 📢
