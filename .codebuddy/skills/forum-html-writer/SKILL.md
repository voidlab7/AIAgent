---
name: forum-html-writer
description: >
  将纯文本文章转换为论坛兼容的纯内联样式 HTML 格式。输出的 HTML 不使用 style 标签、script 标签、CSS class 或外部资源，
  所有样式均写在 style 属性中，可直接粘贴到论坛编辑器发布。
  支持自动章节编号、丰富的可视化组件（对比表格、步骤流程、信息卡片、观点卡片、进度条、SVG 图表等），
  统一的橙色主题色彩体系。
  Use when: (1) 用户要求将文章格式化为论坛 HTML, (2) 用户要求将文章转为可在论坛发布的格式,
  (3) 用户提到"论坛文章"、"论坛HTML"、"论坛格式",
  (4) 用户要求将 Markdown 或纯文本转为带内联样式的 HTML,
  (5) 用户要求创建可直接粘贴发布的 HTML 文章。
---

# Forum HTML Writer

将文章转换为论坛兼容的纯内联样式 HTML。

## 工作流程

### 1. 分析原文

Read the source text and identify:
- 文章标题、副标题
- 核心观点（用于开篇引言）
- 章节结构（按标题层级拆分为 CHAPTER）
- 每个章节中适合可视化的内容：对比、步骤、列表、公式、金句

### 2. 选择组件

For each chapter, match content to the best component. Read [references/format-spec.md](references/format-spec.md) for the complete component catalog and code snippets.

Component selection guide:

| 内容类型 | 推荐组件 |
|---------|---------|
| 核心公式/金句 | 居中观点卡片（白底 or 暖色） |
| A vs B 对比 | 两列对比表格 or GOOD/BAD卡片 |
| 正反做法 | 正反做法对比（❌ vs ✓） |
| 流程/步骤 | 步骤流程卡片（4列） |
| 多个并列概念 | 四宫格信息卡片（emoji装饰） |
| 常见错误 | 反模式清单（红+灰+绿） |
| 引用/格言/总结 | blockquote 引言块 |
| 技术说明/补充 | 蓝色信息提示卡片 |
| 警告/易错点 | 橙色注意事项卡片 |
| 数据对比 | 进度条可视化 |
| 结构关系 | 内联 SVG 图表 |

### 3. 组装 HTML

Use [assets/template.html](assets/template.html) as the starting skeleton. Follow these rules:

**Hard rules (MUST follow):**
- All styles inline via `style=""` — no `<style>`, no `class`, no `var(--)`
- No `<script>`, no external resources
- Outermost container: `max-width:760px; margin:0 auto;`
- System font stack: `-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif`
- SVG colors: direct hex values only (e.g. `fill="#d94f3b"`)

**Structure:**
```
标题区 → 开篇引言 → [hr + CHAPTER]×N → hr + 结语
```

**Chapter numbering:** `CHAPTER 01`, `CHAPTER 02`, ... with zero-padded two digits.

**English subtitles:** Each chapter title should have a short English subtitle in gray: `<span style="color:#888; font-weight:400; font-size:13px; margin-left:8px;">SUBTITLE</span>`

### 4. 质量检查

Before outputting, verify:
- [ ] No `<style>` or `<script>` tags
- [ ] No CSS classes or variables
- [ ] No external resource references
- [ ] All colors use the defined palette from format-spec.md
- [ ] Every chapter has: label + h2 title + English subtitle
- [ ] Chapters separated by `<hr>`
- [ ] At least one visual component per chapter (not just plain text)
- [ ] Opening blockquote captures the article's core thesis
- [ ] Closing section has centered title + summary + gold-sentence card

## Color Palette Quick Ref

- Theme: `#e8913a` | Title: `#1a1a1a` | Body: `#333` | Gray: `#888`
- Border: `#eae8e4` | Quote bg: `#fdf8f3` | Quote border: `#f0dcc8`
- Red: `#d94f3b` | Blue: `#3b7dd8` | Green: `#2a9d6e` | Purple: `#7c5cbf`

## Output

Save the HTML file to the user's specified path (or same directory as source). The file should be a complete, self-contained HTML fragment starting with the outer `<div>` container. Do NOT wrap in `<html>` / `<head>` / `<body>` — it's a fragment for pasting into forums.
