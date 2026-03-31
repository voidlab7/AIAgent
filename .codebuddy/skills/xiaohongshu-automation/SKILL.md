---
name: xiaohongshu-automation
description: >
  小红书自动化技能。当用户需要搜索小红书热门内容、获取笔记详情、发布图文/视频、
  点赞收藏评论、或批量抓取热点时使用。集成 xiaohongshu-mcp 服务的 13 个工具。
allowed-tools:
  - search_feeds
  - get_feed_detail
  - list_feeds
  - publish_content
  - publish_with_video
  - like_feed
  - favorite_feed
  - post_comment_to_feed
  - reply_comment_in_feed
  - user_profile
  - check_login_status
---

# 小红书自动化技能

通过 MCP 服务与小红书平台交互，支持内容搜索、发布、互动等全流程自动化。

## 前置条件

- xiaohongshu-mcp 服务已启动（端口 18060）
- 已登录小红书账号（Cookie 有效）

验证服务状态：
```bash
curl -s http://localhost:18060/health
```

---

## ⚠️ 关键经验：发布超时问题与解决方案

### 问题描述

MCP 客户端对工具调用有 **10 秒超时限制**，但 `publish_content` 需要操控浏览器完成以下步骤：
1. 上传图片（浏览器文件选择器）
2. 填写标题和正文
3. 逐个点击话题标签联想选项
4. 设置可见范围
5. 点击发布按钮

实际耗时约 **30-50 秒**，远超 10 秒限制，导致 MCP 工具调用必定超时。

### 解决方案：直接调用 HTTP API（推荐）

xiaohongshu-mcp 服务同时提供了 HTTP REST API，**绕过 MCP 客户端的超时限制**。

**发布图文内容**：
```bash
curl -s -w "\nHTTP_CODE:%{http_code}\nTIME:%{time_total}s\n" \
  --max-time 120 \
  -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "标题（≤20中文字）",
    "content": "正文内容（不含#标签）",
    "images": ["/tmp/image.png"],
    "tags": ["标签1", "标签2"],
    "is_original": false,
    "visibility": ""
  }'
```

**关键参数**：
- `--max-time 120`：设置 120 秒超时，足够完成发布
- 返回 HTTP 200 表示发布成功
- 可通过 `-w` 参数查看实际耗时

### 发布策略（三级降级）

1. **首选**：直接用 `curl` 调用 HTTP API `/api/v1/publish`（设置 120 秒超时）
2. **备选**：尝试 MCP 工具 `publish_content`（可能超时，仅适合无图或极小图片场景）
3. **兜底**：准备好完整文案，让用户手动发布

### 图片路径处理经验

1. **避免中文路径**：将图片先复制到 `/tmp/` 下，使用纯英文路径
   ```bash
   cp "/Users/user/中文目录/image.png" /tmp/image.png
   ```
2. **图片大小**：建议 < 5MB，实测 400KB 左右的 PNG 可正常上传
3. **图片格式**：支持 png/jpg/jpeg/webp
4. **至少 1 张图片**：小红书图文必须有配图

---

## 核心功能

### 1. 搜索与发现

#### search_feeds - 搜索笔记
搜索小红书内容，支持多维度筛选。

**参数**：
- `keyword` (必填): 搜索关键词
- `filters` (可选): 筛选条件
  - `sort_by`: 综合 | 最新 | 最多点赞 | 最多评论 | 最多收藏
  - `note_type`: 不限 | 视频 | 图文
  - `publish_time`: 不限 | 一天内 | 一周内 | 半年内
  - `location`: 不限 | 同城 | 附近
  - `search_scope`: 不限 | 已看过 | 未看过 | 已关注

**示例**：
```
搜索 "AI" 相关的最新笔记：
search_feeds(keyword="AI", filters={sort_by:"最新"})

搜索最多点赞的视频：
search_feeds(keyword="ChatGPT", filters={sort_by:"最多点赞", note_type:"视频"})
```

