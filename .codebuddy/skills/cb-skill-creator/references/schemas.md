# JSON Schemas

本文档定义 cb-skill-creator 使用的 JSON 数据结构。

---

## evals.json

定义 Skill 的评估用例。位于 `evals/evals.json`（在 Skill 工作区中）。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的示例 prompt",
      "expected_output": "期望结果描述",
      "files": ["evals/files/sample1.txt"],
      "expectations": [
        "输出包含 X",
        "Skill 使用了脚本 Y"
      ]
    }
  ]
}
```

**字段说明：**
- `skill_name`: 匹配 Skill 文件名
- `evals[].id`: 唯一整数标识符
- `evals[].prompt`: 要执行的任务描述
- `evals[].expected_output`: 人类可读的成功描述
- `evals[].files`: 可选的输入文件路径列表（相对于 Skill 根目录）
- `evals[].expectations`: 可验证的断言列表

---

## history.json

跟踪改进模式中的版本进展。位于工作区根目录。

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "extension-analyze",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

**字段说明：**
- `started_at`: 改进开始的 ISO 时间戳
- `skill_name`: 被改进的 Skill 名称
- `current_best`: 最佳版本标识
- `iterations[].version`: 版本标识（v0, v1, ...）
- `iterations[].parent`: 派生自的父版本
- `iterations[].expectation_pass_rate`: 评分通过率
- `iterations[].grading_result`: "baseline", "won", "lost", 或 "tie"
- `iterations[].is_current_best`: 是否为当前最佳版本

---

## eval_metadata.json

每个评估运行的元数据。位于 `<eval-dir>/eval_metadata.json`。

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "用户的任务 prompt",
  "assertions": [
    "输出包含所有异常插件的列表",
    "报告包含 Root Cause 分析"
  ]
}
```

---

## grading.json

评分器 agent 的输出。位于 `<run-dir>/grading.json`。

```json
{
  "expectations": [
    {
      "text": "输出包含所有异常插件的列表",
      "passed": true,
      "evidence": "在报告的 Extension Summary 部分找到了 5 个异常插件的列表"
    },
    {
      "text": "报告包含 Root Cause 分析",
      "passed": false,
      "evidence": "报告只有 Overview 和 Summary，没有 Root Cause 分析部分"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 1,
    "total": 2,
    "pass_rate": 0.50
  },
  "execution_metrics": {
    "tool_calls": {
      "read_file": 5,
      "write_to_file": 2,
      "execute_command": 8
    },
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450
  },
  "timing": {
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "识别了 3 个 CRX 解压失败的插件",
      "type": "factual",
      "verified": true,
      "evidence": "在输出中确认找到了 3 条 OnUnpackFailure 日志"
    }
  ],
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "输出包含所有异常插件的列表",
        "reason": "一个只输出插件名称但不包含错误详情的报告也会通过"
      }
    ],
    "overall": "断言检查了存在性但没有检查正确性。"
  }
}
```

**关键字段说明：**
- `expectations[]`: 评分后的断言，使用 `text`、`passed`、`evidence` 字段
- `summary`: 聚合的通过/失败计数
- `execution_metrics`: 工具使用和输出大小
- `timing`: 时间数据
- `claims`: 从输出中提取并验证的声明
- `eval_feedback`: 对评估本身的改进建议（仅在有必要时出现）

---

## timing.json

运行的时间数据。位于 `<run-dir>/timing.json`。

```json
{
  "total_duration_seconds": 23.3,
  "start_time": "2026-01-15T10:30:00Z",
  "end_time": "2026-01-15T10:30:23Z"
}
```

---

## benchmark.json

基准测试输出。位于 `<workspace>/iteration-N/benchmark.json`。

```json
{
  "metadata": {
    "skill_name": "extension-analyze",
    "skill_path": "/path/to/extension-analyze.md",
    "timestamp": "2026-01-15T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 1
  },
  "runs": [
    {
      "eval_id": 1,
      "eval_name": "基本插件分析",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 42.5,
        "errors": 0
      },
      "expectations": [
        {"text": "...", "passed": true, "evidence": "..."}
      ]
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 45.0, "stddev": 12.0, "min": 32.0, "max": 58.0}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08, "min": 0.28, "max": 0.45},
      "time_seconds": {"mean": 32.0, "stddev": 8.0, "min": 24.0, "max": 42.0}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0"
    }
  },
  "notes": [
    "断言 '输出是有效的报告' 在两个配置中都 100% 通过 — 可能无法区分 Skill 价值",
    "评估 3 显示高方差 — 可能不稳定"
  ]
}
```

**重要：** 查看器按这些字段名精确读取。使用 `config` 替代 `configuration`，或将 `pass_rate` 放在 run 顶层而非嵌套在 `result` 下，会导致查看器显示空值。生成 benchmark.json 时始终参考此 schema。

---

## comparison.json

盲评比较器输出。位于 `<grading-dir>/comparison.json`。

```json
{
  "winner": "A",
  "reasoning": "输出 A 提供了完整的解决方案...",
  "rubric": {
    "A": {
      "content": { "correctness": 5, "completeness": 5, "accuracy": 4 },
      "structure": { "organization": 4, "formatting": 5, "usability": 4 },
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": { "correctness": 3, "completeness": 2, "accuracy": 3 },
      "structure": { "organization": 3, "formatting": 2, "usability": 3 },
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": { "score": 9, "strengths": [...], "weaknesses": [...] },
    "B": { "score": 5, "strengths": [...], "weaknesses": [...] }
  },
  "expectation_results": {
    "A": { "passed": 4, "total": 5, "pass_rate": 0.80, "details": [...] },
    "B": { "passed": 3, "total": 5, "pass_rate": 0.60, "details": [...] }
  }
}
```

---

## analysis.json

事后分析器输出。位于 `<grading-dir>/analysis.json`。

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner",
    "loser_skill": "path/to/loser",
    "comparator_reasoning": "简要总结"
  },
  "winner_strengths": ["..."],
  "loser_weaknesses": ["..."],
  "instruction_following": {
    "winner": { "score": 9, "issues": [] },
    "loser": { "score": 6, "issues": ["..."] }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "...",
      "expected_impact": "..."
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "...",
    "loser_execution_pattern": "..."
  }
}
```

---

## trigger_eval.json

触发评估查询集。用于描述优化。

```json
[
  {"query": "帮我分析一下这个日志里的插件加载错误", "should_trigger": true},
  {"query": "写一个 Python 脚本读取 JSON 文件", "should_trigger": false}
]
```

---

## feedback.json

用户审查反馈。由评估查看器生成。

```json
{
  "reviews": [
    {
      "run_id": "eval-0-with_skill",
      "feedback": "报告缺少时间线分析",
      "timestamp": "2026-01-15T10:45:00Z"
    },
    {
      "run_id": "eval-1-with_skill",
      "feedback": "",
      "timestamp": "2026-01-15T10:46:00Z"
    }
  ],
  "status": "complete"
}
```
