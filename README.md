# AIAgent — 一个人的 AI 工作团队

> 一个人 + AI = 一个工作团队。知识积累、内容生产、产品孵化、工程效率的全方位 AI 工作站。

## 核心理念

- 🧠 **知识积累**：通过 AI 持续学习、总结、沉淀个人知识库
- 🏭 **内容生产**：AI 驱动的内容创作全流程自动化
- 🚀 **产品孵化**：快速验证产品创意，小步快跑，多路验证
- 🔧 **工程效率**：AI 辅助的开发、部署、运维自动化

## 项目架构

```
AIAgent/
│
├── knowledge/                   # 🧠 AI 知识库
│   ├── articles/                #   文章学习笔记（公众号、博客等）
│   ├── insights/                #   行业洞察与深度分析
│   └── playbooks/               #   方法论、经验手册
│
├── pipeline/                    # 🏭 内容创作流水线
│   ├── hotspot/                 #   1. 热点监控
│   ├── topic/                   #   2. 选题筛选
│   ├── material/                #   3. 素材采集
│   ├── writer/                  #   4. 内容创作
│   ├── image/                   #   5. 配图查找
│   ├── formatter/               #   6. 格式优化
│   └── publisher/               #   7. 内容发布
│
├── products/                    # 🚀 产品孵化
│   └── ideas/                   #   产品创意池（含设计文档）
│
├── web_site/                    # 🌐 Web 产品（独立 Git 仓库）
│   └── pawmbti/                 #   PawMBTI 宠物性格测试（已上线）
│
├── common/                      # 🔧 公共模块
│   ├── config.py                #   统一配置管理
│   └── database.py              #   SQLite 数据库封装
│
├── workflows/                   # 工作流编排
├── docs/                        # 📚 项目文档
│   ├── RELEASE.md               #   发版与部署指南
│   └── screenshots/             #   项目截图
├── .codebuddy/                  # AI 助手（Skills / Rules / Memory）
│
├── requirements.txt             # Python 依赖
└── .env.example                 # 环境变量模板
```

## 模块说明

### 🧠 [知识库](./knowledge/README.md)（knowledge/）

AI 学习助手产出的所有知识的统一存储。

| 子目录 | 定位 | 内容来源 |
|--------|------|----------|
| `articles/` | 文章学习笔记 | `@wechat-article-learner` skill 产出 |
| `insights/` | 行业洞察分析 | 深度分析报告、竞品研究、技术趋势 |
| `playbooks/` | 方法论与经验 | 实操经验、工作流程、思维模型 |

### 🏭 [内容流水线](./pipeline/README.md)（pipeline/）

从热点发现到内容发布的 7 步自动化管线。

| 模块 | 功能 | 状态 |
|------|------|------|
| hotspot | 实时抓取各平台热搜 | 🚧 开发中 |
| topic | 基于热点生成选题 | 🚧 开发中 |
| material | 多源素材采集整理 | 📋 待开发 |
| writer | AI 辅助内容创作 | 📋 待开发 |
| image | 自动匹配配图 | 📋 待开发 |
| formatter | 多平台格式适配 | 📋 待开发 |
| publisher | 自动化内容发布 | 🚧 开发中 |

### 🚀 [产品孵化](./products/README.md)（products/）

产品创意池 + 已上线的 Web 产品。

| 产品 | 状态 | 说明 |
|------|------|------|
| PawMBTI 宠物性格测试 | ✅ 已上线 | microlab.top，React + TypeScript |
| 天选城市测试 | ✅ 已上线 | 集成于 PawMBTI 站点 |
| 宝宝性格测试 | 🚧 开发中 | 设计文档完成，待实现 |
| 黑暗人格测试 | 🚧 开发中 | 设计文档完成，待实现 |

Web 产品代码在 `web_site/`（独立 Git 仓库），设计文档在 `products/ideas/`。

## 快速开始

### 安装 Python 依赖
```bash
cd AIAgent
pip install -r requirements.txt
cp .env.example .env  # 配置 API Keys
```

### 运行各模块
```bash
# 热点监控
python -m pipeline.hotspot.scheduler

# 选题分析（趣味测试方向）
python -m pipeline.topic.fun_test_workflow

# 内容发布（小红书）
python -m pipeline.publisher.main
```

### Web 产品（PawMBTI）
```bash
cd web_site/pawmbti
npm install
npm run dev    # 本地开发
npm run build  # 构建生产版本
```

### 发版与部署
参考 [docs/RELEASE.md](./docs/RELEASE.md)

### 配置
所有 Python 配置集中在 `common/config.py`，包括 API Keys、平台账号、内容偏好、发布计划。

## 技术栈

- **语言**：Python 3.9+
- **数据存储**：SQLite
- **任务调度**：APScheduler
- **AI 能力**：Claude / OpenAI API
- **MCP 集成**：小红书 MCP、微信公众号 MCP
- **AI 助手**：CodeBuddy（Skills + Rules + Memory）

## AI Skills

| Skill | 功能 |
|-------|------|
| `wechat-article-learner` | 公众号文章知识点总结学习 |
| `trend-analyst` | 热点趋势分析 |
| `xiaohongshu-automation` | 小红书自动化发布 |
| `pet-content-writer` | 宠物内容创作 |
| `cb-skill-creator` | Skill 创建工具 |
