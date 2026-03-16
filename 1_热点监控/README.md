# 模块1：刷热搜 (Hotspot Monitor)

## 功能描述
实时抓取并分析各大平台的热搜榜单，为选题提供数据支撑。

## 数据源
- ✅ 小红书热门（通过 RedNote MCP）
- 🚧 微博热搜（待实现）
- 🚧 知乎热榜（待实现）
- 🚧 抖音热榜（待实现）
- 🚧 百度风云榜（待实现）

## 核心能力
1. **多源抓取**：支持 5+ 平台热搜数据
2. **热度计算**：自定义算法计算热度分数
3. **智能过滤**：基于关键词过滤相关热点
4. **数据存储**：热点数据持久化 + 历史趋势
5. **定时任务**：每天自动抓取

## 文件结构
```
1_热点监控/
├── fetchers/                   # 各平台抓取器
│   └── xiaohongshu_fetcher.py # 小红书抓取器 ✅
├── docs/                       # 文档
│   └── xiaohongshu_hot_metrics.md # 热度定义文档
├── scheduler.py                # 定时任务调度器 ✅
├── config.json                 # 配置文件 ✅
├── HOW_TO_USE.md              # 使用指南 ✅
├── quick_start.sh             # 快速启动脚本 ✅
├── __init__.py
└── README.md                   # 本文档
```

## 🚀 快速开始

### 方式 1：一键启动（推荐）
```bash
cd /Users/voidzhang/Documents/workspace/AIAgent/1_热点监控
./quick_start.sh
```

### 方式 2：立即执行一次
```bash
cd /Users/voidzhang/Documents/workspace/AIAgent

# 使用默认关键词
python 1_热点监控/scheduler.py --once

# 指定关键词
python 1_热点监控/scheduler.py --once --keywords "AI,ChatGPT,AIGC"
```

### 方式 3：启动定时任务
```bash
cd /Users/voidzhang/Documents/workspace/AIAgent

# 后台运行（每天凌晨 2 点抓取）
nohup python 1_热点监控/scheduler.py > logs/hotspot.log 2>&1 &

# 查看日志
tail -f logs/hotspot.log
```

## 📊 小红书"最热"定义

### 热度计算公式
```
热度分数 = (点赞×1.0 + 收藏×1.5 + 评论×2.0 + 分享×3.0) 
          / (发布时间小时数 + 1)^0.8
```

### 权重说明
- **分享 (×3.0)**：传播力，权重最高
- **评论 (×2.0)**：讨论热度
- **收藏 (×1.5)**：种草平台特征
- **点赞 (×1.0)**：基础认可度

### 热门阈值
- AI 类目：≥ 300
- 科技类：≥ 400
- 生活类：≥ 800
- 默认：≥ 500

详细说明：`docs/xiaohongshu_hot_metrics.md`

## 📋 配置文件

编辑 `config.json` 自定义配置：
```json
{
  "keywords": ["AI", "ChatGPT", "AIGC", "人工智能"],
  "fetch_time": "02:00",
  "max_notes_per_keyword": 20,
  "hot_threshold": {
    "AI": 300,
    "default": 500
  }
}
```

## 使用示例

### 示例 1：搜索单个关键词
```python
from 1_热点监控.fetchers.xiaohongshu_fetcher import XiaohongshuHotFetcher

fetcher = XiaohongshuHotFetcher()
notes = fetcher.fetch_by_keyword("AI", max_count=20)

for note in notes[:5]:
    print(f"{note['title']} - 热度: {note['hot_score']}")
```

### 示例 2：多关键词监控
```python
keywords = ["AI", "ChatGPT", "AIGC"]
notes = fetcher.fetch_multiple_keywords(keywords)

# 保存到数据库
fetcher.save_to_database(notes, "AI")
```

### 示例 3：查看抓取结果
```python
from common.database import Database

db = Database()
db.cursor.execute("""
    SELECT title, hot_score, likes, collects, url
    FROM hotspots
    WHERE platform = 'xiaohongshu'
    ORDER BY hot_score DESC
    LIMIT 10
""")

for row in db.cursor.fetchall():
    print(f"{row[0][:30]} - 热度: {row[1]:.2f}")
```

## Skill 规划
**Skill 名称**：`hotspot-tracker.md`（已创建）

**核心工作流**：
1. 定时触发（每 1 小时）
2. 并发抓取所有平台热搜
3. 数据清洗 + 去重
4. AI 分析热点相关性（基于账号定位）
5. 热度趋势预测
6. 存入数据库
7. 触发通知（有爆发潜力的热点）

## 数据表
使用 `common.database` 的 `hotspots` 表。

## 依赖
- ✅ schedule（定时任务）
- ✅ RedNote MCP (小红书)
- 🚧 requests（其他平台）
- 🚧 BeautifulSoup4（其他平台）

## 开发状态
- ✅ 小红书热门抓取
- ✅ 热度计算算法
- ✅ 定时任务调度
- ✅ 数据库存储
- ✅ 每日报告生成
- 🚧 微博热搜（待实现）
- 🚧 知乎热榜（待实现）

## 📚 详细文档
- **使用指南**: `HOW_TO_USE.md`
- **热度定义**: `docs/xiaohongshu_hot_metrics.md`
- **Skill 文档**: `../skills/hotspot-tracker.md`

## ⚠️ 注意事项
1. 确保 RedNote MCP 已登录小红书：`rednote-mcp init`
2. 建议每天抓取 1 次，避免频繁请求
3. 系统自动基于笔记 ID 去重
4. 仅用于数据分析，不用于商业用途
