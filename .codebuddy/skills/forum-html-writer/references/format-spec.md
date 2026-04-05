# 论坛 HTML 格式规范

## 硬性约束

- **纯内联样式**：不使用 `<style>`、`<script>`、`<link>` 标签
- **零外部依赖**：不引用外部 CSS / JS / 字体 / 图片 CDN
- **无 CSS 变量**：内联样式不支持 `var(--xxx)`，SVG 颜色必须直接写色值
- **无 CSS class**：论坛编辑器不认 class 属性

## 最外层容器

```html
<div style="max-width:760px; margin:0 auto; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; color:#1a1a1a; line-height:1.8; font-size:15px;">
  ...全部内容...
</div>
```

## 色彩体系

| 用途 | 色值 | 场景 |
|------|------|------|
| 主题色（橙） | `#e8913a` | 章节标签、强调文字、核心观点、金句 |
| 标题色 | `#1a1a1a` | h1、h2 标题 |
| 正文色 | `#333` | 段落文字 |
| 辅助灰 | `#888` | 英文副标题、图注、辅助说明 |
| 边框色 | `#eae8e4` | 表格边框、分割线、卡片边框 |
| 引言背景 | `#fdf8f3` | blockquote 和暖色卡片的背景 |
| 引言边框 | `#f0dcc8` | 暖色卡片的边框 |
| 红色 | `#d94f3b` | 错误/反面/警告 |
| 蓝色 | `#3b7dd8` | 中性信息/技术说明/步骤编号 |
| 绿色 | `#2a9d6e` | 正确/正面/成功 |
| 紫色 | `#7c5cbf` | 特殊分类标记 |
| 蓝色信息卡背景 | `#f5f8ff` | 蓝色提示卡片背景 |
| 蓝色信息卡边框 | `#d4e2f7` | 蓝色提示卡片边框 |

## 文档骨架

```
标题区          居中：h1 + 副标题 + 引导语
开篇引言        blockquote 概括全文核心
──分割线──
CHAPTER 01      章节标签 + h2标题 + 正文 + 组件
──分割线──
CHAPTER 02      ...
──分割线──
...
──分割线──
结语            居中收尾 + 金句卡片
```

## 组件代码片段

### 1. 标题区

```html
<div style="text-align:center; padding:32px 0 24px;">
  <h1 style="font-size:32px; font-weight:900; color:#1a1a1a; margin:0 0 8px; line-height:1.4;">主标题</h1>
  <p style="color:#888; font-size:15px; margin:0 0 24px;">副标题 <span style="color:#e8913a; font-weight:700;">强调词</span></p>
</div>
```

### 2. 开篇引言

```html
<blockquote style="border-left:3px solid #e8913a; padding:16px 20px; margin:20px 0 32px; background:#fdf8f3; color:#1a1a1a; font-size:14px; line-height:1.9;">
  核心观点一。<br>
  核心观点二，可以用 <strong>加粗</strong> 强调。
</blockquote>
```

### 3. 分割线

```html
<hr style="border:none; border-top:1px solid #eae8e4; margin:36px 0;">
```

### 4. 章节标题

```html
<p style="font-size:12px; color:#e8913a; letter-spacing:2px; margin:0 0 4px;">CHAPTER 01</p>
<h2 style="font-size:20px; font-weight:800; color:#1a1a1a; margin:0 0 16px; line-height:1.4;">中文标题 <span style="color:#888; font-weight:400; font-size:13px; margin-left:8px;">ENGLISH SUBTITLE</span></h2>
```

### 5. 正文段落

```html
<p style="font-size:15px; color:#333; line-height:2; margin-bottom:14px;">正文内容。<strong>加粗</strong>。<span style="color:#e8913a; font-weight:500;">主题色强调</span>。</p>
```

### 6. 居中观点卡片

白底版：
```html
<div style="text-align:center; padding:24px; background:#fff; border:1px solid #eae8e4; border-radius:8px; margin:20px 0;">
  <div style="font-size:18px; font-weight:700; color:#1a1a1a; margin-bottom:6px;">核心观点 = <span style="color:#e8913a;">A</span> + <span style="color:#e8913a;">B</span></div>
  <div style="font-size:13px; color:#888;">补充说明</div>
</div>
```

暖色版：
```html
<div style="text-align:center; padding:20px; background:#fdf8f3; border:1px solid #f0dcc8; border-radius:8px; margin:20px 0;">
  <div style="font-size:16px; font-weight:700; color:#e8913a; margin-bottom:6px;">金句标题</div>
  <div style="font-size:15px; color:#1a1a1a; font-weight:600;">金句内容</div>
</div>
```

红色警告版：
```html
<div style="text-align:center; padding:20px; background:#fff; border:1px solid #eae8e4; border-radius:8px; margin:20px 0;">
  <div style="font-size:17px; font-weight:700; color:#d94f3b;">警告型观点</div>
</div>
```

### 7. 两列对比表格（带表头）

