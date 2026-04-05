# OpenClaw Agent 编排工具深度分析：一人一团队模式

> 基于 gstack、edict、oh-my-claudecode、Claude Colony、Agentrooms、Agentwise 等主流方案，结合本地知识库和个人场景的综合分析

---

## 一、你的场景画像

根据你的 `总思路.md` 和知识库：

| 维度 | 你的情况 |
|------|---------|
| **本地主机** | 编写代码，CodeBuddy，公司 Token |
| **服务器** | OpenClaw，Linux，用来部署网站 |
| **目标** | 一人一团队，小步迭代，多产品验证 |
| **产品类型** | Web 应用、小红书运营、宠物 MBTI 等 |
| **成本偏好** | 低成本、用公司资源 + 自有服务器 |
| **工作模式** | 本地开发 → 服务器部署，双环境协作 |

**核心约束**：你有两个执行环境（本地 Mac + 远程 Linux），OpenClaw 部署在服务器上作为网关，需要一套编排方案让这两个环境协同工作。

---

## 二、主流 Agent 编排工具全景对比

### 2.1 对比总览

| 工具 | Stars | 定位 | 核心模式 | 环境要求 | 适合你的程度 |
|------|-------|------|---------|---------|------------|
| **gstack** | 60k | Markdown 技能包 | 角色化 Skill + Slash 命令 | Claude Code | ⭐⭐⭐⭐⭐ |
| **edict（三省六部）** | ~1k | 多 Agent 协作框架 | 12 角色分权制衡 + 可视化看板 | Docker/Python | ⭐⭐⭐⭐ |
| **oh-my-claudecode** | 19.8k | 零配置多 Agent 编排 | Team 模式 + 三模型混合 | Claude Code + tmux | ⭐⭐⭐⭐ |
| **Claude Colony** | ~12 | tmux 多 Agent 编排 | 预设团队 + 文件通信 | Claude Code + tmux | ⭐⭐⭐ |
| **Agentrooms** | 300+ | 多 Agent 工作区 | @mention 路由 + 本地远程混合 | Deno + Claude Code | ⭐⭐⭐⭐ |
| **Agentwise** | ~1k | 全栈开发平台 | 8+ 专业代理 + MCP 集成 | Claude Code | ⭐⭐⭐ |
| **OpenClaw 原生** | — | AI 执行网关 | 聊天入口 → Agent 执行 | Docker/Linux | ⭐⭐⭐⭐⭐ |

### 2.2 各工具深度分析

---

### ① gstack — Markdown 操作系统（已深度分析）

**你已有的认知**：在 `gstack-深度分析文档.md` 和 `IMA研发流程AI辅助方案.md` 中已经深度分析。

**对你的价值**：
- ✅ 角色化 Skill 的思想可以直接迁移到 CodeBuddy Rules
- ✅ 非交互式哲学、Fix-First 模式、反谄媚规则通用可用
- ✅ `/ship`、`/review`、`/careful` 等安全护栏你已经在用了
- ⚠️ gstack 原生依赖 Claude Code CLI，CodeBuddy 需要适配
- ⚠️ 它是"技能包"不是"编排器"，不能自动调度多个 Agent

**结论**：**方法论层面必学**，但不是编排方案本身。你需要的是在 gstack 思想之上叠加一个编排层。

---

### ② edict（三省六部）— 制度化 Agent 管理

**核心亮点**：
```
用户(皇上) → 太子(分拣) → 中书省(规划) → 门下省(审核) → 尚书省(派发) → 六部(执行)
```

- 12 个 Agent 角色，严格权限矩阵
- 门下省封驳机制 = 内置 QA 关卡
- 军机处实时看板 = 可视化 Kanban
- 奏折归档 = 全流程审计追溯
- Token 统计 = 成本可控
- 支持飞书、Telegram 下旨

**技术栈**：Python + React + Docker

**对你的场景适配度**：
- ✅ **Docker 部署**，可以直接跑在你的 Linux 服务器上
- ✅ **可视化看板**，一个人管理多个 Agent 需要看到全局
- ✅ **审核机制**，门下省封驳 = 自动 QA，减少人工审查
- ✅ **全流程审计**，适合同时跑多个产品时追溯问题
- ✅ **Telegram 集成**，可以手机下旨控制 Agent
- ⚠️ 项目相对较新（111 commits），生态不如 gstack 成熟
- ⚠️ 需要自己配置 LLM 模型接入

**最适合的场景**：你需要**制度化管理**多个产品的开发流程，每个产品有规划→审核→执行→回奏的完整闭环。

---

### ③ oh-my-claudecode（OMC）— 零配置多 Agent 编排

