# gstack 深度分析文档：AI 工程团队的 Markdown 操作系统

> 分析基于 gstack 仓库所有核心文件的深度阅读，包括 11 个 SKILL.md.tmpl 模板、架构文档、哲学文档、开发指南和生成器脚本。

---

## 一、工程概述

### 1.1 gstack 是什么？

gstack 是 Y Combinator CEO **Garry Tan** 开源的 **AI 工程工作流技能包**（AI Engineering Workflow Skills）。它的核心理念是：

> **用 Markdown 文件将 AI 编码助手（Claude Code）变成一支完整的虚拟工程团队。**

每个 `.md` 文件定义一个专业角色——CEO 审查员、工程经理、产品设计师、QA 工程师、安全官、发布工程师、调试专家等。这些角色不是简单的提示词，而是包含完整工作流程、判断标准、交互规范和输出格式的**技能协议（Skill Protocol）**。

### 1.2 核心数据

| 维度 | 数据 |
|------|------|
| 技能数量 | **28 个**专业角色 |
| 覆盖范围 | 产品构思 → 设计 → 开发 → 审查 → 测试 → 发布 → 部署 → 监控 → 回顾 |
| 驱动方式 | 纯 Markdown + YAML frontmatter |
| 生成系统 | `.tmpl` 模板 + TypeScript 脚本自动生成 |
| 辅助工具 | 无头浏览器守护进程（Bun + Playwright） |
| 目标平台 | Claude Code / Codex（通过 `--host` 参数切换） |

### 1.3 技能全景图

```
┌─────────────────── 产品构思阶段 ───────────────────┐
│  /office-hours     YC 办公时间顾问，重构产品想法      │
│  /plan-ceo-review  CEO 级审查：找到 10 星产品        │
│  /autoplan         自动审查流水线（CEO→Design→Eng）   │
└──────────────────────────────────────────────────────┘

┌─────────────────── 设计阶段 ────────────────────────┐
│  /design-consultation  从零构建完整设计系统            │
│  /plan-design-review   设计维度 0-10 评分             │
│  /design-review        设计审计 + 修复循环             │
└──────────────────────────────────────────────────────┘

┌─────────────────── 开发阶段 ────────────────────────┐
│  /plan-eng-review  锁定架构、数据流、边界情况、测试     │
│  /investigate      系统化根因调试（Iron Law）          │
│  /cso              首席安全官审计（OWASP + STRIDE）    │
└──────────────────────────────────────────────────────┘

┌─────────────────── 质量阶段 ────────────────────────┐
│  /review           PR 预合并审查                      │
│  /qa               打开真实浏览器，发现 Bug 并修复     │
│  /qa-only          仅报告 Bug，不修改代码              │
│  /benchmark        性能回归检测                        │
│  /canary           部署后健康检查                      │
└──────────────────────────────────────────────────────┘

┌─────────────────── 发布阶段 ────────────────────────┐
│  /ship             测试→审查→推送→创建 PR（一条命令）  │
│  /land-and-deploy  合并 PR→等待部署→验证生产环境       │
│  /document-release 更新所有文档匹配已发布内容          │
└──────────────────────────────────────────────────────┘

┌─────────────────── 安全与治理 ──────────────────────┐
│  /careful          危险命令前警告                      │
│  /freeze           锁定目录禁止编辑                    │
│  /guard            同时激活 careful + freeze           │
│  /unfreeze         解除目录限制                        │
└──────────────────────────────────────────────────────┘

┌─────────────────── 运营与回顾 ──────────────────────┐
│  /retro            周回顾：per-person 分析 + 发布趋势  │
│  /browse           无头浏览器操作                      │
│  /setup-browser-cookies  导入真实浏览器 Cookie         │
└──────────────────────────────────────────────────────┘
```

---

## 二、核心设计思想

### 2.1 Builder Ethos（建造者哲学）

gstack 在 `ETHOS.md` 中定义了整个系统的灵魂，两大核心原则：

#### 原则一：Boil the Lake（烧干整个湖）

> "AI 使完整性的成本趋近于零。不做一半的事。"

传统开发中，由于人力成本，我们被迫做取舍——跳过文档、省略测试、简化设计。AI 改变了这个等式：

- 不是"够用就好"，而是"做完整的事"
- 写完代码后，同时更新文档、写测试、做性能基准
- 每个 PR 都经过 CEO 审查、工程审查、设计审查