```html
<table style="width:100%; border-collapse:collapse; margin:20px 0; font-size:14px;">
  <thead>
    <tr>
      <th style="text-align:left; padding:12px 16px; background:#f5f0fa; color:#7c5cbf; font-weight:700; border:1px solid #eae8e4;">🧙 方案A</th>
      <th style="text-align:left; padding:12px 16px; background:#f0f7f2; color:#2a9d6e; font-weight:700; border:1px solid #eae8e4;">⚙️ 方案B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:10px 16px; border:1px solid #eae8e4; color:#555; line-height:1.7;">描述</td>
      <td style="padding:10px 16px; border:1px solid #eae8e4; color:#555; line-height:1.7;">描述</td>
    </tr>
  </tbody>
</table>
```

### 8. 正反做法对比（emoji + 颜色）

```html
<table style="width:100%; border-collapse:collapse; margin:20px 0; font-size:14px;">
  <tr>
    <td style="width:50%; padding:18px; border:1px solid #eae8e4; vertical-align:top; background:#fff;">
      <div style="font-size:18px; margin-bottom:8px;">❌</div>
      <div style="font-weight:700; margin-bottom:4px; color:#d94f3b;">错误做法</div>
      <div style="color:#888; font-size:13px; line-height:1.7;">原因</div>
    </td>
    <td style="width:50%; padding:18px; border:1px solid #eae8e4; vertical-align:top; background:#fff;">
      <div style="font-size:18px; margin-bottom:8px;">✓</div>
      <div style="font-weight:700; margin-bottom:4px; color:#2a9d6e;">正确做法</div>
      <div style="color:#888; font-size:13px; line-height:1.7;">原因</div>
    </td>
  </tr>
</table>
```

### 9. GOOD / BAD 带色背景卡片

```html
<table style="width:100%; border-collapse:collapse; margin:20px 0; font-size:14px;">
  <tr>
    <td style="width:50%; padding:16px; border:1px solid #eae8e4; vertical-align:top; background:#f0f7f2;">
      <div style="font-size:11px; font-weight:700; color:#2a9d6e; letter-spacing:1px; margin-bottom:4px;">GOOD</div>
      <div style="font-weight:700; margin-bottom:4px; color:#1a1a1a;">标题</div>
      <div style="color:#555; font-size:13px; line-height:1.7;">✓ 好处一<br>✓ 好处二</div>
    </td>
    <td style="width:50%; padding:16px; border:1px solid #eae8e4; vertical-align:top; background:#fdf2f0;">
      <div style="font-size:11px; font-weight:700; color:#d94f3b; letter-spacing:1px; margin-bottom:4px;">BAD</div>
      <div style="font-weight:700; margin-bottom:4px; color:#1a1a1a;">标题</div>
      <div style="color:#555; font-size:13px; line-height:1.7;">✕ 问题一<br>✕ 问题二</div>
    </td>
  </tr>
</table>
```

### 10. 步骤流程卡片

```html
<table style="width:100%; border-collapse:collapse; margin:20px 0; font-size:14px;">
  <tr>
    <td style="width:25%; padding:18px 14px; border:1px solid #eae8e4; vertical-align:top; background:#fff; text-align:center;">
      <div style="font-size:28px; font-weight:900; color:#3b7dd8; opacity:0.15; line-height:1; margin-bottom:8px;">1</div>
      <div style="font-weight:700; margin-bottom:4px; font-size:13px;">标题</div>
      <div style="color:#888; font-size:12px; line-height:1.6;">说明</div>
    </td>
    <!-- 重复 td 用 #e8913a / #d94f3b / #2a9d6e 交替颜色 -->
  </tr>
</table>
```

步骤数字颜色顺序：`#3b7dd8` → `#e8913a` → `#d94f3b` → `#2a9d6e`。

### 11. 四宫格信息卡片

```html
<table style="width:100%; border-collapse:collapse; margin:20px 0; font-size:14px;">
  <tr>
    <td style="width:50%; padding:16px; border:1px solid #eae8e4; vertical-align:top; background:#fff;">
      <div style="font-size:18px; margin-bottom:8px;">📐</div>
      <div style="font-weight:700; margin-bottom:4px; color:#1a1a1a;">标题</div>
      <div style="color:#888; font-size:13px; line-height:1.7;">说明文字</div>
    </td>
    <td style="width:50%; padding:16px; border:1px solid #eae8e4; vertical-align:top; background:#fff;">
      <div style="font-size:18px; margin-bottom:8px;">🧩</div>
      <div style="font-weight:700; margin-bottom:4px; color:#1a1a1a;">标题</div>
      <div style="color:#888; font-size:13px; line-height:1.7;">说明文字</div>
    </td>
  </tr>
  <!-- 第二行同理 -->
</table>
```

### 12. 反模式清单

```html
<table style="width:100%; border-collapse:collapse; margin:20px 0; font-size:13px;">
  <tr>
    <td style="padding:14px 16px; border:1px solid #eae8e4; vertical-align:top; background:#fff; width:50%;">
      <strong style="color:#d94f3b;">✕ 错误做法</strong><br>
      <span style="color:#888; font-size:12px;">问题</span><br>
      <span style="color:#2a9d6e; font-size:12px; font-weight:500;">→ 正确方案</span>
    </td>
  </tr>
</table>
```