**核心亮点**：
- 32 个专业 Agent（架构、研究、设计、测试、数据科学等）
- Team 模式：plan → prd → exec → verify → fix 流水线
- 三模型混合：Codex(架构) + Gemini(UI) + Claude(综合)
- 智能模型路由：简单任务用 Haiku，复杂用 Opus，省 30-50% Token
- 自动提取调试模式为可复用技能
- 支持 OpenClaw 集成（事件转发）

**对你的场景适配度**：
- ✅ **零配置**，开箱即用，适合快速上手
- ✅ **OpenClaw 集成**，可以将会话事件转发到 OpenClaw
- ✅ **成本优化**，智能模型路由省 Token
- ✅ **多模式**，Team/Autopilot/Ultrawork 按需切换
- ⚠️ 依赖 Claude Code CLI（你本地用的是 CodeBuddy）
- ⚠️ 需要 Claude Max/Pro 订阅或 API key
- ⚠️ 运行在本地，不是服务器端方案

**最适合的场景**：如果你有 Claude Code CLI 访问权限，这是**最省心的本地编排方案**。

---

### ④ Claude Colony — tmux 可视化团队

**核心亮点**：
- 每个 Agent 是完整的 Claude Code 实例
- tmux 分屏实时监控每个 Agent 的工作
- 预设团队：fullstack / frontend / api / mobile / docs
- 基于文件的 @mention 通信协议
- 共享 Scratchpad 协作

**对你的场景适配度**：
- ✅ **可视化**，tmux 看到所有 Agent 的实时工作
- ✅ **预设团队**，fullstack 团队直接用
- ⚠️ 项目很新（12 stars），不够成熟
- ⚠️ Token 消耗快（每个都是完整 Claude Code 实例）
- ⚠️ 需要 Claude Max 计划

**最适合的场景**：需要同时看到多个 Agent 并行工作、实时干预的场景。

---

### ⑤ Agentrooms — 本地+远程混合编排

**核心亮点**：
- @mention 路由：`@api-agent` 直接指派任务
- 支持**本地 Agent + 远程 Agent 混合**
- Web UI 动态添加/删除 Agent
- 内置免费编排器
- 支持自定义 API 端点

**对你的场景适配度**：
- ✅ **本地+远程混合**，完美匹配你的双环境（Mac + Linux）
- ✅ **Web UI 管理**，不需要 tmux
- ✅ **自定义端点**，可以集成 OpenClaw
- ✅ 支持私有化部署
- ⚠️ 项目较新，社区还在成长
- ⚠️ 依赖 Deno 运行时

**最适合的场景**：你需要在**本地 Mac 和远程 Linux 服务器之间**协调多个 Agent 工作。

---

### ⑥ OpenClaw 原生 — 你已经有的基础设施

**核心定位**：AI 执行网关，连接聊天入口（Telegram/WhatsApp/Discord）到 AI Agent

**OpenClaw 作为编排层的能力**：
- 读取业务上下文（Obsidian 笔记、会议记录）
- 根据任务类型选择最合适的执行 Agent
- 监控 Agent 进度，失败后动态重写 Prompt
- 完成通知（Telegram 等）
- 主动任务发现（扫描 Sentry、Git log）

**一人团队的经典架构**（来自 Elvis 的案例）：
```
你（用户）
  ↓ 下旨（通过 Telegram/Web）
OpenClaw（编排层）
  ├── 读取 Obsidian 笔记获取业务上下文
  ├── 拆解任务
  ├── 分配 Agent
  │   ├── Claude Code → 前端工作
  │   ├── Codex → 后端复杂逻辑
  │   └── Gemini → 设计/安全审查
  ├── 监控进度（cron 每 10 分钟）
  ├── 自动 Code Review（多模型交叉审查）
  ├── CI 自动测试
  └── Telegram 通知你审查合并
```

**成本参考**：每月约 $190（Claude $100 + Codex $90），起步只需 $20

---

## 三、推荐方案：适合你的分层架构

### 3.1 推荐的「三层编排架构」

```
┌─────────────────────────────────────────────────────────────────┐
│                     第一层：你（决策者）                          │
│  通过 Telegram / Web / CodeBuddy 下达指令                        │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│               第二层：OpenClaw（编排网关）                        │
│  部署在 Linux 服务器上，24/7 运行                                │
│                                                                  │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐     │
│  │ 任务拆解 │  │ Agent 调度│  │ 进度监控  │  │ 结果汇总通知  │     │
│  └─────────┘  └──────────┘  └──────────┘  └──────────────┘     │
│                                                                  │
│  ┌─── edict（三省六部）可选叠加 ──────────────────────────────┐  │
│  │  中书省(规划) → 门下省(审核) → 尚书省(派发) → 六部(执行)   │  │
│  │  + 军机处看板 + 奏折归档 + Token 统计                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│               第三层：执行 Agents（干活的）                       │
│                                                                  │
│  ┌─── 本地 Mac（CodeBuddy）──┐  ┌─── Linux 服务器 ────────┐    │
│  │ • 复杂编码（gstack Skills）│  │ • 网站部署              │    │
│  │ • 代码审查                 │  │ • CI/CD 运行            │    │
│  │ • 设计/调试                │  │ • 自动化任务执行         │    │
│  │ • 宠物文章创作             │  │ • 爬虫/数据采集          │    │
│  └───────────────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 分阶段实施路线

#### **Phase 1（立即可用）：gstack 思想 + OpenClaw 原生**

你已经做了大量 gstack 分析工作，直接应用：

```
当前状态：
✅ CodeBuddy Rules 已有 gstack 风格的 /careful、/freeze、/guard、/retro、/ship
✅ OpenClaw 已部署在 Linux 服务器上
✅ 小红书自动化、宠物写作 Skill 已就绪

