# 单机 Agent 编排方案：一台电脑，四类工作

> 聚焦一台 Mac + CodeBuddy，不考虑多主机，把「写代码、做任务、做分析、做部署」四件事编排起来

---

## 一、你当前的单机能力盘点

### 已有的武器库

```
CodeBuddy IDE（主战场）
├── 23 个 Rules（gstack 风格角色）
│   ├── 产品构思：office-hours / plan-ceo-review / autoplan
│   ├── 设计：design-consultation / design-review / plan-design-review
│   ├── 开发：plan-eng-review / investigate / cso
│   ├── 质量：review / qa / qa-only / benchmark / canary
│   ├── 发布：ship / land-and-deploy / document-release / setup-deploy
│   └── 安全：careful / freeze / guard / unfreeze
│
├── 9 个 Skills（实操工具）
│   ├── 内容创作：pet-content-writer / wechat-article-learner
│   ├── 小红书：xiaohongshu-automation / trend-analyst
│   ├── 发布部署：pawmbti-release / scp-upload / aiagent-release-deploy
│   └── 开发工具：cb-skill-creator
│
├── MCP 工具（外部能力）
│   ├── devops-stream-pipeline（蓝盾流水线）
│   ├── playwright（浏览器自动化）
│   └── xiaohongshu（小红书操作）
│
└── 内置能力
    ├── Agent Teams（多 Agent 并行）
    ├── Automation（定时任务）
    ├── Task（子 Agent 派发）
    └── Web Search / Web Fetch（联网搜索）
```

### 关键发现：你不需要额外装任何编排工具

CodeBuddy **已经内置了编排能力**：
- **Task 工具** = 子 Agent 派发（code-explorer 等）
- **Agent Teams** = 多 Agent 并行协作（team_create / send_message）
- **Automation** = 定时/周期任务调度
- **Skills** = 专业角色按需加载
- **Rules** = 始终生效 / 智能触发的行为规范

**你缺的不是工具，是一套「编排协议」——告诉 CodeBuddy 什么时候用什么角色、怎么串联四类工作。**

---

## 二、单机编排架构

### 2.1 四类工作 × 角色映射

```
┌─────────────────────────────────────────────────────────────────┐
│                        你（一句话下旨）                           │
│  "帮我给 pawmbti 加个分享功能"                                   │
│  "分析下宠物 MBTI 这个品类的小红书数据"                           │
│  "把最新版本部署到服务器"                                        │
│  "每天早上 9 点自动发一篇宠物文章"                               │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CodeBuddy 编排中枢                             │
│                                                                  │
│  ┌─ 意图识别 ─────────────────────────────────────────────────┐ │
│  │ 关键词/上下文 → 自动匹配工作类型 → 调用对应角色              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  ┌─────────────┬──────────────┬──────────────┬──────────────┐   │
│  │  写代码      │  做任务       │  做分析       │  做部署      │   │
│  │  Coding     │  Task        │  Analysis    │  Deploy      │   │
│  ├─────────────┼──────────────┼──────────────┼──────────────┤   │
│  │ @plan-eng   │ @office-hours│ @trend-      │ @ship        │   │
│  │  -review    │ @autoplan    │  analyst     │ @pawmbti-    │   │
│  │ @implement  │ @pet-content │ @wechat-     │  release     │   │
│  │ @review     │  -writer     │  article-    │ @scp-upload  │   │
│  │ @investigate│ @xiaohongshu │  learner     │ @land-and-   │   │
│  │ @qa         │  -automation │ codebase_    │  deploy      │   │
│  │ @cso        │ Automation   │  search      │ @setup-deploy│   │
│  │             │  定时任务     │ web_search   │ 蓝盾流水线    │   │
│  └─────────────┴──────────────┴──────────────┴──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 每类工作的完整编排流程

---

### 🔧 类型一：写代码

**触发词**：加功能、修 Bug、重构、写测试、改样式...

**编排流程**：

```
Step 1: 需求理解
  ├── 简单需求 → 直接 @plan-eng-review 锁定方案
  └── 复杂需求 → @office-hours 产品构思 → @plan-ceo-review 审查

Step 2: 方案设计
  └── @plan-eng-review → 架构、数据流、边界情况、测试计划

Step 3: 编码实现
  ├── 用 Task(code-explorer) 先搜索相关代码
  ├── 读懂上下文后开始编码
  └── 遵循 @careful / @freeze 安全护栏

Step 4: 质量保证
  ├── @review → 自审（Fix-First 模式：机械问题直接修）
  ├── @qa → 如果有 UI，打开浏览器验证
  └── @cso → 安全敏感代码走安全审计

Step 5: 提交发布
  └── @ship → 测试 → 审查 → 推送 → 创建 PR
```

**实际操作示例**：

```
你: "给 pawmbti 的分享页面加上猫咪插画动画"

