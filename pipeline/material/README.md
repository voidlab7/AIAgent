# 模块3：搜资料整理素材 (Material Collector)

## 功能描述
根据确定的选题，自动搜集、整理、结构化素材。

## 输入
- 选题信息（来自模块2）
- 搜索深度配置

## 输出
结构化素材库：
- **观点类**：专家观点、用户评论
- **数据类**：统计数据、图表
- **案例类**：成功案例、失败案例
- **金句类**：可引用的精彩语句

## 核心能力
1. **多源搜索**：Google、Bing、微信搜狗、知乎、小红书
2. **智能摘要**：AI 提取核心信息
3. **去重整合**：合并相似素材
4. **结构化存储**：分类标签 + 可搜索

## 文件结构
```
3_素材采集/
├── searchers/          # 搜索引擎
│   ├── google.py
│   └── weixin.py
├── extractors/         # 内容提取
│   ├── article.py
│   └── comment.py
├── organizer.py        # 素材整理
├── main.py
└── README.md
```

## 使用方式

### 为指定选题搜集素材
```bash
python -m 3_素材采集.main --topic-id 1
```

### 批量搜集（未搜集的选题）
```bash
python -m 3_素材采集.main --batch
```

### 查看素材库
```bash
python -m 3_素材采集.main --show --topic-id 1
```

## Skill 规划
**Skill 名称**：`material-organizer.md`

**核心工作流**：
1. 读取选题信息
2. 生成搜索查询（AI 扩展关键词）
3. 并发搜索（Google + 微信 + 知乎 + 小红书）
4. 内容提取：
   - 文章正文提取
   - 评论区挖掘
5. AI 摘要 + 分类（观点/数据/案例/金句）
6. 去重整合
7. 存入 `materials` 表

## 数据表
`materials` 表（`common/database.py`）

## 依赖
- Serper API (Google Search)
- BeautifulSoup4
- Readability (正文提取)
- OpenAI API (摘要)

## 开发状态
📋 待开发

## 注意事项
- 搜索结果需要缓存，避免重复请求
- 优先使用已有的 `ai_daily_fetcher` 微信/小红书抓取能力