#### get_feed_detail - 获取笔记详情
获取笔记的完整信息：内容、图片、互动数据（点赞/收藏/评论数）、评论列表。

**参数**：
- `feed_id` (必填): 笔记 ID（从搜索结果获取）
- `xsec_token` (必填): 访问令牌（从搜索结果获取）
- `load_all_comments` (可选): 是否加载全部评论（默认仅前 10 条）

---

### 2. 内容发布

#### 发布工作流（优化版）

**步骤 1：检查登录状态**
```
调用 MCP: xiaohongshu.check_login_status
```
> 注意：check_login_status 是轻量查询，MCP 工具不会超时，可以正常使用。

如果未登录，执行登录流程（见下方「登录二维码获取」章节）。

**步骤 2：准备图片**
```bash
# 将图片复制到 /tmp 下，避免中文路径问题
cp "/原始/中文路径/image.png" /tmp/image.png
# 验证图片存在且大小合理
ls -la /tmp/image.png
```

**步骤 3：通过 HTTP API 发布**
```bash
curl -s -w "\nHTTP_CODE:%{http_code}\nTIME:%{time_total}s\n" \
  --max-time 120 \
  -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "标题",
    "content": "正文",
    "images": ["/tmp/image.png"],
    "tags": ["标签1", "标签2"]
  }'
```

**步骤 4：验证发布结果**
```bash
# 检查服务日志确认发布状态
tail -20 /Users/voidzhang/Documents/workspace/xiaohongshu-mcp/mcp_server.log
```
> 日志中出现 `POST /api/v1/publish 200` 且耗时 30-50 秒表示发布成功。

#### 登录二维码获取（聊天窗口无法显示时）

> ⚠️ **已知问题**：MCP 工具 `get_login_qrcode` 返回的 Base64 图片在聊天窗口中无法正常渲染。
> 解决方案：通过 HTTP API 获取二维码数据，生成 HTML 文件后在浏览器中打开扫码。

**一键获取二维码并在浏览器中打开**：
```bash
curl -s http://localhost:18060/api/v1/login/qrcode | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
img_data = data['data']['img']
html = f'''<!DOCTYPE html>
<html>
<head><title>小红书登录二维码</title></head>
<body style=\"display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#f5f5f5;flex-direction:column\">
<h2 style=\"color:#333;font-family:sans-serif\">请用小红书 App 扫码登录</h2>
<img src=\"{img_data}\" style=\"width:300px;height:300px;border:2px solid #ddd;border-radius:8px\" />
<p style=\"color:#999;font-family:sans-serif;margin-top:16px\">二维码有效期约 4 分钟，过期请重新获取</p>
</body>
</html>'''
with open('/Users/voidzhang/Documents/workspace/AIAgent/qrcode.html', 'w') as f:
    f.write(html)
print('HTML file generated successfully')
" && open /Users/voidzhang/Documents/workspace/AIAgent/qrcode.html
```

**工作原理**：
1. 调用 HTTP API `GET /api/v1/login/qrcode` 获取 Base64 编码的二维码图片（需等待约 8-10 秒，因为后端要启动浏览器加载小红书页面）
2. 将 Base64 数据嵌入 HTML 的 `<img src="data:image/png;base64,...">` 中
3. 生成 `qrcode.html` 文件并用 `open` 命令在浏览器中打开
4. 用户用小红书 App 扫码后，服务端自动保存 Cookie

**注意事项**：
- 命令可能因为等待浏览器加载而被放到后台执行，属于正常现象
- 二维码有效期约 **4 分钟**，过期需重新执行命令
- 扫码成功后，通过 `check_login_status` 确认登录状态
- API 返回的 JSON 结构：`{"success": true, "data": {"timeout": "4m0s", "is_logged_in": false, "img": "data:image/png;base64,..."}, "message": "获取登录二维码成功"}`

---

