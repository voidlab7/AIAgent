---
name: cb-skill-creator
description: >
  创建、修改和优化 CodeBuddy Skills。当用户想要从零创建 Skill、更新或优化现有 Skill、
  运行测试评估 Skill 效果、对比不同版本 Skill 的性能差异、或优化 Skill 的触发描述以提升
  触发准确率时使用此 Skill。即使用户只是提到"写个规则"、"做个工具"、"自动化流程"等，
  只要涉及可复用的 AI 指令模板，都应该考虑使用此 Skill。
---

# CodeBuddy Skill Creator

一个用于创建新 Skills 并迭代改进它们的 Skill。

## 总体流程

创建一个 Skill 的高层流程：

1. **明确意图** — 确定 Skill 要做什么，大致如何做
2. **编写草稿** — 撰写 Skill 的 `.md` 定义文件
3. **创建测试** — 编写 2-3 个测试 prompt 并运行
4. **评估结果** — 帮助用户定性和定量评估结果
   - 运行过程中，同步编写量化断言（如果还没有）
   - 使用 `eval-viewer/generate_review.py` 生成可视化审查页面
5. **改进迭代** — 基于用户反馈改写 Skill
6. **重复** — 直到满意为止
7. **扩展测试** — 增加测试用例数量，在更大规模上验证

你的任务是判断用户当前处于这个流程的哪个阶段，然后帮助他们推进。比如用户说"我想做一个 X 的 Skill"，你就帮他们细化需求、写草稿、编写测试用例、确定评估方式、运行所有 prompt，然后迭代。

如果用户已经有了 Skill 草稿，就直接进入 评估/迭代 环节。

当然，始终保持灵活。如果用户说"不需要跑一堆测试，直接跟我一起调就行"，那就按他们的方式来。

Skill 完成后，还可以运行描述优化器来改善 Skill 的触发准确率。

---

## 与用户的沟通

注意根据上下文线索判断用户的技术背景，调整沟通方式：

- "评估"和"基准测试"是可以的
- "JSON"和"断言"需要看到用户确实了解才能直接使用，否则简单解释
- 如果不确定，简短解释术语是可以的

---

## 创建 Skill

### 捕获意图

首先理解用户的意图。当前对话可能已经包含了用户想要固化的工作流（比如"把这个过程做成 Skill"）。如果是这样，先从对话历史中提取答案 — 使用了哪些工具、步骤序列、用户做了哪些修正、观察到的输入输出格式。用户可能需要补充信息，确认后再进入下一步。

1. 这个 Skill 要让 AI 能做什么？
2. 什么时候应该触发这个 Skill？（什么用户短语/上下文）
3. 期望的输出格式是什么？
4. 是否需要设置测试用例来验证？
   - 有客观可验证输出的 Skill（文件转换、数据提取、代码生成、固定工作流步骤）适合测试用例
   - 主观输出的 Skill（写作风格、设计）通常不需要
   - 根据 Skill 类型建议合适的默认值，但让用户决定

### 访谈和调研

主动询问边界情况、输入输出格式、示例文件、成功标准和依赖项。等到这些都明确了再编写测试 prompt。

检查可用的 MCP 工具 — 如果对调研有帮助（搜索文档、查找类似 Skill、查阅最佳实践），可以通过 Task 工具并行调研。尽量提前准备好上下文，减少用户的负担。

### 编写 Skill 文件

在本项目中，Skill 是 `skills/` 目录下的 `.md` 文件。基于用户访谈，填写以下组件：

#### Skill 文件结构

```
skills/
├── my-skill.md              # 简单 Skill（单文件）
├── analysis/                 # 按领域分组
│   ├── memory-analyze.md
│   └── extension-analyze.md
└── my-complex-skill/         # 复杂 Skill（带资源）
    ├── README.md             # Skill 定义
    ├── scripts/              # 可执行脚本
    ├── references/           # 参考文档
    └── assets/               # 模板、配置等资源
```

#### Skill 文件必需组件

每个 Skill `.md` 文件应包含：

