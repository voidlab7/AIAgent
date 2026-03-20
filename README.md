# AI 自媒体创作助手

> 从热搜发现到内容发布的完整自动化工作流

## 项目架构

```
AIAgent/
├── 1_热点监控/      # 刷热搜 - 实时监控各平台热点
├── 2_选题筛选/       # 找选题 - 基于热点生成选题
├── 3_素材采集/   # 搜资料整理素材 - 多源内容聚合
├── 4_内容创作/       # 写稿 - AI 辅助内容创作
├── 5_配图查找/         # 找配图 - 自动匹配合适配图
├── 6_格式优化/            # 排版 - 多平台格式适配
├── 7_内容发布/            # 登后台发布 - 自动化发布
├── common/                 # 公共模块（数据库、配置、工具）
└── workflows/              # 完整工作流编排
```

## 模块说明

### 1. 刷热搜 (hotspot_monitor)
**功能**：实时抓取并分析各平台热搜榜单
- **数据源**：微博热搜、知乎热榜、小红书热门、抖音热榜、百度风云榜
- **输出**：热点关键词、热度值、趋势分析
- **Skill规划**：`hotspot-tracker.md` - 定时监控 + 热度预测

### 2. 找选题 (topic_selector)
**功能**：基于热点和账号定位生成选题
- **输入**：热搜数据 + 账号画像 + 历史数据
- **输出**：选题列表（标题、角度、预期流量）
- **Skill规划**：`topic-generator.md` - AI 辅助选题 + 竞品分析

### 3. 搜资料整理素材 (material_collector)
**功能**：根据选题搜集并整理素材
- **数据源**：搜索引擎、知识库、竞品内容、评论区
- **输出**：结构化素材库（观点、数据、案例、金句）
- **Skill规划**：`material-organizer.md` - 智能摘要 + 去重

### 4. 写稿 (content_writer)
**功能**：AI 辅助内容创作
- **模式**：提纲生成 → 段落扩写 → 全文润色
- **输出**：Markdown 初稿 + 多版本
- **Skill规划**：`content-creator.md` - 风格化写作 + SEO 优化

### 5. 找配图 (image_finder)
**功能**：自动匹配文章配图
- **来源**：无版权图库（Unsplash、Pexels）、AI 生成、素材库
- **输出**：配图 URL + 本地缓存
- **Skill规划**：`image-matcher.md` - 语义匹配 + 尺寸适配

### 6. 排版 (formatter)
**功能**：多平台格式转换和美化
- **支持**：微信公众号、小红书、知乎、头条号
- **输出**：平台专属 HTML/Markdown
- **Skill规划**：`format-adapter.md` - 样式预设 + 一键美化

### 7. 登后台发布 (publisher)
**功能**：自动化内容发布
- **平台**：微信公众号、小红书、知乎（通过 MCP）
- **模式**：定时发布、预览审核
- **Skill规划**：`auto-publisher.md` - 发布日历 + 效果追踪

## 快速开始

### 安装依赖
```bash
cd AIAgent
pip install -r requirements.txt
```

### 运行单个模块
```bash
# 示例：刷热搜
python -m 1_热点监控.main

# 示例：完整工作流
python -m workflows.daily_creator
```

### 配置
所有配置集中在 `common/config.py`，包括：
- API Keys
- 平台账号
- 内容偏好
- 发布计划

## 开发计划

| 模块 | 状态 | 优先级 |
|---|---|---|
| 刷热搜 | 🚧 开发中 | P0 |
| 找选题 | 📋 待开发 | P0 |
| 搜资料整理素材 | 📋 待开发 | P1 |
| 写稿 | 📋 待开发 | P0 |
| 找配图 | 📋 待开发 | P1 |
| 排版 | 📋 待开发 | P1 |
| 登后台发布 | 📋 待开发 | P2 |

## 技术栈

- **语言**：Python 3.9+
- **数据存储**：SQLite
- **任务调度**：APScheduler
- **AI 能力**：Claude/OpenAI API
- **MCP 集成**：小红书 MCP、微信公众号 MCP

## 已有基础

当前已有 `ai_daily_fetcher` 模块（微信公众号 + 小红书热文抓取），作为**刷热搜**和**搜资料**模块的基础实现。

## 🚀 版本发布与部署

项目提供完整的版本发布和部署自动化工具：

### 快速发版

```bash
# 一键发版（测试、打包、推送）
./release.sh 1.0.0 "feat: 新增趣味测试分析功能"

# GitHub Actions 自动构建 Release（约 2 分钟）
```

### 服务器部署

```bash
# 部署到服务器（OpenClaw）
./deploy.sh v1.0.0
```

### 测试工具

```bash
# 测试打包流程（不推送）
./test_build.sh 0.1.0-test

# 验证打包产物
./verify_release.sh aiagent-v0.1.0-test.tar.gz
```

**详细文档**：
- [完整工作流](./RELEASE_WORKFLOW.md) - 详细的发布和部署流程
- [使用指南](./RELEASE_GUIDE.md) - 快速参考和命令手册
- [Skill 文档](./.codebuddy/skills/aiagent-release-deploy.md) - CodeBuddy 集成
