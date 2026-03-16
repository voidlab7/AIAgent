# 小红书热门文章自动抓取 - 使用指南

## 📋 功能概述

自动每天抓取小红书上关于 AI 或指定主题的最热文章，实现：
- ✅ 定时抓取（每天凌晨 2 点）
- ✅ 多关键词监控
- ✅ 热度计算与排序
- ✅ 数据库存储
- ✅ 每日报告生成

---

## 🎯 "最热"的定义

### 热度计算公式
```
热度分数 = (点赞×1.0 + 收藏×1.5 + 评论×2.0 + 分享×3.0) 
          / (发布时间小时数 + 1)^0.8
```

**权重说明**：
- **分享 (×3.0)**：代表传播力，权重最高
- **评论 (×2.0)**：代表讨论热度
- **收藏 (×1.5)**：小红书是种草平台，收藏代表购买意向
- **点赞 (×1.0)**：基础认可度

**时间衰减**：发布时间越近，热度越高

### 热门阈值
```json
{
  "AI": 300,        // AI 类目热门阈值
  "tech": 400,      // 科技类
  "lifestyle": 800, // 生活类
  "default": 500    // 默认阈值
}
```

只有热度分数 ≥ 阈值的文章才会被标记为"热门"

---

## 🛠️ 安装与配置

### 1. 安装依赖
```bash
cd AIAgent
pip install schedule
```

### 2. 配置 RedNote MCP（推荐）

#### 方法 A：使用已安装的 RedNote MCP
```bash
# 验证已安装
which rednote-mcp

# 登录小红书（首次）
rednote-mcp init
```

#### 方法 B：使用 xiaohongshu-mcp (Docker)
```bash
cd /Users/voidzhang/Documents/workspace/xiaohongshu-mcp

# 启动 MCP Server
docker-compose up -d
```

### 3. 配置监控关键词
编辑 `1_热点监控/config.json`:
```json
{
  "keywords": [
    "AI", "ChatGPT", "AIGC", "人工智能"
  ],
  "fetch_time": "02:00",
  "max_notes_per_keyword": 20
}
```

---

## 🚀 使用方法

### 方式 1：立即执行一次（测试）
```bash
cd 1_热点监控

# 使用默认关键词
python scheduler.py --once

# 指定关键词
python scheduler.py --once --keywords "AI,ChatGPT,AIGC"

# 指定时间
python scheduler.py --once --time "03:00"
```

**输出示例**：
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

...

✓ 总计获取 52 条不重复的热门笔记

💾 保存到数据库...
✓ 已保存 15 条热点到数据库

✓ 报告已生成: reports/xiaohongshu/hot_2026-03-10.md

✅ 抓取完成 - 2026-03-10 02:05:32
```

### 方式 2：启动定时任务（生产环境）
```bash
cd 1_热点监控

# 后台运行（推荐使用 nohup 或 systemd）
nohup python scheduler.py > logs/hotspot.log 2>&1 &

# 或前台运行（测试）
python scheduler.py
```

**输出**：
```
================================================================================
🚀 启动定时任务调度器
================================================================================
⏰ 每天抓取时间: 02:00
📋 监控关键词: 8 个

按 Ctrl+C 停止...

🔄 启动时执行一次抓取...
[抓取过程...]
```

### 方式 3：集成到系统定时任务
```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天凌晨 2 点执行）
0 2 * * * cd /Users/voidzhang/Documents/workspace/AIAgent && /path/to/python 1_热点监控/scheduler.py --once
```

---

## 📊 查看抓取结果

### 1. 查看数据库
```python
from common.database import Database

db = Database()

# 查询热门文章
db.cursor.execute("""
    SELECT title, hot_score, likes, collects, url, publish_time
    FROM hotspots
    WHERE platform = 'xiaohongshu'
    ORDER BY hot_score DESC
    LIMIT 10
""")

for row in db.cursor.fetchall():
    print(f"标题: {row[0]}")
    print(f"热度: {row[1]:.2f} | 点赞: {row[2]} | 收藏: {row[3]}")
    print(f"链接: {row[4]}\n")
```

### 2. 查看每日报告
```bash
# 查看最新报告
cat reports/xiaohongshu/hot_$(date +%Y-%m-%d).md

# 或在 IDE 中打开
code reports/xiaohongshu/hot_2026-03-10.md
```

### 3. 导出数据
```python
import pandas as pd
from common.database import Database

