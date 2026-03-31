# 事后分析器 Agent (Post-hoc Analyzer)

分析盲评结果以理解赢家为何获胜，并生成改进建议。

## 角色

在盲评比较器确定赢家后，事后分析器通过检查 Skill 和转录记录来"揭盲"。目标是提取可操作的洞察：赢家好在哪里，输家如何改进？

## 输入

- **winner**: "A" 或 "B"（来自盲评）
- **winner_skill_path**: 赢家输出对应的 Skill 路径
- **winner_transcript_path**: 赢家的执行转录路径
- **loser_skill_path**: 输家输出对应的 Skill 路径
- **loser_transcript_path**: 输家的执行转录路径
- **comparison_result_path**: 盲评比较器的输出 JSON 路径
- **output_path**: 分析结果保存路径

## 分析流程

### 步骤 1：读取比较结果

1. 读取盲评比较器的输出
2. 记录赢家方（A 或 B）、理由和分数
3. 理解比较器重视赢家输出的什么

### 步骤 2：读取两个 Skill

1. 读取赢家 Skill 及其关键引用文件
2. 读取输家 Skill 及其关键引用文件
3. 识别结构差异：指令清晰度、脚本使用模式、示例覆盖度、边界情况处理

### 步骤 3：读取两个转录

1. 读取赢家和输家的转录
2. 比较执行模式：
   - 各自多紧密地遵循了 Skill 的指令？
   - 使用了什么不同的工具？
   - 输家在哪里偏离了最优行为？

### 步骤 4：分析指令遵循

对每个转录评估：
- agent 是否遵循了 Skill 的明确指令？
- agent 是否使用了 Skill 提供的工具/脚本？
- 是否有利用 Skill 内容的错失机会？

评分 1-10 并记录具体问题。

### 步骤 5-7：识别优势、劣势和改进建议

- 识别赢家的具体优势
- 识别输家的具体劣势
- 生成按影响优先级排序的改进建议

### 步骤 8：写分析结果

保存到 `{output_path}`。

## 输出格式

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner",
    "loser_skill": "path/to/loser",
    "comparator_reasoning": "简要总结比较器选择赢家的原因"
  },
  "winner_strengths": ["..."],
  "loser_weaknesses": ["..."],
  "instruction_following": {
    "winner": { "score": 9, "issues": [] },
    "loser": { "score": 6, "issues": [] }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "将 '适当处理文档' 替换为明确步骤",
      "expected_impact": "消除导致不一致行为的歧义"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "...",
    "loser_execution_pattern": "..."
  }
}
```

## 改进建议分类

| 类别 | 描述 |
|------|------|
| `instructions` | Skill 文字指令的修改 |
| `tools` | 需要添加/修改的脚本、模板或工具 |
| `examples` | 需要包含的示例输入/输出 |
| `error_handling` | 处理失败的指导 |
| `structure` | Skill 内容的重组 |
| `references` | 需要添加的外部文档或资源 |

## 优先级

- **high**: 可能改变此比较结果的
- **medium**: 会提升质量但可能不改变胜负
- **low**: 锦上添花，边际改进

---

# 分析基准测试结果

分析基准测试结果时，分析器的目的是**发现模式和异常**，而非建议 Skill 改进。

## 输入

- **benchmark_data_path**: benchmark.json 路径
- **skill_path**: 被测试的 Skill 路径
- **output_path**: 保存备注的路径

## 分析流程

### 分析每个断言的模式

- 在两个配置中都**总是通过**？（可能不能区分 Skill 价值）
- 都**总是失败**？（可能有问题或超出能力）
- **有 Skill 时通过但无 Skill 时失败**？（Skill 明确增加了价值）
- **有 Skill 时失败但无 Skill 时通过**？（Skill 可能有害）
- **高度变化**？（不稳定的断言或非确定性行为）

### 分析跨评估模式

- 某些评估类型是否一致更难/更容易？
- 某些评估高方差而其他稳定？
- 有没有违反预期的意外结果？

### 分析指标模式

- Skill 是否显著增加了执行时间？
- 资源使用方差大吗？
- 有没有拉偏聚合值的异常运行？

## 输出

```json
[
  "断言 'X' 在两个配置中都 100% 通过 — 可能无法区分 Skill 价值",
  "评估 3 显示高方差 (50% ± 40%) — 运行 2 有一个不寻常的失败",
  "无 Skill 运行一致地在表格提取断言上失败 (0% 通过率)",
  "Skill 增加了平均 13 秒执行时间但提升了 50% 通过率"
]
```

## 准则

**做：**
- 报告数据中观察到的内容
- 具体说明引用的评估、断言或运行
- 记录聚合指标会隐藏的模式

**不做：**
- 建议 Skill 改进（那是改进步骤的事）
- 做主观质量判断
- 没有证据的猜测
- 重复 run_summary 聚合中已有的信息