1. **标题** — Skill 名称和简短描述
2. **触发条件** — 列出触发该 Skill 的关键词和场景（这是主要触发机制）
3. **使用方法** — CLI 命令或代码调用示例
4. **输入参数** — 参数表格（名称/类型/必填/说明）
5. **核心逻辑** — 分析规则、处理步骤、诊断方法等
6. **输出格式** — 期望的输出结构
7. **AI 分析提示** — 给 AI 的分析指引（可选但推荐）
8. **关联资源** — 相关代码目录、文档、配置（可选）

#### 触发条件编写指南

触发条件是 Skill 是否被使用的关键。要让触发条件稍微"积极"一些，避免欠触发：

```markdown
## 触发条件

当用户提到以下关键词时使用此 Skill：
- `内存分析` / `内存泄漏` / `OOM` / `memory`
- `内存占用` / `RSS增长` / `堆内存`
- 用户描述"应用越来越慢"或"内存越来越大"等症状时也应触发
```

#### 编写风格

- 使用祈使句
- 解释**为什么**某件事重要，而不是堆砌 MUST/NEVER
- 用类比和因果关系让模型理解意图
- 先写草稿，然后以全新的视角审视并改进
- 保持通用性，不要过度限定在特定示例上

### 测试用例

编写 Skill 草稿后，想出 2-3 个现实的测试 prompt — 真实用户会说的话。和用户分享："这里有几个测试用例，看看是否合适？需要添加更多吗？"然后运行它们。

将测试用例保存到 `evals/evals.json`。先不写断言 — 只写 prompt。断言在下一步运行时再起草。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的任务描述",
      "expected_output": "期望结果描述",
      "files": []
    }
  ]
}
```

完整 schema 参见 `references/schemas.md`。

---

## 运行和评估测试用例

本节是一个连续序列 — 不要中途停下。

将结果放在 `<skill-name>-workspace/` 中，作为 Skill 目录的兄弟目录。在工作区内按迭代组织结果（`iteration-1/`、`iteration-2/` 等），每个测试用例一个目录（`eval-0/`、`eval-1/` 等）。

### 步骤 1：启动所有运行（有 Skill 和基线对照）

对每个测试用例，在同一轮中启动两个运行 — 一个使用 Skill，一个不使用。同时启动，让所有运行大约同时完成。

**使用 Skill 的运行：**

通过 Task 工具启动子 agent：
```
执行此任务：
- Skill 路径：<path-to-skill>
- 任务：<eval prompt>
- 输入文件：<eval files if any, or "none">
- 保存输出到：<workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- 需要保存的输出：<用户关心的内容>
```

**基线运行（取决于场景）：**
- **创建新 Skill**：不使用任何 Skill，保存到 `without_skill/outputs/`
- **改进现有 Skill**：使用旧版本。编辑前先快照 Skill，然后将基线子 agent 指向快照。保存到 `old_skill/outputs/`

为每个测试用例编写 `eval_metadata.json`：

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "用户的任务描述",
  "assertions": []
}
```

### 步骤 2：运行期间起草断言

不要干等运行完成 — 利用这段时间起草量化断言。好的断言是客观可验证的，名称要描述清楚。

主观的 Skill（写作风格、设计质量）更适合定性评估 — 不要强行给需要人工判断的内容加断言。

更新 `eval_metadata.json` 和 `evals/evals.json` 中的断言。

### 步骤 3：运行完成后捕获时间数据

当每个 Task 子 agent 完成时，保存时间数据到 `timing.json`：

```json
{
  "total_duration_seconds": 23.3,
  "timestamp": "2026-01-15T10:30:00Z"
}
```

### 步骤 4：评分、聚合和启动查看器

所有运行完成后：

1. **评分** — 参照 `agents/grader.md` 评估每个断言。保存到 `grading.json`。
   grading.json 中的 expectations 数组必须使用 `text`、`passed`、`evidence` 字段。
   对于可编程检查的断言，编写并运行脚本。

2. **聚合基准** — 运行聚合脚本：
   ```bash
   python cb-skill-creator/scripts/aggregate_benchmark.py \
     <workspace>/iteration-N --skill-name <name>
   ```
   生成 `benchmark.json` 和 `benchmark.md`。

3. **分析** — 参照 `agents/analyzer.md` 分析模式和异常。

4. **启动查看器**：
   ```bash
   python cb-skill-creator/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json
   ```
   迭代 2+ 时，传 `--previous-workspace <workspace>/iteration-<N-1>`。

   如果无法打开浏览器，使用 `--static <output_path>` 生成静态 HTML 文件。