这解释了为什么 gstack 有 28 个技能——因为它追求**全面性**，而 AI 的成本使全面性变得可行。

#### 原则二：Search Before Building（先搜索再建造）

gstack 定义了**三层知识体系**：

```
Layer 1 (Tried and True): 经典方法——被验证过的解决方案
Layer 2 (New and Popular): 当前趋势——社区最新实践
Layer 3 (First Principles): 第一性原理——为什么这样做？
```

每个技能在做决策前都必须经过三层搜索。如果 Layer 3 推理揭示了传统方法的缺陷，会触发 **"EUREKA moment"**（灵感时刻），这是唯一允许偏离传统的时机。

### 2.2 角色化 Prompt 工程

gstack 最核心的创新是**将 AI 从通用助手变为专业角色**。每个技能都有：

1. **明确的身份定义**（"你是一个 YC 办公时间合伙人"、"你是一个部署过千次的发布工程师"）
2. **行为准则**（反谄媚规则、什么时候该停下来问用户）
3. **认知模式**（CEO 有 18 种思维模式、工程经理有 15 种）
4. **分阶段工作流程**（每个阶段有明确的输入、处理逻辑、输出）
5. **完成标准**（什么算完成，什么算有风险地完成）

### 2.3 非交互式哲学

gstack 的一个关键设计原则是**最小化交互中断**：

```
当用户说 "/ship"，意思是"帮我做完"，而不是"每一步都问我"。

Never stop for（永远不要为这些事停下来）:
- 选择合并方式
- 提交消息措辞
- 超时警告

Always stop for（必须为这些事停下来）:
- 测试失败
- 安全问题
- 需要用户判断的决策
```

每个技能都有明确的 **"Never stop for"** 和 **"Always stop for"** 清单，这是用户体验设计的核心。

### 2.4 Fix-First Review（先修后问）

`/review` 技能展示了一个精妙的审查模式：

```
AUTO-FIX: 机械性问题直接修复（拼写、格式、导入顺序）
ASK:      需要判断的问题才询问用户（架构决策、行为变更）
```

AI 不会问"这里有个拼写错误，要不要修？"，而是直接修好。只有在需要人类判断时才中断。

### 2.5 反谄媚规则（Anti-Sycophancy）

gstack 明确禁止 AI 的讨好行为：

```
❌ 禁止说的话:
"Great question!"
"That's a really interesting approach!"
"I love this idea!"

✅ 替代表达:
"这里有一个问题…"
"让我推回一下…"
"有一个更简单的方式…"
```

这确保 AI 给出**真实、有用的反馈**，而不是让用户感觉良好但毫无价值的恭维。

---

## 三、SKILL.md 写法深度解构

### 3.1 文件结构总览

每个 SKILL.md 遵循严格的结构协议：

```markdown
---
# ① YAML Frontmatter（元数据）
name: skill-name
preamble-tier: 1-4        # 共享前置模块级别
version: 1.0.0
description: |
  多行描述：做什么、何时触发、关键词
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - WebSearch
---

# ② Preamble（共享前置模块，由模板自动注入）
{{PREAMBLE}}

# ③ 角色定义（1-3 段话）
你是一个 [角色名]，拥有 [核心能力]。你知道 [领域知识]。

# ④ 交互规范
**Only stop for:** [需要中断的情况]
**Never stop for:** [不需要中断的情况]
**NEVER do:** [绝对禁止的行为]

# ⑤ 分阶段工作流程
## Phase 0: Pre-checks（预检查）
## Phase 1: [第一阶段]
## Phase 2: [第二阶段]
...

# ⑥ 输出格式（ASCII 表格/结构化报告）

# ⑦ Important Rules（底线规则）
```

### 3.2 YAML Frontmatter 详解

```yaml
---
name: plan-ceo-review
preamble-tier: 3           # 值越高，前置模块包含的功能越多
version: 1.0.0
description: |
  CEO-level plan review. Finds the 10-star product hidden in the user's
  request. Use when: "review my plan", "is this a good idea",
  "scope check", "product direction".
allowed-tools:             # 权限白名单——限制 AI 能做什么
  - Bash                   # 运行命令
  - Read                   # 读文件
  - Write                  # 写文件
  - Edit                   # 编辑文件
  - Glob                   # 文件匹配
  - Grep                   # 搜索
  - AskUserQuestion        # 与用户交互
  - WebSearch              # 搜索互联网
---
```

