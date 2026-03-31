---
description: AI Agent 项目版本发布和部署工具。当用户需要发布新版本、部署到服务器、回滚版本、查看发布流程时使用此 Skill。触发关键词包括：发版、发布、部署、打包、release、deploy、版本管理、回滚。
globs: **/*.sh,**/*.yml,.github/**/*
version: 1.0.0
alwaysApply: false
---

# AI Agent 版本发布和部署 Skill

## 🎯 Skill 用途

当用户提到以下需求时，使用此 Skill：
- 发布新版本
- 部署到服务器
- 版本回滚
- 查看发布流程
- 打包项目
- 配置 CI/CD

## 📦 核心工具

### 1️⃣ 本地发版脚本：`release.sh`

**用法**：
```bash
./release.sh 1.0.0 "feat: 新增趣味测试分析功能"
```

**功能**：
- ✅ 检查工作区状态
- ✅ 运行测试（如果有）
- ✅ 更新版本号到 `common/__version__.py`
- ✅ 打包项目（排除缓存、日志等）
- ✅ 提交代码并创建 Git Tag
- ✅ 推送到 GitHub，触发 Actions

**参数**：
- `VERSION`: 版本号（如 `1.0.0` 或 `v1.0.0`）
- `MESSAGE`: 更新说明（建议使用 Conventional Commits 格式）

---

### 2️⃣ 服务器部署脚本：`deploy.sh`

**用法**：
```bash
# 部署指定版本
./deploy.sh v1.0.0

# 部署最新版本
./deploy.sh latest
```

**功能**：
- ✅ 备份当前版本到 `/var/www/backups/`
- ✅ 从 GitHub Release 下载构建产物
- ✅ 解压并部署，保留 `.env`、`data/`、`logs/`
- ✅ 安装 Python 依赖（虚拟环境）
- ✅ 执行数据库初始化
- ✅ 重启服务（systemd/supervisor/PM2）
- ✅ 记录部署日志

**配置**（需修改脚本中的变量）：
```bash
REPO="YOUR_USERNAME/AIAgent"         # GitHub 仓库
DEPLOY_DIR="/var/www/aiagent"        # 部署目录
BACKUP_DIR="/var/www/backups"        # 备份目录
```

---

### 3️⃣ GitHub Actions 工作流：`.github/workflows/release.yml`

**触发条件**：推送 `v*` 格式的 Tag（如 `v1.0.0`）

**自动执行**：
1. 检出代码
2. 设置 Python 环境
3. 安装依赖并运行测试
4. 更新版本号到 `common/__version__.py`
5. 打包项目为 `aiagent-v1.0.0.tar.gz`
6. 生成 CHANGELOG（从 commit 提取，按类型分类）
7. 创建 GitHub Release 并上传构建产物
8. 上传到 Artifacts（保留 90 天）
9. 可选：发送企业微信通知

**CHANGELOG 自动分类**：
- ✨ 新增功能：`feat:` 开头的 commit
- 🐛 Bug 修复：`fix:` 开头的 commit
- 📝 其他变更：其他 commit

---

## 🚀 使用场景

### 场景 1：快速发版

**用户说**：
- "帮我发布一个新版本"
- "打包并发布到 GitHub"
- "准备发 v1.0.0"

**你应该**：
1. 确认版本号和更新说明
2. 执行 `./release.sh <版本号> "<更新说明>"`
3. 等待 GitHub Actions 完成
4. 提示用户可以部署了

**示例**：
```bash
# 确认当前状态
git status
python main.py status

# 执行发版
./release.sh 1.0.0 "feat: 新增趣味测试分析功能"

# 查看 Actions 进度
# https://github.com/YOUR_USERNAME/AIAgent/actions
```

---

### 场景 2：服务器部署

**用户说**：
- "部署到服务器"
- "更新生产环境"
- "发布 v1.0.0 到 OpenClaw"

**你应该**：
1. 确认版本号
2. 在服务器上执行 `./deploy.sh v1.0.0`
3. 验证部署结果

**示例**：
```bash
# SSH 到服务器
ssh user@your-server

# 执行部署
cd /path/to/aiagent
./deploy.sh v1.0.0

# 验证部署
python main.py status
python main.py funtest --demo
```

---

### 场景 3：版本回滚

**用户说**：
- "回滚到上一个版本"
- "部署出问题了，恢复旧版本"
- "回退到 v1.0.0"

**你应该**：
```bash
# 方式 1：重新部署旧版本
./deploy.sh v1.0.0

# 方式 2：从备份恢复
sudo systemctl stop aiagent.service
rm -rf /var/www/aiagent/*
cp -r /var/www/backups/aiagent_backup_YYYYMMDD_HHMMSS/* /var/www/aiagent/
sudo systemctl start aiagent.service
```

---

### 场景 4：查看发布历史

**用户说**：
- "有哪些版本"
- "最新版本是什么"
- "查看发布记录"

**你应该**：
```bash
# 查看所有 tags
git tag -l

# 查看最新 tag
git describe --tags --abbrev=0

# 查看 tag 详情
git show v1.0.0

# 查看两个版本之间的变更
git log v0.1.0..v1.0.0 --oneline
```

---

## 📋 版本管理规范