5. **告知用户** — "结果已经准备好了。有两个标签页 — 'Outputs' 可以逐个查看测试结果并留下反馈，'Benchmark' 显示量化对比。看完后告诉我。"

### 步骤 5：读取反馈

用户完成审查后，读取 `feedback.json`：

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "图表缺少坐标轴标签", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."}
  ],
  "status": "complete"
}
```

空反馈表示用户觉得没问题。聚焦于有具体反馈的测试用例。

---

## 改进 Skill

这是迭代循环的核心。你已经运行了测试用例，用户已经审查了结果，现在需要基于反馈改进 Skill。

### 改进思路

1. **从反馈中泛化** — Skill 是要被很多次使用的。不要为了让几个特定测试通过而做过度拟合的修改。如果有顽固的问题，尝试换一种方式表达，用不同的隐喻或推荐不同的工作模式。

2. **保持精简** — 删除没有作用的内容。阅读执行转录记录，如果 Skill 让模型浪费大量时间做无意义的事情，就去掉导致这种行为的部分。

3. **解释原因** — 尽量解释每件事的**为什么**。当今的 LLM 很聪明，理解因果关系后能做得更好。如果你发现自己在写大写的 ALWAYS 或 NEVER，那是一个提示 — 尝试重新表述，解释推理过程。

4. **发现重复劳动** — 阅读测试运行的转录记录，注意子 agent 是否都独立写了类似的辅助脚本。如果所有测试用例都导致 agent 写了类似的脚本，那是一个强信号：Skill 应该打包那个脚本。

### 迭代循环

改进 Skill 后：

1. 应用改进
2. 重新运行所有测试用例到新的 `iteration-<N+1>/` 目录
3. 启动带 `--previous-workspace` 的查看器
4. 等用户审查
5. 读取反馈，继续改进

持续直到：
- 用户满意
- 所有反馈都是空的
- 没有实质性进展

---

## 进阶：盲评对比

需要更严格比较两个版本时，可以使用盲评系统。参见 `agents/comparator.md` 和 `agents/analyzer.md`。

基本思路：将两个输出交给独立 agent，不告诉它哪个是哪个，让它判断质量。

这是可选的，需要 Task 子 agent，大多数用户不需要。

---

## 描述优化

触发条件/描述是决定 Skill 是否被正确使用的主要机制。创建或改进 Skill 后，可以提供描述优化。

### 步骤 1：生成触发评估查询

创建 20 个评估查询 — 混合应触发和不应触发的：

```json
[
  {"query": "用户的 prompt", "should_trigger": true},
  {"query": "另一个 prompt", "should_trigger": false}
]
```

查询必须是现实的，有具体细节的。不要抽象的请求，要具体的场景，包含文件路径、个人背景、具体数值等。

**应触发的查询**（8-10 个）：覆盖不同的表达方式 — 正式的、随意的。包含用户没有明确指名 Skill 但显然需要的情况。

**不应触发的查询**（8-10 个）：最有价值的是近似匹配 — 共享关键词但实际需要不同处理的查询。

### 步骤 2：与用户审查

使用 `assets/eval_review.html` 模板展示评估集，让用户编辑和确认。

### 步骤 3：运行优化循环

保存评估集后运行：

```bash
python cb-skill-creator/scripts/run_trigger_eval.py \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --max-iterations 5
```

### 步骤 4：应用结果

取最佳描述并更新 Skill 文件的触发条件部分。向用户展示前后对比。

---

## 参考文件

`agents/` 目录包含专门的子 agent 指令。需要时读取：

- `agents/grader.md` — 如何评估断言
- `agents/comparator.md` — 如何做盲评 A/B 对比
- `agents/analyzer.md` — 如何分析为什么一个版本比另一个好

`references/` 目录包含额外文档：
- `references/schemas.md` — evals.json、grading.json 等的 JSON 结构

---

核心循环总结：

1. 弄清 Skill 要做什么
2. 编写或修改 Skill
3. 在测试 prompt 上运行（使用/不使用 Skill）
4. 与用户一起评估输出
5. 基于反馈改进
6. 重复直到满意
7. 可选：优化触发描述