**关键设计决策：**

- `allowed-tools` 是**安全边界**——QA 技能可以运行浏览器但不能写代码，审查技能可以读代码但有选择地写
- `preamble-tier` 控制共享前置模块的级别（1=最小，4=完整），避免不需要的功能占用上下文
- `description` 中包含**触发关键词**（"when: ..."），帮助调度器匹配用户意图

### 3.3 角色定义的写法模式

gstack 的角色定义不是简单的"你是 XXX"，而是包含**身份 + 能力 + 经验 + 态度**四个维度：

#### 模式 A：经验叙事型（最常用）

```markdown
# /land-and-deploy — Merge, Deploy, Verify

You are a **Release Engineer** who has deployed to production thousands of times.
You know the two worst feelings in software: the merge that breaks prod,
and the merge that sits in queue for 45 minutes while you stare at the screen.
Your job is to handle both gracefully — merge efficiently, wait intelligently,
verify thoroughly, and give the user a clear verdict.
```

**分析：** 不说"你是一个有经验的发布工程师"，而是用**具体场景**（"合并后打破生产环境"、"在合并队列前盯着屏幕 45 分钟"）让 AI 理解这个角色**真正关心什么**。

#### 模式 B：姿态定义型

```markdown
# /design-consultation

You are a senior product designer with strong opinions about typography, color,
and visual systems. You don't present menus — you listen, think, research,
and propose. You're opinionated but not dogmatic.

**Your posture:** Design consultant, not form wizard. You propose a complete
coherent system, explain why it works, and invite the user to adjust.
```

**分析：** 明确区分"是什么"和"不是什么"——"设计顾问，不是表单向导"。这防止 AI 退化为列出选项让用户选择的模式。

#### 模式 C：认知模式注入型（最复杂）

```markdown
# CEO Cognitive Modes (18 种思维模式)

| Mode | Description |
|------|-------------|
| dream-state-mapper | 找到用户没想到的梦想状态 |
| scope-expansion-detector | 检测范围膨胀的早期信号 |
| time-interrogator | 质疑时间估算（通常太乐观） |
| premise-challenger | 挑战基本前提假设 |
| ...（共 18 种） |
```

**分析：** 这是最高级的角色定义——不只是告诉 AI"你是 CEO"，而是把 CEO 的**思维方式**编码为可执行的模式。AI 在审查时会逐个应用这些思维模式。

### 3.4 工作流设计模式

#### 模式 1：线性阶段流（最常见）

```
Phase 0: Pre-checks（预检查）
  → 检查先决条件，如果不满足就 STOP
Phase 1: Gather（收集信息）
  → 读取代码、分析 diff、搜索上下文
Phase 2: Analyze（分析）
  → 应用认知模式、检测问题
Phase 3: Report（报告）
  → 输出结构化结果
Phase 4: Fix（修复，如果适用）
  → 自动修复或询问用户
```

**示例：** `/review`（PR 审查）

```
Phase 0: 检测 diff 范围和类型
Phase 1: 第一遍扫描——CRITICAL 级别问题
Phase 2: 第二遍扫描——INFORMATIONAL 级别问题
Phase 3: Fix-First 模式（AUTO-FIX 或 ASK）
Phase 4: 输出审查报告
```

#### 模式 2：循环修复流

```
Phase 1: Test（测试）
  → 发现 Bug
Phase 2: Triage（分类）
  → 按严重程度排序
Phase 3: Fix（修复）
  → 修复最高优先级 Bug
Phase 4: Verify（验证）
  → 回归测试
  → 如果还有 Bug → 回到 Phase 1
  → 如果全部通过 → Phase 5
Phase 5: Final Report
```

**示例：** `/qa`（QA 测试+修复）使用了**11 个阶段的循环流**，核心是"测试→分类→修复→回归测试"的循环，直到所有 Bug 修复。

#### 模式 3：流水线串联流

```
Stage 1: CEO Review → 输出分析
Stage 2: Design Review → 输入上一阶段输出
Stage 3: Eng Review → 输入前两阶段输出
Consensus: 合并三阶段结果 → 最终决策
```

**示例：** `/autoplan` 将三个审查技能串联为自动流水线，并使用**双重声音**（Claude 子代理 + Codex）进行独立评审。

