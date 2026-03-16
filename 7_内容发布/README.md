# 模块7：登后台发布 (Publisher)

## 功能描述
自动化发布文章到各平台（通过 MCP 或 API）。

## 输入
- 格式化后的文章（来自模块6）
- 发布配置（定时、标签、原创声明）

## 输出
- 发布状态
- 平台文章 ID
- 实时数据（阅读量、点赞、评论）

## 核心能力
1. **自动登录**：MCP 管理平台账号
2. **定时发布**：支持预约发布
3. **批量发布**：一键发布到多个平台
4. **效果追踪**：实时抓取文章数据

## 文件结构
```
7_内容发布/
├── platforms/          # 平台发布器
│   ├── weixin.py      # 微信公众号 (MCP)
│   ├── xiaohongshu.py # 小红书 (MCP)
│   └── zhihu.py       # 知乎 (API)
├── scheduler.py        # 定时发布
├── tracker.py          # 效果追踪
├── main.py
└── README.md
```

## 使用方式

### 立即发布
```bash
python -m 7_内容发布.main --article-id 1 --platform weixin
```

### 定时发布
```bash
python -m 7_内容发布.main --article-id 1 --platform weixin --schedule "2026-03-11 08:00"
```

### 批量发布到多平台
```bash
python -m 7_内容发布.main --article-id 1 --platforms weixin,xiaohongshu
```

### 查看发布状态
```bash
python -m 7_内容发布.main --list
```

## Skill 规划
**Skill 名称**：`auto-publisher.md`

**核心工作流**：
1. 读取格式化文章
2. 根据平台调用对应发布器
3. **微信公众号**：
   - 调用 `wechat-publisher-mcp`
   - 上传封面图
   - 发布文章（预览/正式）
4. **小红书**：
   - 调用 `RedNote-MCP`（发布功能需开发）
   - 上传图片
   - 发布笔记
5. 记录发布状态到 `publish_records`
6. 定时任务：每 1 小时抓取文章数据（阅读/点赞）

## 数据表
`publish_records` 表（`common/database.py`）

## 依赖
- wechat-publisher-mcp (微信公众号)
- RedNote-MCP (小红书，需扩展发布能力)
- APScheduler (定时任务)

## 开发状态
📋 待开发

## 注意事项
- 微信公众号建议先用**预览模式**人工审核后再发布
- 小红书 MCP 目前只有搜索功能，发布能力需要扩展
- 知乎暂无官方 API，可能需要 Selenium