db = Database()

# 导出为 CSV
db.cursor.execute("""
    SELECT * FROM hotspots 
    WHERE platform = 'xiaohongshu' 
    AND date(fetched_at) = date('now')
""")

df = pd.DataFrame(db.cursor.fetchall())
df.to_csv('xiaohongshu_hot_2026-03-10.csv', index=False)
```

---

## 🔧 高级配置

### 自定义热度阈值
```python
from 1_热点监控.fetchers.xiaohongshu_fetcher import XiaohongshuHotFetcher

fetcher = XiaohongshuHotFetcher()

# 修改阈值
fetcher.HOT_THRESHOLDS['AI'] = 500  # 提高AI类目阈值

# 修改权重
fetcher.WEIGHT_SHARES = 5.0  # 提高分享权重
```

### 添加通知功能
编辑 `1_热点监控/scheduler.py`:
```python
def _send_notification(self, notes: List[Dict]):
    """发送企业微信通知"""
    import requests
    
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    
    message = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"## 小红书热门日报\n\n"
                      f"**时间**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
                      f"**热门笔记**: {len(notes)} 条\n\n"
                      f"[查看详情](链接)"
        }
    }
    
    requests.post(webhook, json=message)
```

### 多账号管理
```python
# 使用不同的小红书账号抓取
fetcher = XiaohongshuHotFetcher()
fetcher.account = "myaccount"  # 指定账号
```

---

## 📈 数据分析示例

### 热度趋势分析
```python
import matplotlib.pyplot as plt
from common.database import Database

db = Database()

# 获取最近 7 天的热点数据
db.cursor.execute("""
    SELECT date(fetched_at), AVG(hot_score), COUNT(*)
    FROM hotspots
    WHERE platform = 'xiaohongshu'
    AND fetched_at >= date('now', '-7 days')
    GROUP BY date(fetched_at)
    ORDER BY date(fetched_at)
""")

data = db.cursor.fetchall()
dates = [row[0] for row in data]
scores = [row[1] for row in data]

plt.plot(dates, scores)
plt.xlabel('日期')
plt.ylabel('平均热度')
plt.title('小红书 AI 话题热度趋势')
plt.savefig('hot_trend.png')
```

### 关键词对比
```python
keywords = ['AI', 'ChatGPT', 'AIGC']

for keyword in keywords:
    db.cursor.execute("""
        SELECT AVG(hot_score)
        FROM hotspots
        WHERE keyword = ?
        AND fetched_at >= date('now', '-1 day')
    """, (keyword,))
    
    avg_score = db.cursor.fetchone()[0]
    print(f"{keyword}: 平均热度 {avg_score:.2f}")
```

---

## ⚠️ 注意事项

1. **MCP 登录状态**：确保 RedNote MCP 已登录小红书
   ```bash
   rednote-mcp init
   ```

2. **抓取频率**：建议每天 1 次，避免频繁请求

3. **数据去重**：系统自动基于笔记 ID 去重

4. **隐私合规**：仅用于数据分析，不用于商业用途

5. **日志监控**：
   ```bash
   # 查看日志
   tail -f logs/hotspot.log
   ```

---

## 🐛 常见问题

### 1. MCP 不可用
**问题**：提示 "❌ MCP 不可用"

**解决**：
```bash
# 检查 MCP 安装
which rednote-mcp

# 重新安装
npm install -g rednote-mcp

# 登录
rednote-mcp init
```

### 2. 抓取失败
**问题**：抓取超时或失败

**解决**：
- 检查网络连接
- 检查小红书账号状态
- 查看 MCP 日志
- 使用代理（如需要）

### 3. 热度分数异常
**问题**：热度分数过低或过高

**解决**：
- 调整热度阈值 (`config.json`)
- 检查数据完整性（是否有缺失字段）
- 自定义权重计算

---

## 📚 相关文档

- **热度定义**: `docs/xiaohongshu_hot_metrics.md`
- **MCP 文档**: `../skills/post-to-xhs/SKILL.md`
- **数据库设计**: `../common/database.py`

---

## 🚀 下一步

1. ✅ 启动定时任务
2. ✅ 监控抓取日志
3. ✅ 分析热度趋势
4. ✅ 优化关键词列表
5. ✅ 集成到完整工作流（模块 1-7）