#### 模式 4：条件深度流

```
Phase 5: Deploy strategy detection（部署策略检测）
  → 检测项目类型
  → if 只有文档变更 → 跳过验证
  → if 有前端变更 → 完整金丝雀检查
  → if 有后端变更 → 控制台 + 性能检查
  → if 有 GitHub Actions → 等待工作流
  → if 有 Vercel/Netlify → 等待 60 秒后直接检查
```

**示例：** `/land-and-deploy` 根据变更范围动态调整验证深度。

### 3.5 交互设计规范

gstack 为每个用户交互点定义了严格的 **AskUserQuestion 格式**：

```markdown
AskUserQuestion:
- **Re-ground:** 重新描述上下文（"我们正在审查 PR #123..."）
- **Context:** 当前发现（具体数据和证据）
- **RECOMMENDATION:** 明确推荐选项及理由
- A) [选项 A] (Completeness: 10/10)
- B) [选项 B] (Completeness: 7/10)
- C) [选项 C] (Completeness: 3/10)
```

**关键设计：**

- 每个选项都标注 **Completeness 分数**（完整性评分），让用户知道选择的代价
- 总是有明确的 **RECOMMENDATION**——AI 不会说"这取决于你"
- 总是包含"跳过/取消"选项——用户永远有退出的权利

### 3.6 输出格式规范

gstack 大量使用 **ASCII 结构化报告**，而非自由文本：

```
╔══════════════════════════════════════════════════════════╗
║              PRE-MERGE READINESS REPORT                  ║
╠══════════════════════════════════════════════════════════╣
║  PR: #NNN — title                                        ║
║  Branch: feature → main                                  ║
║                                                          ║
║  REVIEWS                                                 ║
║  ├─ Eng Review:    CURRENT / STALE (N commits) / —       ║
║  ├─ CEO Review:    CURRENT / — (optional)                ║
║  └─ Design Review: CURRENT / — (optional)                ║
║                                                          ║
║  TESTS                                                   ║
║  ├─ Free tests:    PASS / FAIL (blocker)                 ║
║  ├─ E2E tests:     52/52 pass (25 min ago) / NOT RUN     ║
║  └─ LLM evals:     PASS / NOT RUN                        ║
║                                                          ║
║  WARNINGS: N  |  BLOCKERS: N                             ║
╚══════════════════════════════════════════════════════════╝
```

**设计意图：** 结构化输出让用户在 3 秒内抓住关键信息，而不是阅读一大段文字。

### 3.7 完成状态协议（Completion Status Protocol）

每个技能结束时必须报告标准化状态：

```
DONE                 — 全部完成，无问题
DONE_WITH_CONCERNS   — 完成但有隐忧
BLOCKED              — 被阻塞，需要外部操作
NEEDS_CONTEXT        — 信息不足，需要更多上下文
```

这是技能间通信的基础——流水线中的下一个技能可以根据上一个技能的状态决定行为。

### 3.8 模板系统（SKILL.md.tmpl）

gstack 使用**模板 + 占位符**实现代码复用：

```markdown
# 模板文件 (.tmpl)
{{PREAMBLE}}           — 共享前置模块（更新检查、会话追踪、遥测）
{{BROWSE_SETUP}}       — 浏览器二进制文件查找和设置
{{BASE_BRANCH_DETECT}} — Git 基础分支检测
{{SLUG_EVAL}}          — 项目标识符计算
{{COMMAND_REFERENCE}}  — 从源代码自动提取的命令参考
{{SNAPSHOT_FLAGS}}     — 快照命令参数说明
{{DEPLOY_BOOTSTRAP}}   — 部署配置引导
```

**生成流程：**

```
.tmpl 模板文件 → gen-skill-docs.ts 脚本 → 最终 SKILL.md
                  ↑
              从源代码解析
              占位符内容
```

**最佳实践：** 编辑 `.tmpl` 模板，而非生成的 `.md` 文件。运行 `bun run gen:skill-docs` 重新生成。

---

## 四、可借鉴的 AI 团队构建方法论

### 4.1 角色设计清单

基于 gstack 的实践，创建一个 AI 角色需要回答以下问题：