### 语义化版本号

```
v主版本.次版本.修订号

v1.0.0 → v1.0.1 → v1.1.0 → v2.0.0
  │        │        │        │
  │        │        │        └─ 不兼容的 API 变更
  │        │        └────────── 向下兼容的功能新增
  │        └───────────────────── 向下兼容的问题修复
  └────────────────────────────── 首个稳定版本
```

### Commit 消息规范（Conventional Commits）

```
<类型>(<范围>): <简短描述>

[可选的正文]

[可选的脚注]
```

**类型**：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链

**示例**：
```bash
feat(funtest): 新增趣味测试分析模块

- 集成小红书 MCP
- 实现关键词触发
- 生成爆款选题报告

Closes #123
```

---

## 🔧 首次配置

### 1. 赋予脚本执行权限

```bash
chmod +x release.sh deploy.sh
```

### 2. 修改配置

**`release.sh` 第 79 行**：
```bash
echo "   https://github.com/YOUR_USERNAME/AIAgent/actions"
```
替换为你的 GitHub 仓库地址。

**`deploy.sh` 第 8-10 行**：
```bash
REPO="YOUR_USERNAME/AIAgent"         # 替换为你的仓库
DEPLOY_DIR="/var/www/aiagent"        # 配置部署目录
BACKUP_DIR="/var/www/backups"        # 配置备份目录
```

### 3. 配置服务器服务

创建 systemd 服务（`/etc/systemd/system/aiagent.service`）：

```ini
[Unit]
Description=AI Agent Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/aiagent
Environment="PATH=/var/www/aiagent/venv/bin"
ExecStart=/var/www/aiagent/venv/bin/python main.py workflow --daily
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable aiagent.service
sudo systemctl start aiagent.service
```

### 4. 上传部署脚本到服务器

```bash
scp deploy.sh user@your-server:/path/to/aiagent/
ssh user@your-server "chmod +x /path/to/aiagent/deploy.sh"
```

---

## 🎯 完整发布流程示例

### 开发 → 发布 → 部署

```bash
# 1. 开发新功能
git checkout -b feature/new-module
# ... 开发 ...
git commit -m "feat: 新增功能模块"

# 2. 合并到主分支
git checkout main
git merge feature/new-module

# 3. 运行测试（如果有）
pytest tests/ -v

# 4. 一键发版
./release.sh 1.0.0 "feat: 新增功能模块"

# ↓ GitHub Actions 自动执行（~2 分钟）
#   - 安装依赖
#   - 运行测试
#   - 打包项目
#   - 创建 Release

# 5. 在服务器部署
ssh user@your-server
cd /path/to/aiagent
./deploy.sh v1.0.0

# 6. 验证部署
python main.py status
```

**总耗时**：约 3-5 分钟 🚀

---

## 💡 常见问题处理

### Q1: GitHub Actions 构建失败

**检查**：
```bash
# 1. 检查 requirements.txt
pip install -r requirements.txt

# 2. 本地测试
pytest tests/ -v

# 3. 查看 Actions 日志
# https://github.com/YOUR_USERNAME/AIAgent/actions
```

### Q2: 部署后服务无法启动

**检查**：
```bash
# 1. 查看服务状态
sudo systemctl status aiagent.service

# 2. 查看日志
sudo journalctl -u aiagent.service -f

# 3. 查看部署日志
tail -f /var/log/aiagent-deploy.log

# 4. 检查环境变量
cat /var/www/aiagent/.env

# 5. 手动测试
cd /var/www/aiagent
source venv/bin/activate
python main.py status
```

### Q3: 需要紧急回滚

**最快方式**：
```bash
# 从备份恢复（~30 秒）
sudo systemctl stop aiagent.service
rm -rf /var/www/aiagent/*
LATEST_BACKUP=$(ls -t /var/www/backups/ | head -1)
cp -r /var/www/backups/$LATEST_BACKUP/* /var/www/aiagent/
sudo systemctl start aiagent.service
```

---

## 📊 项目文件结构

```
AIAgent/
├── .github/
│   └── workflows/
│       └── release.yml          # GitHub Actions 工作流
├── common/
│   └── __version__.py           # 版本号文件
├── release.sh                   # 本地发版脚本
├── deploy.sh                    # 服务器部署脚本
├── RELEASE_WORKFLOW.md          # 发布流程文档
└── requirements.txt             # Python 依赖
```

---

## 🚀 快速命令参考

```bash
# 发布新版本
./release.sh 1.0.0 "feat: 新功能"

# 部署到服务器
./deploy.sh v1.0.0

# 查看版本
git describe --tags

# 查看变更
git log v0.1.0..v1.0.0 --oneline

# 回滚
./deploy.sh v0.9.0

# 验证
python main.py status
```

---

## 📝 总结

这套工具提供了：
- ✅ **一键发版**：自动化测试、打包、推送
- ✅ **自动构建**：GitHub Actions 无需本地构建
- ✅ **快速部署**：从 Release 拉取，自动备份回滚
- ✅ **规范管理**：语义化版本、Conventional Commits
- ✅ **安全可靠**：备份机制、服务重启、日志记录

全流程耗时 **3-5 分钟**，让发版和部署变得简单高效！🎉