CodeBuddy 自动执行:
1. [plan-eng-review] 分析 CatIllustration.tsx 现有实现，输出方案
2. [编码] 修改组件，添加动画
3. [review] 自审代码质量
4. [ship] git add → commit → push → PR
```

---

### 📋 类型二：做任务

**触发词**：写文章、发小红书、每天自动执行、批量处理...

**编排流程**：

```
一次性任务:
  ├── 写宠物文章 → @pet-content-writer Skill
  ├── 发小红书 → @xiaohongshu-automation Skill
  ├── 总结公众号 → @wechat-article-learner Skill
  └── 批量操作 → 直接使用 MCP 工具

定时/周期任务（用 Automation）:
  ├── 每天早 9 点 → 自动写宠物文章
  ├── 每周一 → 工程回顾 @retro
  ├── 每天晚 10 点 → 小红书数据采集
  └── 自定义 cron → 任意定时任务
```

**实际操作示例**：

```
你: "每天早上 9 点帮我写一篇宠物文章并发到小红书"

CodeBuddy 执行:
1. [创建 Automation] 设置 FREQ=DAILY;BYHOUR=9;BYMINUTE=0
2. Automation 触发时自动执行:
   a. @pet-content-writer → 生成文章 + 标题 + 标签
   b. @xiaohongshu-automation → 发布到小红书
   c. 完成通知
```

---

### 📊 类型三：做分析

**触发词**：分析、调研、数据、趋势、竞品、选题...

**编排流程**：

```
代码分析:
  ├── codebase_search → 语义搜索代码库
  ├── Task(code-explorer) → 大范围代码探索
  └── @investigate → 系统化根因调试

市场/内容分析:
  ├── @trend-analyst → 小红书选题热度分析
  ├── web_search → 联网搜索最新信息
  └── web_fetch → 抓取特定页面深度分析

工程分析:
  ├── @retro → 每周工程回顾（git 历史 + 代码质量）
  ├── @benchmark → 性能回归检测
  └── @canary → 部署后健康检查
```

**实际操作示例**：

```
你: "分析下'猫咪性格测试'这个选题在小红书上的热度"

CodeBuddy 执行:
1. [trend-analyst] Skill 自动:
   a. 搜索小红书相关笔记 → 获取互动数据
   b. 分析热门标题模式
   c. 统计点赞/收藏/评论分布
   d. 输出选题分析报告 + 建议
```

---

### 🚀 类型四：做部署

**触发词**：部署、上线、发版、打包、上传服务器...

**编排流程**：

```
网站部署（pawmbti 等）:
  Step 1: @pawmbti-release → 打包构建 + 版本号
  Step 2: @scp-upload → SCP 上传到 microlab.top
  Step 3: 远程执行部署脚本

流水线触发（IMA 日常构建等）:
  Step 1: MCP devops-stream-pipeline → 触发蓝盾流水线
  Step 2: 查询构建状态
  Step 3: 通知结果

通用部署:
  Step 1: @setup-deploy → 检测部署配置
  Step 2: @ship → 测试 + 提交 + PR
  Step 3: @land-and-deploy → 合并 + 等待部署 + 验证
```

**实际操作示例**：

```
你: "把 pawmbti 最新版本部署到服务器"

CodeBuddy 执行:
1. [pawmbti-release] npm run build → 打包
2. [scp-upload] scp 到 microlab.top
3. 远程 nginx reload
4. 健康检查验证
```

---

## 三、核心编排模式

### 3.1 模式一：串行流水线（最常用）

```
需求 → 方案 → 编码 → 审查 → 测试 → 发布
  ↓       ↓       ↓       ↓       ↓       ↓
office  plan-   直接    review   qa     ship
-hours  eng-    编码
        review
```

**适用场景**：正常的功能开发、Bug 修复

### 3.2 模式二：并行任务（Team 模式）

```
                    ┌── Agent A: 前端编码
你: "全栈改造" ──→ ├── Agent B: 后端编码
                    └── Agent C: 写测试
                              ↓
                      汇总 → 集成测试 → ship
```

**适用场景**：大型功能需要拆分并行

**CodeBuddy 实现方式**：

```python
# 用 Agent Teams 内置能力
team_create("pawmbti-feature")

# 并行派发
Task(name="frontend", prompt="实现分享页面 UI...")
Task(name="backend", prompt="实现分享 API...")
Task(name="tester", prompt="写分享功能的测试...")

# Agent 间通信
send_message(type="message", recipient="frontend", content="API 接口已就绪...")
```

### 3.3 模式三：定时自动化（Automation）

```
┌── 每天 09:00 → 写宠物文章 + 发小红书
├── 每天 22:00 → 小红书数据采集
├── 每周一 09:00 → @retro 工程回顾
└── 每次 push → @review + @qa 自动审查
```

**CodeBuddy 实现方式**：

```
automation_update:
  mode: "suggested create"
  name: "daily-pet-article"
  prompt: "使用 pet-content-writer Skill 生成一篇宠物文章，然后使用 xiaohongshu-automation 发布"
  rrule: "FREQ=DAILY;BYHOUR=9;BYMINUTE=0"
  status: "ACTIVE"
