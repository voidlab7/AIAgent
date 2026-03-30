# 模块5：找配图 (Image Finder)

## 功能描述
自动为文章匹配合适的配图（封面图 + 内文插图）。

## 输入
- 文章内容（Markdown）
- 平台要求（尺寸、数量）

## 输出
- **图片列表**：URL + 本地缓存路径
- **Alt 文本**：图片描述（SEO）

## 核心能力
1. **语义匹配**：AI 理解文章主题，匹配图片
2. **多源搜索**：Unsplash、Pexels、免费图库
3. **尺寸适配**：自动裁剪/压缩
4. **AI 生成**（可选）：DALL-E、Midjourney

## 文件结构
```
5_配图查找/
├── searchers/          # 图片源
│   ├── unsplash.py
│   └── pexels.py
├── matcher.py          # 语义匹配
├── processor.py        # 图片处理（裁剪/压缩）
├── main.py
└── README.md
```

## 使用方式

### 为文章找配图
```bash
python -m 5_配图查找.main --article-id 1
```

### 仅封面图
```bash
python -m 5_配图查找.main --article-id 1 --cover-only
```

## Skill 规划
**Skill 名称**：`image-matcher.md`

**核心工作流**：
1. 读取文章内容
2. AI 提取关键词（主题、情绪、风格）
3. 搜索图片（Unsplash API）
4. 语义匹配：
   - 图片描述 vs 关键词
   - 打分排序
5. 下载缓存到本地
6. 尺寸适配（平台要求）
7. 存入 `images` 表

## 数据表
`images` 表（`common/database.py`）

## 依赖
- Unsplash API
- Pexels API
- Pillow (图片处理)

## 开发状态
📋 待开发
