# AIAgent 项目 Skills

这是 AIAgent 项目专属的 Skills 目录。CodeBuddy 会在当前项目中自动加载这些 Skills。

## 已有 Skills

### xiaohongshu-automation
小红书自动化技能，提供：
- 🔍 搜索与发现（search_feeds, get_feed_detail, user_profile）
- 📝 内容发布（publish_content, publish_with_video）
- 💬 互动操作（like_feed, favorite_feed, post_comment_to_feed）
- 👤 账号管理（check_login_status, delete_cookies）

**使用场景**：
- 热点内容监控与抓取
- 自动发布图文/视频
- 批量点赞/评论/收藏
- 竞品分析

**前置条件**：
- xiaohongshu-mcp 服务已启动（端口 18060）
- 已登录小红书账号

**快速测试**：
```
帮我搜索小红书上关于 "AI" 的最多点赞笔记
```

### scp-upload
SCP 上传文件到服务器，提供：
- 📤 通过 sshpass + SCP 上传文件到 microlab.top 服务器
- 🔧 上传后远程执行命令（赋权限、重启服务等）

**触发关键词**：上传到服务器、scp、传到服务器、部署脚本到服务器

---

### aiagent-release-deploy
AI Agent 主项目（Python 后端）版本发布和部署工具。

**触发关键词**：发版、发布、部署、打包、release、deploy

---

### pawmbti-release
PawMBTI 网站打包发版 Skill，提供：
- 🏗️ 构建前端项目（npm run build）
- 📦 升级 package.json 版本号
- 🔖 Git 提交、打 Tag、推送到 GitHub
- 🚀 创建 GitHub Release
- 🌐 可选部署到线上服务器

**触发关键词**：打包上传、打包发版、上传到 GitHub、升级 release、更新版本、pawmbti 发版

**快速测试**：
```
帮我把 pawmbti 打包发版上传到 GitHub
```

---

### trend-analyst
选题分析 Skill，分析小红书热度、选题调研、生成分析报告。

**触发关键词**：选题分析、热点分析、趋势分析、爆款选题、小红书分析

---

## Skill 开发指南

### 创建新 Skill

1. 在此目录下创建文件夹（如 `my-skill/`）
2. 创建 `SKILL.md` 文件（必需）
3. 添加 YAML frontmatter：
```yaml
---
name: my-skill
description: Skill 的描述和使用场景
---
```

### 目录结构

```
.codebuddy/skills/
├── README.md
└── xiaohongshu-automation/
    └── SKILL.md
```

### 与全局 Skills 的区别

| 项目 | 项目级别 Skills | 全局 Skills |
|------|----------------|-------------|
| 位置 | `<项目>/.codebuddy/skills/` | `~/.codebuddy/skills/` |
| 作用域 | 仅当前项目 | 所有项目 |
| 优先级 | 高（优先加载） | 低 |
| 适用场景 | 项目特定功能 | 通用功能 |

---

## 相关文档

- [Agent Skills Spec](https://github.com/anthropics/anthropic-skills)
- [AIAgent 项目文档](../README.md)
- [小红书 MCP 文档](https://github.com/xpzouying/xiaohongshu-mcp)
