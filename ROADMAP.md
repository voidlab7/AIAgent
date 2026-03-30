# 开发路线图

## 项目愿景
打造 **一个人的 AI 工作团队** —— 通过 AI 实现知识积累、内容生产、产品孵化、工程效率的全方位提升。一个人 + AI = 一个工作团队。

---

## Phase 1: 基础设施（已完成 ✅）

### 1.1 项目架构
- [x] 四大核心模块划分（knowledge / pipeline / products / common）
- [x] 内容流水线 7 阶段（pipeline/hotspot ~ pipeline/publisher）
- [x] AI 知识库模块（knowledge/articles、insights、playbooks）
- [x] 产品孵化模块（products/ideas、products/web_site）
- [x] 公共模块（config、database）
- [x] 工作流编排框架
- [x] Skill 开发规范

### 1.2 技术选型
- [x] Python + SQLite
- [x] APScheduler（定时任务）
- [x] MCP 集成（小红书、微信公众号）
- [x] AI API（OpenAI/Claude）

### 1.3 基础能力
- [x] 数据库模型设计（6 张表）
- [x] 统一配置管理
- [x] 主入口与 CLI

---

## Phase 1.5: AI 知识库（进行中 🚧）

### 知识库基础建设
**目标**：建立个人 AI 知识积累体系

**已完成**：
- [x] 目录结构搭建（articles / insights / playbooks）
- [x] `wechat-article-learner` Skill 实现
- [x] 行业洞察文档迁移（GStack 分析等）
- [x] 方法论文档迁移（经验文档等）

**待开发**：
- [ ] 知识检索与引用能力（跨文档搜索）
- [ ] 自动标签与分类系统
- [ ] 知识图谱可视化
- [ ] 定期知识回顾与整理 Skill

---

## Phase 2: 内容流水线开发（进行中 🚧）

### 2.1 pipeline/hotspot — 热点监控 (P0)
**目标**：每小时自动抓取各平台热搜，过滤相关热点

**任务清单**：
- [ ] 微博热搜抓取器 (`fetchers/weibo.py`)
- [ ] 知乎热榜抓取器 (`fetchers/zhihu.py`)
- [ ] 小红书热门抓取器（通过 RedNote MCP）
- [ ] AI 相关性分析 (`analyzer.py`)
- [ ] 热度趋势预测
- [ ] 定时调度（APScheduler）
- [ ] Skill 实现：`hotspot-tracker.md`

**预计时间**：3-5 天

---

### 2.2 pipeline/topic — 选题筛选 (P0)
**目标**：基于热点 AI 生成 3-5 个高质量选题

**任务清单**：
- [ ] 热点过滤器（匹配账号定位）
- [ ] 竞品分析器（搜索同类内容）
- [ ] AI 选题生成器（多角度切入）
- [ ] 选题打分排序
- [ ] Skill 实现：`topic-generator.md`

**预计时间**：2-3 天

---

### 2.3 pipeline/material — 素材采集 (P1)
**目标**：自动搜集并整理选题相关素材

**任务清单**：
- [ ] Google 搜索引擎（Serper API）
- [ ] 微信公众号搜索（复用 `ai_daily_fetcher`）
- [ ] 知乎/小红书内容抓取
- [ ] AI 智能摘要（提取观点/数据/案例）
- [ ] 素材去重与分类
- [ ] Skill 实现：`material-organizer.md`

**预计时间**：3-4 天

---

### 2.4 pipeline/writer — 内容创作 (P0)
**目标**：AI 辅助从提纲到成稿

**任务清单**：
- [ ] 提纲生成器（AI 生成结构）
- [ ] 段落扩写器（基于素材）
- [ ] 全文润色器（语言优化）
- [ ] 风格适配器（多平台）
- [ ] 原创检测（AI 自检）
- [ ] Skill 实现：`content-creator.md`

**预计时间**：4-5 天

---

### 2.5 pipeline/image — 配图查找 (P1)
**目标**：自动匹配文章配图