#### publish_content 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 标题（≤20 个中文字或英文单词） |
| `content` | string | ✅ | 正文内容（不包含 # 开头的标签） |
| `images` | string[] | ✅ | 图片路径列表（至少 1 张，推荐用 /tmp 下的纯英文路径） |
| `tags` | string[] | ❌ | 话题标签列表，如 ["AI", "ChatGPT"] |
| `is_original` | boolean | ❌ | 是否声明原创 |
| `visibility` | string | ❌ | 可见范围（公开可见 / 仅自己可见 / 仅互关好友可见） |
| `schedule_at` | string | ❌ | 定时发布时间（ISO8601 格式） |
| `products` | string[] | ❌ | 商品关键词列表 |

---

### 3. HTTP API 完整参考

xiaohongshu-mcp 服务的 REST API 路由（端口 18060）：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/api/v1/login/status` | 检查登录状态 |
| GET | `/api/v1/login/qrcode` | 获取登录二维码 |
| DELETE | `/api/v1/login/cookies` | 删除 cookies |
| POST | `/api/v1/publish` | 发布图文 |
| POST | `/api/v1/publish_video` | 发布视频 |
| GET | `/api/v1/feeds/list` | 获取首页 Feeds |
| GET/POST | `/api/v1/feeds/search` | 搜索笔记 |
| POST | `/api/v1/feeds/detail` | 获取笔记详情 |
| POST | `/api/v1/user/profile` | 获取用户主页 |

> **重要**：对于耗时操作（发布图文/视频），优先使用 HTTP API + curl，避免 MCP 超时。
> 对于轻量查询（登录状态、搜索、详情），可以正常使用 MCP 工具。

---

### 4. 互动操作

#### like_feed - 点赞/取消点赞
为指定笔记点赞或取消点赞。

#### favorite_feed - 收藏/取消收藏
收藏指定笔记或取消收藏。

#### post_comment_to_feed - 发表评论
为笔记发表一级评论。

**参数**：
- `feed_id` (必填): 笔记 ID
- `xsec_token` (必填): 访问令牌
- `content` (必填): 评论内容

---

## 自动化场景

### 场景 1：热点内容监控

用户说："帮我找出小红书上关于 AI 的最热门笔记"

**工作流程**：
1. 调用 `search_feeds(keyword="AI", filters={sort_by:"最多点赞"})`
2. 对每个结果调用 `get_feed_detail()` 获取详细数据
3. 计算热度分数：`(点赞×1 + 收藏×1.5 + 评论×2 + 分享×3) / (发布时间小时数 + 1)^0.8`
4. 按热度排序返回 Top 10

### 场景 2：自动发布（优化版）

用户说："把这篇文章发到小红书"

**工作流程**：
1. 检查登录状态（MCP 工具）
2. 提取文章标题（压缩到 ≤20 字）
3. 提取正文内容（移除 # 标签到 tags 数组）
4. 准备图片（复制到 /tmp，纯英文路径）
5. **通过 curl 调用 HTTP API 发布**（120 秒超时）
6. 检查服务日志确认发布成功

### 场景 3：批量互动

用户说："给搜索结果的前 5 条笔记点赞并评论"

**工作流程**：
1. 调用 `search_feeds()` 获取列表
2. 遍历前 5 条：
   - 调用 `like_feed()`
   - 调用 `post_comment_to_feed()`

---

## 注意事项

### 1. MCP 工具 vs HTTP API 选择指南

| 操作 | 推荐方式 | 原因 |
|------|----------|------|
| 检查登录状态 | MCP 工具 | 轻量查询，秒级响应 |
| **获取登录二维码** | **HTTP API (curl) + HTML** | **MCP 返回的 Base64 图片在聊天窗口无法渲染，需通过 API 获取后生成 HTML 在浏览器打开** |
| 搜索笔记 | MCP 工具 | 查询操作，不涉及浏览器上传 |
| 获取笔记详情 | MCP 工具 | 查询操作 |
| **发布图文** | **HTTP API (curl)** | **浏览器操作耗时 30-50 秒，MCP 必超时** |
| **发布视频** | **HTTP API (curl)** | **同上** |
| 点赞/收藏 | MCP 工具 | 轻量操作 |
| 评论 | MCP 工具 | 轻量操作 |

### 2. 热度计算公式
```
热度分数 = (点赞×1.0 + 收藏×1.5 + 评论×2.0 + 分享×3.0) 
          / (发布时间小时数 + 1)^0.8