### 13. 章节引言块

```html
<blockquote style="border-left:3px solid #e8913a; padding:14px 20px; margin:20px 0; background:#fdf8f3; color:#555; font-size:14px; line-height:1.8; font-style:italic;">
  引言内容。
</blockquote>
```

### 14. 信息提示卡片

蓝色（技术说明）：
```html
<div style="padding:20px 24px; background:#f5f8ff; border:1px solid #d4e2f7; border-radius:8px; margin:20px 0;">
  <div style="display:inline-block; font-size:11px; font-weight:700; padding:3px 10px; background:#e8f0fe; color:#3b7dd8; border-radius:4px; margin-bottom:10px;">标签</div>
  <div style="font-weight:700; font-size:15px; margin-bottom:6px; color:#1a1a1a;">标题</div>
  <p style="font-size:14px; color:#555; line-height:1.8; margin:0;">内容</p>
</div>
```

橙色（注意事项）：
```html
<div style="padding:20px 24px; background:#fdf8f3; border:1px solid #f0dcc8; border-radius:8px; margin:20px 0;">
  <div style="display:inline-block; font-size:11px; font-weight:700; padding:3px 10px; background:#fceede; color:#e8913a; border-radius:4px; margin-bottom:10px;">⚠️ 注意</div>
  <div style="font-weight:700; font-size:15px; margin-bottom:6px; color:#1a1a1a;">标题</div>
  <p style="font-size:14px; color:#555; line-height:1.8; margin:0;">内容</p>
</div>
```

### 15. 进度条

```html
<div style="padding:24px; background:#fff; border:1px solid #eae8e4; border-radius:8px; margin:20px 0;">
  <div style="margin-bottom:14px;">
    <div style="font-size:13px; font-weight:600; color:#2a9d6e; margin-bottom:6px;">标签 — 90%</div>
    <div style="background:#eae8e4; border-radius:6px; overflow:hidden; height:28px;">
      <div style="width:90%; height:100%; background:linear-gradient(90deg,#2a9d6e,#48c78e); border-radius:6px; color:#fff; font-size:11px; font-weight:600; line-height:28px; padding-left:12px;">说明</div>
    </div>
  </div>
</div>
```

### 16. SVG 图表容器

```html
<div style="background:#fff; border:1px solid #eae8e4; border-radius:14px; padding:32px; margin:24px 0;">
  <div style="font-size:14px; font-weight:700; color:#1a1a1a; margin-bottom:16px;">图表标题 <span style="color:#888; font-weight:400; font-size:12px;">LABEL</span></div>
  <svg viewBox="0 0 720 300" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block; max-width:100%;">
    <!-- SVG 内容，所有颜色直接用色值 -->
  </svg>
  <p style="font-size:12px; color:#888; text-align:center; margin:12px 0 0;">图注</p>
</div>
```

### 17. 图片

```html
<div style="text-align:center; margin:24px 0;">
  <img src="文件名.png" alt="描述" style="max-width:100%; height:auto; border-radius:8px; border:1px solid #eae8e4;">
  <p style="font-size:12px; color:#888; margin-top:8px;">图片说明</p>
</div>
```

### 18. 结语区

```html
<hr style="border:none; border-top:1px solid #eae8e4; margin:40px 0;">
<div style="text-align:center; padding:20px 0 32px;">
  <h2 style="font-size:22px; font-weight:900; color:#1a1a1a; margin:0 0 16px; line-height:1.5;">结语标题<br>可以<span style="color:#e8913a;">换行强调</span></h2>
  <p style="font-size:14px; color:#555; max-width:520px; margin:0 auto 24px; line-height:2;">
    结语正文。
  </p>
  <div style="max-width:480px; margin:0 auto; padding:18px 24px; background:#fdf8f3; border:1px solid #f0dcc8; border-radius:8px; font-size:15px; font-weight:700; color:#e8913a;">
    ✦ 收尾金句 ✦
  </div>
</div>
```

## 样式速查

| 元素 | 样式 |
|------|------|
| 正文段落 | `font-size:15px; color:#333; line-height:2; margin-bottom:14px;` |
| 章节标题 | `font-size:20px; font-weight:800; color:#1a1a1a; margin:0 0 16px; line-height:1.4;` |
| 章节标签 | `font-size:12px; color:#e8913a; letter-spacing:2px; margin:0 0 4px;` |
| 英文副标题 | `color:#888; font-weight:400; font-size:13px; margin-left:8px;` |
| 表格单元格 | `padding:10px 16px; border:1px solid #eae8e4; color:#555; line-height:1.7;` |
| 引言块 | `border-left:3px solid #e8913a; padding:14px 20px; margin:20px 0; background:#fdf8f3;` |
| 分割线 | `border:none; border-top:1px solid #eae8e4; margin:36px 0;` |
| 主题色强调 | `color:#e8913a; font-weight:500;` |