立即行动：
1. 在 OpenClaw 上配置 Telegram 入口 → 手机随时下旨
2. 用 OpenClaw 的 cron 跑「主动任务」：
   - 每早扫描 GitHub Issues
   - 每晚扫描 Git log 更新文档
3. 把 gstack 的核心 Skills 适配为 OpenClaw 的 Prompt 模板
```

#### **Phase 2（1-2 周内）：叠加 edict 做制度化管理**

```
行动：
1. Docker 部署 edict 到 Linux 服务器
2. 配置 edict 的 LLM 接入（用你公司的模型资源）
3. 设计你的「朝廷」：
   - 太子 → 消息分拣（区分产品 A/B/C 的任务）
   - 中书省 → 任务规划和拆解
   - 门下省 → 自动 QA 审核
   - 工部 → 代码编写
   - 礼部 → 文档/小红书内容
   - 户部 → 数据分析
4. 用军机处看板监控所有产品的进度
```

#### **Phase 3（按需扩展）：多 Agent 并行执行**

```
如果你获得了 Claude Code CLI 访问权限：
→ 叠加 oh-my-claudecode 的 Team 模式做并行执行
→ 或用 Agentrooms 做本地+远程混合编排

如果继续用 CodeBuddy：
→ 用 CodeBuddy 的 Agent Teams 功能（已内置）
→ gstack Skills 通过 Rules 驱动
→ OpenClaw + edict 在服务器端编排
```

---

## 四、各方案的适配打分

| 评估维度 | gstack | edict | OMC | Colony | Agentrooms | OpenClaw原生 |
|---------|--------|-------|-----|--------|-----------|-------------|
| **与 CodeBuddy 兼容** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Linux 服务器部署** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **低成本** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **多产品管理** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **可视化监控** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **学习曲线** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **社区成熟度** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **一人团队适配** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 五、终极推荐

### 最佳组合：**OpenClaw（网关）+ edict（管理）+ gstack（方法论）**

```
为什么这个组合最适合你：

1. OpenClaw = 你的 7×24 执行网关
   - 已部署、已熟悉、零额外成本
   - Telegram 入口让你随时随地下旨
   - 自动监控和通知

2. edict = 你的制度化管理层
   - Docker 一键部署到同一台 Linux 服务器
   - 可视化看板让一个人管理多个产品
   - 门下省审核机制保证质量
   - 全流程审计追溯
   - 用你公司的模型资源，零额外 API 成本

3. gstack = 你的思想武器
   - 角色化 Skill 编写方法论（已掌握）
   - 非交互式哲学、Fix-First、反谄媚（已内化）
   - 通过 CodeBuddy Rules 实现（已在用）

三者关系：
gstack 教你「怎么写好 Prompt/Skill」
edict 帮你「制度化管理多个 Agent」
OpenClaw 帮你「7×24 执行和通知」
```

### 备选加分项

| 如果... | 则加入... |
|--------|---------|
| 你获得 Claude Code CLI | oh-my-claudecode（零配置多 Agent） |
| 需要本地+远程混合编排 | Agentrooms（Web UI 管理） |
| 需要极致并行 | Claude Colony（tmux 可视化） |

---

## 六、相关资源链接

| 工具 | GitHub | 文档 |
|------|--------|------|
| gstack | https://github.com/garrytan/gstack | 仓库内 SKILL.md |
| edict | https://github.com/cft0808/edict | 仓库 README |
| oh-my-claudecode | https://github.com/Yeachan-Heo/oh-my-claudecode | https://ohmyclaudecode.com/ |
| Claude Colony | https://github.com/MakingJamie/claude-colony | 仓库 README |
| Agentrooms | https://github.com/baryhuang/claude-code-by-agents | https://claudecode.run/ |
| Agentwise | https://github.com/zanebarker-ops/cc-agentwise-orchestrator | https://vibecodingwithphil.github.io/agentwise/ |
| OpenClaw | https://github.com/openclaw | https://docs.openclaw.ai/ |

---

*分析基于 2026-04-01 的最新数据，结合本地知识库 gstack 深度分析、IMA 研发流程 AI 辅助方案*