```
□ 1. 这个角色是谁？
     - 专业身份（"你是一个高级产品设计师"）
     - 核心能力（"对字体和色彩有强烈观点"）
     - 经验叙事（"你已经部署了上千次"）
     - 性格姿态（"顾问型，不是表单向导"）

□ 2. 这个角色做什么？
     - 触发条件（什么时候调用这个角色？关键词列表）
     - 工作流程（分阶段，每个阶段有输入/处理/输出）
     - 输出格式（结构化报告、ASCII 表格、Markdown 文档）

□ 3. 这个角色不做什么？
     - Never stop for 列表
     - NEVER do 列表
     - 工具权限白名单（只能用哪些工具）

□ 4. 这个角色怎么和用户交互？
     - AskUserQuestion 格式规范
     - 选项必须有推荐和完整性评分
     - 反谄媚规则

□ 5. 这个角色怎么判断完成？
     - 完成状态（DONE / BLOCKED / NEEDS_CONTEXT）
     - 质量门（什么条件算通过？）

□ 6. 这个角色怎么和其他角色协作？
     - 输入：接收什么数据？
     - 输出：产生什么数据？
     - 升级：什么时候升级到其他角色？
```

### 4.2 建议的 AI 团队角色模板

以下是一个可直接使用的 SKILL.md 模板骨架：

```markdown
---
name: your-skill-name
version: 1.0.0
description: |
  一句话描述这个技能做什么。
  Use when: "关键词1", "关键词2", "关键词3".
allowed-tools:
  - [工具列表]
---

# /your-skill-name — 一句话标题

你是一个 **[角色名]**，[经验叙事——用具体场景描述这个角色理解什么]。
你的工作是 [核心职责]。

**你的姿态：** [是什么]，不是 [不是什么]。

---

## 交互规范

**Only stop for:**
- [需要用户判断的决策]
- [安全相关的问题]
- [权限不足]

**Never stop for:**
- [机械性操作]
- [明确有正确答案的问题]

**NEVER do:**
- [绝对禁止的行为]

---

## Phase 0: Pre-checks

[检查先决条件，不满足则 STOP]

---

## Phase 1: [收集/分析]

[第一阶段的工作内容]

---

## Phase 2: [执行/输出]

[第二阶段的工作内容]

### 输出格式

[定义结构化输出格式]

---

## Phase N: Report

[最终报告格式]

完成状态: DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT

---

## Important Rules

1. **[规则 1]** — [为什么]
2. **[规则 2]** — [为什么]
3. **[规则 3]** — [为什么]
```

### 4.3 推荐的 AI 团队组合

基于 gstack 的经验，一个最小可行的 AI 团队需要以下角色：

#### 核心团队（必备）

| 角色 | 对应 gstack 技能 | 核心价值 |
|------|------------------|----------|
| **产品顾问** | /office-hours | 在写代码前重构问题，挑战前提假设 |
| **代码审查员** | /review | 发现 CI 通过但生产环境会崩溃的 Bug |
| **QA 工程师** | /qa | 真实浏览器测试，发现→修复→验证循环 |
| **发布工程师** | /ship | 一条命令完成测试→审查→推送→创建 PR |

#### 扩展团队（推荐）

| 角色 | 对应 gstack 技能 | 核心价值 |
|------|------------------|----------|
| **架构审查员** | /plan-eng-review | 锁定架构和数据流 |
| **设计顾问** | /design-consultation | 构建完整设计系统 |
| **安全审计员** | /cso | OWASP + STRIDE 威胁建模 |
| **文档工程师** | /document-release | 确保文档和代码同步 |
| **调试专家** | /investigate | 系统化根因分析 |

### 4.4 gstack 的 10 个最佳实践（可直接借鉴）

1. **身份叙事优于指令列表** —— "你是一个部署过千次的发布工程师"比"你要执行以下步骤"更有效
2. **明确禁止清单** —— "NEVER do"比"请尽量避免"更可靠
3. **交互最小化** —— 默认自动执行，只在需要人类判断时中断
4. **结构化输出** —— ASCII 表格和固定格式报告，不要自由文本
5. **完成状态协议** —— 标准化的 DONE/BLOCKED 状态，支持技能间通信
6. **工具权限白名单** —— 明确每个角色能用什么工具
7. **认知模式注入** —— 不只定义角色，还定义角色的思维方式
8. **三层搜索原则** —— Layer 1 经典 → Layer 2 趋势 → Layer 3 第一性原理
9. **反谄媚规则** —— 禁止无价值的恭维，要求直接坦诚
10. **Fix-First 模式** —— 机械性问题直接修，需要判断的才问