```

### 3.4 模式四：事件驱动（响应式）

```
触发事件                         自动响应
────────                        ────────
说 "careful"          →         激活安全模式
说 "ship"            →         一键发布流程
说 "retro"           →         生成工程回顾
提到 "bug"            →         @investigate 根因分析
提到 "部署/发版"       →         @pawmbti-release 打包流程
提到 "选题分析"        →         @trend-analyst 热度报告
```

**已实现**：通过 Rules 的 description 关键词触发 + Skills 的触发词匹配。

---

## 四、实操：为你定制的「四象限」快捷入口

### 快速参考卡

| 我要... | 说什么 | CodeBuddy 做什么 |
|--------|--------|-----------------|
| **写代码** | "给 XX 加个 YY 功能" | plan-eng-review → 编码 → review → ship |
| **修 Bug** | "XX 页面 YY 不工作" | investigate → 编码 → review → ship |
| **写文章** | "写篇宠物文章" | pet-content-writer → 输出文章 |
| **发小红书** | "发到小红书" | xiaohongshu-automation → 发布 |
| **选题分析** | "分析 XX 选题热度" | trend-analyst → 输出报告 |
| **工程回顾** | "retro" | 分析 git 历史 → 输出回顾报告 |
| **部署网站** | "部署 pawmbti" | pawmbti-release → scp-upload → 验证 |
| **触发构建** | "启动 143 日常构建" | MCP 蓝盾流水线 → 查询状态 |
| **定时任务** | "每天 9 点写文章" | 创建 Automation |
| **并行开发** | "同时做前后端" | Agent Teams → 并行派发 |
| **安全模式** | "careful" | 激活破坏性命令警告 |
| **代码审查** | "review 下这个 PR" | review Rule → Fix-First 审查 |

---

## 五、进阶：构建你的「单机编排 Skill」

如果你想把上面的编排逻辑**固化为一个 Skill**，让一句话触发完整流水线：

### 5.1 示例：`/fullstack` 全流程 Skill

```markdown
触发: "fullstack"、"全流程开发"、"从需求到上线"

流程:
1. @office-hours → 理解需求，输出设计文档
2. @plan-eng-review → 锁定技术方案
3. 编码实现（可并行 Agent Teams）
4. @review → 自审
5. @qa → 浏览器测试（如有 UI）
6. @ship → 提交 + PR
7. @pawmbti-release / @scp-upload → 部署
8. @canary → 健康检查

每个阶段完成后报告状态:
DONE → 进入下一阶段
BLOCKED → 停下来问你
```

### 5.2 示例：`/daily-ops` 每日运营 Skill

```markdown
触发: "daily ops"、"今日运营"、"每日任务"

流程:
1. 检查 Git 状态 → 有未完成的 PR 吗？
2. @retro → 昨日工作回顾（简版）
3. @pet-content-writer → 生成今日宠物文章
4. @trend-analyst → 今日小红书热点
5. 汇总报告: 今日待办 + 建议优先级

输出格式:
┌─────────────── 今日运营报告 ───────────────┐
│ 📋 未完成 PR: 2 个                          │
│ 📝 今日文章: [标题] 已生成                   │
│ 📊 热点选题: [3 个推荐选题]                  │
│ 🎯 建议优先级:                              │
│   1. 合并 PR #xx                           │
│   2. 发布宠物文章                           │
│   3. 开发 XX 功能                           │
└────────────────────────────────────────────┘
```

---

## 六、总结：单机编排的核心原则

```
1. 不需要额外工具 — CodeBuddy 已内置 Task / Teams / Automation / Skills / Rules
2. 角色即编排 — 23 个 Rules + 9 个 Skills = 你的虚拟团队
3. 关键词触发 — 说对的话，自动匹配对的角色
4. 四类工作四条流水线 — 写代码/做任务/做分析/做部署各有固定路径
5. 串行为主、并行为辅 — 日常串行流水线，大功能用 Teams 并行
6. Automation 解放时间 — 重复任务全部定时化
7. 渐进增强 — 先把串行跑通，再逐步加并行和自动化
```

```
你的单机编排全景:

  你（一句话）
    │
    ├── 写代码 → plan-eng-review → 编码 → review → ship
    ├── 做任务 → pet-content-writer / xiaohongshu / Automation
    ├── 做分析 → trend-analyst / retro / investigate / web_search
    └── 做部署 → pawmbti-release → scp-upload → canary
```

---

*基于 CodeBuddy 现有能力和你的工具链分析*
*2026-04-01*