```

### 3. 标题长度限制
小红书标题最多 **20 个中文字或英文单词**。计算方式：
- 中文/全角字符：计 2
- 英文/半角字符：计 1

### 4. API 限流
小红书平台有请求频率限制，批量操作时建议：
- 搜索：每次间隔 2-3 秒
- 发布：每次间隔 10-15 秒
- 点赞/评论：每次间隔 3-5 秒

### 5. Cookie 过期
如果 Cookie 过期，需要重新登录：

**方式 1（推荐）：通过 HTTP API 获取二维码 HTML 扫码登录**
```bash
curl -s http://localhost:18060/api/v1/login/qrcode | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
img_data = data['data']['img']
html = f'''<!DOCTYPE html>
<html>
<head><title>小红书登录二维码</title></head>
<body style=\"display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#f5f5f5;flex-direction:column\">
<h2 style=\"color:#333;font-family:sans-serif\">请用小红书 App 扫码登录</h2>
<img src=\"{img_data}\" style=\"width:300px;height:300px;border:2px solid #ddd;border-radius:8px\" />
<p style=\"color:#999;font-family:sans-serif;margin-top:16px\">二维码有效期约 4 分钟，过期请重新获取</p>
</body>
</html>'''
with open('/Users/voidzhang/Documents/workspace/AIAgent/qrcode.html', 'w') as f:
    f.write(html)
print('HTML file generated successfully')
" && open /Users/voidzhang/Documents/workspace/AIAgent/qrcode.html
```

**方式 2：如需彻底重置登录状态**
```bash
# 先删除旧 cookies
curl -s -X DELETE http://localhost:18060/api/v1/login/cookies
# 再获取新二维码（同方式 1）
```

### 6. 发布后验证
发布后通过服务日志确认结果：
```bash
tail -20 /Users/voidzhang/Documents/workspace/xiaohongshu-mcp/mcp_server.log
```
关键日志标志：
- `POST /api/v1/publish 200` + 耗时 30-50s → ✅ 发布成功
- `图片已提交上传` → 图片上传中
- `成功点击标签联想选项 tag=xxx` → 标签添加成功
- `检查标题长度：通过` → 标题验证通过

### 7. 避免重复发布
HTTP API 调用可能因为命令被放到后台执行而看不到返回值。务必通过日志确认是否已发布成功，避免重复调用导致发布多篇相同内容。

### 8. 发布后禁止自动重试（强制规则）
**铁律：发布操作只执行一次，无论结果如何（成功、失败、超时），都必须等待用户手动确认后才能决定下一步。**

- ❌ 禁止：发布超时后自动重试
- ❌ 禁止：发布报错后自动重试
- ✅ 正确做法：发布一次后，返回结果（或超时提示），等待用户确认
- ✅ 超时时提醒用户："请去小红书 App 检查是否已发布成功，确认后告诉我是否需要重新发布"

**背景**：MCP 工具和 HTTP API 都可能因为浏览器操作耗时而超时，但超时≠发布失败。自动重试会导致发布重复内容。

---

## 相关文档

- 项目位置: `/Users/voidzhang/Documents/workspace/AIAgent`
- MCP 服务源码: `/Users/voidzhang/Documents/workspace/xiaohongshu-mcp`
- MCP 端点: `http://localhost:18060/mcp`
- HTTP API: `http://localhost:18060/api/v1/`
- 服务日志: `/Users/voidzhang/Documents/workspace/xiaohongshu-mcp/mcp_server.log`
- 热度计算说明: `1_热点监控/docs/xiaohongshu_hot_metrics.md`