### 4.5 在 CodeBuddy 中的应用建议

虽然 gstack 原生为 Claude Code 设计，但其核心思想完全可以迁移到 CodeBuddy：

1. **SKILL.md 可作为 CodeBuddy 的 Rules** —— 将角色定义和工作流程写入项目 Rules
2. **角色切换通过 prompt 触发** —— 在对话中说"现在以 QA 工程师的角色审查这段代码"
3. **模板系统可以简化** —— CodeBuddy 不需要 `.tmpl` 生成系统，直接维护 Markdown 规则文件
4. **认知模式表可以复用** —— CEO 的 18 种思维模式、工程经理的 15 种思维模式可直接借鉴
5. **交互规范可以嵌入** —— AskUserQuestion 的格式规范可以写入 Rules 中

---

## 五、总结：gstack 的本质

gstack 的本质不是"一堆提示词"，而是：

> **一个用 Markdown 编写的 AI 工程团队操作系统。**

它解决的核心问题是：**如何让 AI 从"聊天机器人"变成"专业工程师"？**

答案是：

- 给 AI **身份**（角色定义）—— 让它知道自己是谁
- 给 AI **知识**（认知模式）—— 让它知道怎么思考
- 给 AI **流程**（分阶段工作流）—— 让它知道做什么
- 给 AI **边界**（Never do + 工具白名单）—— 让它知道不能做什么
- 给 AI **标准**（完成状态 + 质量门）—— 让它知道什么算完成
- 给 AI **态度**（反谄媚 + 直接坦诚）—— 让它像专业人士一样沟通

这些原则是通用的，无论你用 Claude Code、CodeBuddy、还是其他 AI 编码工具，都可以借鉴。

---

## 六、产品构思阶段三个角色深度分析

### 6.1 角色总览

产品构思阶段是 gstack 工作流的**起点**，由三个角色组成：

```
/office-hours          /plan-ceo-review         /autoplan
  (发现问题)      →      (审查计划)           →   (全自动流水线)
  产出：设计文档          产出：完整审查报告         产出：三阶段审查 + 审批门
  
  ┌──────────┐     ┌────────────────┐     ┌───────────────────────┐
  │ 问对问题  │ ──→ │ 战略级审查     │ ──→ │ CEO→Design→Eng 全串联  │
  │ 写设计文档 │     │ 10个维度×4模式 │     │ 6原则自动决策          │
  │ 不写代码   │     │ 18种认知模式   │     │ 品味决策交给人类        │
  └──────────┘     └────────────────┘     └───────────────────────┘
```

### 6.2 `/office-hours` — YC 办公时间顾问

**角色定位：** YC（Y Combinator）办公时间合伙人

**核心任务：** 在写任何代码之前，确保问题被真正理解。产出设计文档，不是代码。

**工作流程：**

| 阶段 | 内容 |
|------|------|
| **Phase 1: 上下文收集** | 读取项目文件、git 历史、设计文档，通过关键问题判断用户目标类型 |
| **Phase 2A: Startup 模式** | 扮演严厉 YC 合伙人，通过 6 个逼问式问题诊断创业想法 |
| **Phase 2B: Builder 模式** | 扮演热情协作者，帮用户找到想法的最酷版本 |
| **Phase 2.75: 景观感知** | 搜索行业现有方案，三层知识体系分析 |
| **Phase 3: 前提挑战** | 在提出方案前，质疑核心假设 |
| **Phase 4: 替代方案** | 必须产出 2-3 个不同实现路径 |
| **Phase 5: 设计文档** | 输出完整设计文档 |
| **Phase 6: 交接** | 根据创始人信号强度，给出个性化反馈 |

**6 个逼问式问题：**

1. **需求真实性** — "你有什么最强证据证明有人真正需要这个？"
2. **现状分析** — "用户现在是怎么解决这个问题的？"
3. **绝望的具体性** — "说出最需要这个产品的那个人的名字、职位"
4. **最窄楔子** — "最小可付费版本是什么？"
5. **观察与意外** — "你看过用户不借助帮助使用产品吗？"
6. **未来适配性** — "3 年后世界变了，你的产品更重要还是更不重要？"

**按产品阶段智能路由：** 前产品→Q1,Q2,Q3 | 有用户→Q2,Q4,Q5 | 有付费客户→Q4,Q5,Q6

