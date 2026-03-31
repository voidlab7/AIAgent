# cb-skill-creator

基于 Anthropic Claude Code Skill Creator 定制的 **CodeBuddy 中文版 Skill 开发套件**。

专为 CodeBuddy 环境设计，提供完整的 Skill 创建、评估、迭代和优化流程，全中文指令，降低使用门槛。

## 核心优点

### 1. 全中文工作流

所有指令、提示、反馈模板均为中文，适合中文用户无障碍使用。无需在英文指令和中文需求之间来回切换。

### 2. 完整的评估框架

不只是"写个 Skill 就完事"，而是提供从创建到验证的闭环：

- **A/B 对比测试** — 同时运行"使用 Skill"和"不使用 Skill"两组测试，量化 Skill 的实际价值
- **量化断言系统** — 用客观可验证的断言评估输出质量，生成 pass_rate 指标
- **基准聚合** — `aggregate_benchmark.py` 自动生成 `benchmark.json` 和 `benchmark.md`
- **多轮迭代追踪** — 按 `iteration-1/`、`iteration-2/` 组织，支持跨迭代对比

### 3. 子 Agent 协作

内置三个专用子 Agent 指令文件：

| Agent | 文件 | 职责 |
|-------|------|------|
| Grader | `agents/grader.md` | 评估断言通过/失败，输出 `grading.json` |
| Comparator | `agents/comparator.md` | 盲评 A/B 对比，不告知版本身份 |
| Analyzer | `agents/analyzer.md` | 分析胜出/落败原因，输出改进建议 |

### 4. 触发描述优化

专用的 `run_trigger_eval.py` 脚本，自动评估和优化 Skill 的触发条件准确率，减少漏触发和误触发。

### 5. 贴合项目结构

Skill 直接放在项目的 `skills/` 目录下，支持按领域分组（如 `skills/analysis/`），与项目代码紧密集成。

## 目录结构

```
cb-skill-creator/
├── SKILL.md                          # 核心指令文件（中文）
├── agents/                           # 子 Agent 指令
│   ├── grader.md                     # 评分器
│   ├── comparator.md                 # 盲评比较器
│   └── analyzer.md                   # 分析器
├── scripts/                          # 工具脚本
│   ├── aggregate_benchmark.py        # 基准聚合
│   ├── run_trigger_eval.py           # 触发描述优化
│   ├── quick_validate.py             # 快速验证
│   └── utils.py                      # 公共工具
└── references/                       # 参考文档
    └── schemas.md                    # JSON 数据结构定义
```

## 与 CodeBuddy 内置 skill-creator 的区别

CodeBuddy 内置的 `skill-creator` 是一个**轻量级创建指南**，主要帮助你快速初始化和编写 Skill 文件。

| 维度 | CodeBuddy 内置 | cb-skill-creator |
|------|---------------|-----------------|
| **定位** | 快速创建 Skill | 创建 + 评估 + 迭代打磨 |
| **语言** | 英文 | 中文 |
| **评估框架** | 无 | A/B 对比 + 量化断言 + 基准聚合 |
| **子 Agent** | 无 | grader / comparator / analyzer |
| **触发优化** | 无 | `run_trigger_eval.py` 自动化优化 |
| **初始化工具** | `init_skill.py` 生成模板 | 手动编写，提供详细的结构和编写指南 |
| **打包** | `package_skill.py` → `.zip` | 无内置打包（可结合内置版使用） |
| **Skill 文件规范** | 标准 YAML frontmatter (name + description) | 扩展规范：触发条件、输入参数、AI 分析提示等 8 个组件 |

**简单说**：内置版解决"怎么写"，cb-skill-creator 解决"怎么写好"。

## 与 Anthropic 原版 skill-creator 的区别

Anthropic 原版是为 Claude Code 设计的英文全功能套件（即本项目 `skill-creator/` 目录）。cb-skill-creator 在其基础上做了中文化和适配裁剪。

| 维度 | Anthropic 原版 | cb-skill-creator |
|------|--------------|-----------------|
| **语言** | 英文 | 中文 |
| **目标平台** | Claude Code / Claude.ai / Cowork | CodeBuddy |
| **脚本数量** | 8 个 | 5 个 |
| **eval-viewer** | 有 (`generate_review.py` + `viewer.html`) | 引用但未包含（SKILL.md 中引用了 `eval-viewer/generate_review.py`） |
| **交互式审查** | `assets/eval_review.html` 模板 | 无 |
| **描述优化** | `run_loop.py` + `run_eval.py`（依赖 `claude -p` CLI） | `run_trigger_eval.py`（独立实现，不依赖 `claude` CLI） |
| **打包** | `package_skill.py` → `.skill` 文件 | 无 |
| **报告生成** | `generate_report.py` | 无 |
| **Skill 存放路径** | `.claude/skills/` | `skills/`（项目目录） |
| **Skill 文件规范** | 通用结构（name + description + body） | 扩展结构（增加触发条件、输入参数、AI 分析提示等） |

**简单说**：原版功能最全但依赖 Claude Code 生态，cb-skill-creator 做了 CodeBuddy 适配和中文本地化，但部分工具尚未迁移。

## 使用方式

### 创建新 Skill

```
@cb-skill-creator 我想创建一个分析内存泄漏日志的 Skill
```

### 评估现有 Skill

```
@cb-skill-creator 帮我评估 skills/analysis/extension-analyze.md 这个 Skill 的效果
```

### 优化触发描述

```
@cb-skill-creator 优化 extension-analyze 的触发条件，减少漏触发
```

## 核心工作流

```
明确意图 → 编写草稿 → 创建测试 → A/B 评估 → 改进迭代 → 触发优化
    ↑                                              |
    └──────────── 重复直到满意 ←───────────────────┘
```

## 待完善

以下功能在 Anthropic 原版中存在，cb-skill-creator 中尚未迁移：

- [ ] `eval-viewer/` — 可视化审查页面（generate_review.py + viewer.html）
- [ ] `assets/eval_review.html` — 触发评估交互式审查模板
- [ ] `generate_report.py` — 报告生成脚本
- [ ] `package_skill.py` — Skill 打包工具
- [ ] 多环境适配（Claude.ai / Cowork 支持）
