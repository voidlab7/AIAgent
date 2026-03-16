# 模块6：排版 (Formatter)

## 功能描述
将 Markdown 文章转换为各平台专属格式，并美化排版。

## 输入
- 文章内容（Markdown）
- 目标平台（微信/小红书/知乎）
- 配图列表

## 输出
- 平台专属格式（HTML/Markdown）
- 预览 HTML
- 样式配置（CSS/主题）

## 核心能力
1. **格式转换**：Markdown → 微信 HTML/小红书文本
2. **样式美化**：代码高亮、引用块、分割线
3. **配图插入**：自动插入封面 + 内文图
4. **一键复制**：生成可直接粘贴到后台的格式

## 文件结构
```
6_格式优化/
├── converters/         # 格式转换器
│   ├── weixin.py      # 微信公众号 HTML
│   ├── xiaohongshu.py # 小红书纯文本+表情
│   └── zhihu.py       # 知乎 Markdown
├── themes/             # 样式主题
│   ├── default.css
│   └── tech.css
├── main.py
└── README.md
```

## 使用方式

### 转换为微信格式
```bash
python -m 6_格式优化.main --article-id 1 --platform weixin
```

### 批量转换
```bash
python -m 6_格式优化.main --batch --platform weixin
```

### 预览
```bash
python -m 6_格式优化.main --article-id 1 --preview
```

## Skill 规划
**Skill 名称**：`format-adapter.md`

**核心工作流**：
1. 读取文章内容 + 配图
2. 根据目标平台选择转换器
3. **微信公众号**：
   - Markdown → HTML
   - 应用样式主题
   - 插入配图（居中、间距）
   - 生成可复制的 HTML
4. **小红书**：
   - 纯文本 + 表情包
   - 分段优化（短句、回车）
   - 标签提取（#话题#）
5. **知乎**：
   - Markdown（保留原样）
   - 插入配图链接
6. 生成预览文件
7. 更新 `articles` 表状态

## 数据表
`articles` 表（更新 `status` 为 `formatted`）

## 依赖
- markdown2
- BeautifulSoup4
- Pygments (代码高亮)

## 开发状态
📋 待开发

## 参考项目
- [md-nice](https://github.com/mdnice/markdown-nice) - 微信 Markdown 编辑器