**核心原则：** 反谄媚（禁止说"好问题！"）、逼问到具体（"企业"不是客户，"Sarah 在 Acme 公司"才是）、一次只问一个问题。

---

### 6.3 `/plan-ceo-review` — CEO 级计划审查员

**角色定位：** 不是来盖橡皮章的，而是来把计划变成非凡的

**核心任务：** 接手 `/office-hours` 产出的设计文档，从 CEO/创始人的战略高度进行全面审查。

**工作流程：**

| 阶段 | 内容 |
|------|------|
| **预审系统审计** | 读取代码库历史、现有文档、设计文档和交接笔记 |
| **Step 0A: 前提挑战** | 是正确的问题吗？什么都不做会怎样？ |
| **Step 0B: 代码杠杆** | 哪些已有代码能复用？是否重复造轮子？ |
| **Step 0C: 梦想状态映射** | 当前状态 → 这个计划 → 12 个月后理想状态 |
| **Step 0C-bis: 替代方案** | 必须产出 2-3 个不同实现路径（强制） |
| **Step 0D: 模式特定分析** | 根据选中模式进行深度分析 |
| **Step 0E: 时间审讯** | 预判实现过程中每个小时会遇到什么决策 |
| **Step 0F: 模式选择** | 4 种审查模式 |
| **Section 1-11** | 架构、错误、安全、数据流、代码质量、测试、性能、可观测性、部署、长期轨迹、UI/UX |

**4 种审查模式：**

| 模式 | 范围 | 推荐姿态 | 默认适用 |
|------|------|---------|---------|
| **SCOPE EXPANSION** | 推高 | 热情推荐 | 全新功能 |
| **SELECTIVE EXPANSION** | 保持+展示机会 | 中性 | 功能增强 |
| **HOLD SCOPE** | 维持 | N/A | Bug修复、重构 |
| **SCOPE REDUCTION** | 推低 | N/A | 触及>15文件 |

**18 种 CEO 认知模式：** 包括分类本能（Bezos 单向门/双向门）、逆向思维（Munger）、聚焦即减法（Jobs 从 350 个产品砍到 10 个）、速度校准（70% 信息就够决策）等。

---

### 6.4 `/autoplan` — 自动审查流水线

**角色定位：** 全自动审查编排器——"一条命令进，完整审查出"

**核心任务：** 将三个审查技能（CEO → Design → Eng）按严格顺序自动执行，用 6 个决策原则代替人类判断。

**6 个自动决策原则：**

| # | 原则 | 含义 |
|---|------|------|
| 1 | **选择完整性** | 覆盖更多边界情况的方案优先 |
| 2 | **烧干湖水** | 爆炸半径内的所有问题一并修复 |
| 3 | **务实** | 两个方案效果一样，选更干净的 |
| 4 | **DRY** | 和现有功能重复？拒绝 |
| 5 | **显式优于聪明** | 10 行明显的代码 > 200 行抽象 |
| 6 | **倾向行动** | 合并 > 反复审查 > 停滞讨论 |

**决策分类：**
- **机械性决策** — 只有一个正确答案，静默自动处理
- **品味决策** — 合理的人会有分歧（接近的方案、边界范围、模型分歧），记录下来最后交给用户

**唯一的人类关口：** Phase 1 中的前提确认是整个流程中唯一不自动决策的问题。

---

### 6.5 三个角色的协作关系总结

- `/office-hours` 是**发现者** — "我们到底在解决什么问题？"
- `/plan-ceo-review` 是**审查者** — "这个计划够好吗？怎么让它变非凡？"
- `/autoplan` 是**编排器** — "让机器跑完全部审查，只把真正需要人类判断的留给你"

---

## 七、在 CodeBuddy 中使用产品构思阶段技能

### 7.1 适配方案概述

gstack 原生为 Claude Code 设计，使用 `SKILL.md` 文件作为技能协议。在 CodeBuddy 中，我们将这三个角色适配为 **CodeBuddy Rules**（规则），利用 CodeBuddy 的规则系统实现同样的效果。

**适配后的规则文件结构：**

```
.codebuddy/rules/
├── office-hours/
│   └── RULE.mdc          # YC 办公时间产品构思顾问
├── plan-ceo-review/
│   └── RULE.mdc          # CEO 级计划审查
└── autoplan/
    └── RULE.mdc          # 自动审查流水线
```

