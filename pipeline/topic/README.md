# 趣味测试爆款选题分析

## 功能描述
支持聊天框关键词触发，自动从小红书爬取和分析当下最热门的"趣味测试"话题，并输出《爆款选题报告》。

## 触发方式

### 1. 聊天框关键词触发
在与CodeBuddy对话时，输入包含以下关键词的消息即可自动触发：

**主要关键词：**
- 趣味测试
- 心理测试
- 性格测试
- MBTI测试
- 测试分析
- 测试报告
- 爆款选题
- 小红书测试

**触发示例语句：**
```
"帮我分析一下小红书趣味测试的热点"
"抓取趣味测试数据并生成报告"
"小红书上爬取和分析当下最热门的趣味测试话题"
"生成一份趣味测试的爆款选题报告"
```

### 2. 命令行方式

```bash
# 使用示例数据演示
python main.py funtest --demo

# 使用自定义JSON数据
python main.py funtest --data your_data.json

# 通过trigger命令触发
python main.py trigger "分析小红书趣味测试热点"
```

### 3. Python代码调用

```python
from 2_选题筛选.quick_start import run_with_mcp_data

# 使用MCP获取的数据
result = run_with_mcp_data(mcp_notes_data)

# 或使用分析器
from 2_选题筛选.fun_test_analyzer import FunTestAnalyzer

analyzer = FunTestAnalyzer()
analyzer.load_notes_from_data(notes_data)
result = analyzer.analyze()
report_path = analyzer.generate_report()
```

## 工作流程

```
1. 检测触发关键词
   ↓
2. 通过MCP搜索小红书数据
   - 关键词：趣味测试、心理测试、性格测试
   - 获取热门笔记的点赞、收藏、评论、分享数据
   ↓
3. 数据分析
   - 计算热度分数
   - 分类内容类型（性格分析、情感预测、MBTI等）
   - 识别高互动内容
   ↓
4. 生成《爆款选题报告》
   - TOP 10 热门笔记
   - 内容类型分析
   - 爆款选题建议
   - 创作指南
```

## 输出报告

报告保存在 `reports/` 目录下，文件名格式：
```
趣味测试爆款选题报告_YYYYMMDD.md
```

报告包含：
1. **热度概览** - 核心数据统计
2. **热门TOP 10** - 最热门的笔记及其数据
3. **内容类型分析** - 各类测试内容的表现分析
4. **爆款选题建议** - 推荐的创作方向和标题模板
5. **创作指南** - 制作技巧和发布建议
6. **数据附录** - 完整的笔记数据

## MCP数据格式

如果您要手动提供数据，请使用以下JSON格式：

```json
[
  {
    "note_id": "笔记ID",
    "title": "笔记标题",
    "author": "作者名称",
    "likes": 10000,
    "collects": 500,
    "comments": 200,
    "shares": 100,
    "url": "https://www.xiaohongshu.com/explore/xxx",
    "type": "图文"
  }
]
```

## 文件结构

```
2_选题筛选/
├── __init__.py           # 模块初始化
├── fun_test_analyzer.py  # 核心分析器
├── keyword_trigger.py    # 关键词触发器
├── fun_test_workflow.py  # 自动化工作流
├── quick_start.py        # 快速启动脚本
└── README.md             # 本文档
```

## 依赖

- Python 3.8+
- 小红书MCP（用于数据爬取）

## 使用小红书MCP

确保小红书MCP已配置并登录：

```bash
# 检查登录状态
# 使用CodeBuddy的MCP工具: check_login_status

# 搜索数据
# 使用CodeBuddy的MCP工具: search_feeds
# 参数: keyword="趣味测试", filters={"sort_by": "最多点赞"}
```

## 示例输出

```
🎯 趣味测试爆款选题分析

📊 数据概览
- 分析笔记数: 50 篇
- 总点赞数: 85,000
- 总收藏数: 12,000
- 总评论数: 35,000

🔥 热门 TOP 5
1. 别笑，你也过不了第二关 - 👍19,183
2. 情侣小测试！蒙眼猜身高 - 👍10,642
3. 内向程度测试题 - 👍4,030
4. 神秘小实验 - 👍3,960
5. 反应力测试 - 👍1,913

📝 完整报告已生成: reports/趣味测试爆款选题报告_20260314.md
```

## 注意事项

1. 首次使用前请确保小红书MCP已登录
2. 建议每周运行一次以追踪热点变化
3. 报告中的选题建议仅供参考，请结合自身账号定位使用