**任务清单**：
- [ ] Unsplash API 集成
- [ ] Pexels API 集成
- [ ] AI 语义匹配（关键词 → 图片）
- [ ] 图片下载与缓存
- [ ] 尺寸裁剪与压缩
- [ ] Skill 实现：`image-matcher.md`

**预计时间**：2 天

---

### 2.6 pipeline/formatter — 格式优化 (P1)
**目标**：多平台格式转换与美化

**任务清单**：
- [ ] Markdown → 微信 HTML 转换器
- [ ] 微信样式主题（代码高亮、引用块）
- [ ] 小红书纯文本 + 表情转换
- [ ] 知乎 Markdown 适配
- [ ] 一键复制功能
- [ ] Skill 实现：`format-adapter.md`

**预计时间**：3 天

---

### 2.7 pipeline/publisher — 内容发布 (P2)
**目标**：自动化发布到各平台

**任务清单**：
- [ ] 微信公众号发布（wechat-publisher-mcp）
- [ ] 小红书发布（扩展 RedNote MCP）
- [ ] 定时发布调度
- [ ] 发布状态追踪
- [ ] 数据抓取（阅读量、点赞）
- [ ] Skill 实现：`auto-publisher.md`

**预计时间**：3-4 天

---

## Phase 3: 工作流集成（2 周）

### 3.1 每日创作流
**任务清单**：
- [ ] 实现 `workflows/daily_creator.py`
- [ ] 串联 7 个模块
- [ ] 定时任务（每天 7:00 开始）
- [ ] 异常处理与通知

### 3.2 半自动辅助流
**任务清单**：
- [ ] 实现 `workflows/manual_helper.py`
- [ ] 交互式 CLI 界面
- [ ] 关键节点人工确认

### 3.3 爆款复制流
**任务清单**：
- [ ] 实现 `workflows/viral_replicate.py`
- [ ] 竞品 URL 解析
- [ ] 爆款因素分析
- [ ] 相似选题生成

---

## Phase 4: 优化与增强（持续）

### 4.1 性能优化
- [ ] 并发任务优化
- [ ] 数据库索引优化
- [ ] 本地缓存机制
- [ ] 减少 API 调用次数

### 4.2 平台扩展
- [ ] 抖音热榜
- [ ] 头条号发布
- [ ] B 站专栏
- [ ] Twitter/X

### 4.3 AI 能力增强
- [ ] 更精准的选题预测
- [ ] 更自然的写作风格
- [ ] 爆款标题生成器
- [ ] 评论区互动回复

### 4.4 数据分析
- [ ] 内容效果分析看板
- [ ] 最佳发布时间预测
- [ ] 用户画像分析
- [ ] 竞品对比报告

---

## Phase 5: 产品化（未来规划）

### 5.1 Web 界面
- [ ] Flask/FastAPI 后端
- [ ] React/Vue 前端
- [ ] 可视化工作流编辑器
- [ ] 实时预览

### 5.2 多账号管理
- [ ] 多账号配置
- [ ] 账号切换
- [ ] 批量发布

### 5.3 团队协作
- [ ] 用户权限管理
- [ ] 内容审核流程
- [ ] 评论与反馈

---

## 里程碑

| 里程碑 | 目标 | 预计完成时间 |
|---|---|---|
| **M1: MVP** | 完成模块 1-4，实现选题 → 写稿流程 | 2 周 |
| **M2: 完整链路** | 完成全部 7 个模块 | 4 周 |
| **M3: 自动化运行** | 实现每日自动创作工作流 | 5 周 |
| **M4: 多平台发布** | 支持 3+ 平台自动发布 | 6 周 |

---

## 当前进度
- ✅ Phase 1: 基础设施搭建完成
- 🚧 Phase 1.5: AI 知识库基础建设（已完成目录结构和文档迁移）
- 🚧 Phase 2: 内容流水线开发（0/7 完成）
- 📋 Phase 3-5: 待开始

**下一步行动**：
1. 完善知识库的检索与引用能力
2. 开发 pipeline/hotspot（热点监控），实现第一个完整的流水线模块
3. 填写 `.env` 文件，配置必要的 API Keys
4. 测试 RedNote MCP 和 wechat-publisher-mcp