### 7.2 规则类型选择

三个规则均使用 **"智能体请求"（Agent Requested）** 类型：

| 规则 | 类型 | 原因 |
|------|------|------|
| office-hours | 智能体请求 | 当 Agent 根据描述判断用户在构思产品时自动触发 |
| plan-ceo-review | 智能体请求 | 当 Agent 判断用户想审查计划时自动触发 |
| autoplan | 智能体请求 | 当 Agent 判断用户想自动运行全部审查时自动触发 |

**为什么不用 "总是" 类型？** 产品构思技能不是每次对话都需要的（写代码、修 Bug 时不需要），使用"智能体请求"类型让 Agent 只在相关时才加载，避免上下文浪费。

**如何手动触发？** 在对话中使用 `@office-hours`、`@plan-ceo-review`、`@autoplan` 来手动调用。

### 7.3 适配中的关键调整

从 gstack 原版到 CodeBuddy 规则的适配做了以下调整：

| 原版功能 | CodeBuddy 适配 | 原因 |
|---------|---------------|------|
| `{{PREAMBLE}}` 模板占位符 | 直接内联所有内容 | CodeBuddy 不需要模板生成系统 |
| `~/.gstack/projects/` 存储路径 | `docs/designs/` 项目目录 | 放在项目内更适合版本控制和团队共享 |
| `allowed-tools` 工具白名单 | 移除 | CodeBuddy 的权限模型不同 |
| `SKILL.md.tmpl` → `SKILL.md` 生成 | 直接维护 `RULE.mdc` | 更简单直接 |
| Codex 双重声音系统 | 移除 | CodeBuddy 环境中不可用 |
| YC 推荐和 Garry Tan 个人信息 | 移除 | 这是 gstack 特有的营销内容 |
| `gstack-review-log` 命令 | 移除 | CodeBuddy 有自己的会话追踪 |
| `$B` 浏览器二进制调用 | 移除 | 产品构思阶段不需要浏览器 |

### 7.4 使用流程

#### 场景 1: 从零开始构思一个产品

```
用户: @office-hours 我有个想法，想做一个AI驱动的代码审查工具

→ AI 进入 /office-hours 模式
→ 判断 Startup 模式 or Builder 模式
→ 根据产品阶段智能选择问题
→ 逐个提问，追问到具体
→ 搜索行业景观
→ 挑战前提
→ 生成 2-3 个替代方案
→ 产出设计文档到 docs/designs/
→ 建议下一步: @plan-ceo-review 或 @plan-eng-review
```

#### 场景 2: 审查已有的计划文件

```
用户: @plan-ceo-review 帮我审查这个产品计划

→ AI 进入 CEO 审查模式
→ 系统审计（git 历史、TODO、现有设计文档）
→ 前提挑战 + 代码杠杆分析
→ 梦想状态映射
→ 替代方案生成
→ 模式选择（4 种模式）
→ 10 个审查 Section 逐一进行
→ 产出完整审查报告
```

#### 场景 3: 一键自动审查

```
用户: @autoplan 自动审查这个计划，帮我做决定

→ AI 进入自动审查模式
→ 保存恢复点
→ Phase 1: CEO 审查（前提需人工确认）
→ Phase 2: 设计审查（如果有 UI 范围）
→ Phase 3: 工程审查
→ 最终审批门（品味决策交给用户）
→ 所有机械性决策自动处理
```

### 7.5 进一步优化建议

1. **配合 CODEBUDDY.md 使用：** 在项目根目录放置 `CODEBUDDY.md`，描述项目背景、技术栈、团队约定，让产品构思规则有更好的上下文
2. **设计文档存储：** 建议在 `docs/designs/` 目录统一存放设计文档，便于版本控制和团队发现
3. **规则组合使用：** 可以将产品构思阶段的规则与设计阶段（`@plan-design-review`）、开发阶段（`@plan-eng-review`）的规则串联使用，形成完整的产品开发流水线
4. **团队共享：** `.codebuddy/rules/` 目录可以提交到 git，让整个团队共享这套产品构思工作流

---

*分析基于 gstack 仓库所有核心文件的深度阅读，包括 11 个 SKILL.md.tmpl 模板、架构文档、哲学文档、开发指南和生成器脚本。*
*生成日期：2026-03-24*
