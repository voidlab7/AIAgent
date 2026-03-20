# AI Agent 发布工具使用指南

## 📦 工具概览

本项目提供完整的版本发布和部署自动化工具，包括：

| 工具 | 文件 | 用途 |
|------|------|------|
| 🚀 发版脚本 | `release.sh` | 本地一键发版（测试、打包、推送） |
| 📤 部署脚本 | `deploy.sh` | 服务器一键部署（下载、安装、重启） |
| 🧪 测试打包 | `test_build.sh` | 测试打包流程（不推送） |
| 🔍 验证工具 | `verify_release.sh` | 验证打包产物 |
| 🤖 自动构建 | `.github/workflows/release.yml` | GitHub Actions 自动化 |
| 📚 文档 | `RELEASE_WORKFLOW.md` | 详细工作流文档 |
| 🎯 Skill | `.codebuddy/skills/aiagent-release-deploy.md` | CodeBuddy 集成 |

---

## 🚀 快速开始

### 1. 首次配置

```bash
# 1. 赋予脚本执行权限（已完成）
chmod +x release.sh deploy.sh test_build.sh verify_release.sh

# 2. 修改配置
# - release.sh: 第 79 行，替换 GitHub 仓库地址
# - deploy.sh: 第 8-10 行，配置仓库和部署路径

# 3. 上传部署脚本到服务器
scp deploy.sh user@your-server:/path/to/aiagent/
```

### 2. 测试打包流程

```bash
# 测试打包（不会推送到 GitHub）
./test_build.sh 0.1.0-test

# 验证打包产物
./verify_release.sh aiagent-v0.1.0-test.tar.gz

# 清理测试文件
rm -f aiagent-v0.1.0-test.tar.gz aiagent-v0.1.0-test-安装说明.txt
```

### 3. 正式发版

```bash
# 一键发版
./release.sh 1.0.0 "feat: 新增趣味测试分析功能"

# 等待 GitHub Actions 构建（约 2 分钟）
# 访问: https://github.com/YOUR_USERNAME/AIAgent/actions

# 查看 Release
# 访问: https://github.com/YOUR_USERNAME/AIAgent/releases
```

### 4. 服务器部署

```bash
# SSH 到服务器
ssh user@your-server

# 部署指定版本
cd /path/to/aiagent
./deploy.sh v1.0.0

# 或部署最新版本
./deploy.sh latest
```

---

## 📋 命令参考

### release.sh - 本地发版

```bash
# 基本用法
./release.sh <版本号> "<更新说明>"

# 示例
./release.sh 1.0.0 "feat: 新增趣味测试分析功能"
./release.sh 1.0.1 "fix: 修复数据库连接问题"
./release.sh 1.1.0 "feat: 新增热点监控模块"
```

**自动完成**：
- ✅ 检查工作区状态
- ✅ 运行测试（如果有）
- ✅ 更新版本号
- ✅ 打包项目
- ✅ 提交代码 + 创建 Tag
- ✅ 推送到 GitHub
- ✅ 触发 GitHub Actions

---

### deploy.sh - 服务器部署

```bash
# 部署指定版本
./deploy.sh v1.0.0

# 部署最新版本
./deploy.sh latest
```

**自动完成**：
- ✅ 备份当前版本
- ✅ 从 GitHub Release 下载
- ✅ 解压并部署
- ✅ 保留配置和数据
- ✅ 安装依赖
- ✅ 重启服务

**配置项**（在脚本中修改）：
```bash
REPO="YOUR_USERNAME/AIAgent"         # GitHub 仓库
DEPLOY_DIR="/var/www/aiagent"        # 部署目录
BACKUP_DIR="/var/www/backups"        # 备份目录
```

---

### test_build.sh - 测试打包

```bash
# 测试打包（不推送）
./test_build.sh [版本号]

# 示例
./test_build.sh 0.1.0-test
./test_build.sh         # 默认 0.0.1-test
```

**检查项目**：
- ✅ 项目结构
- ✅ Python 环境
- ✅ 依赖安装
- ✅ 语法检查
- ✅ 测试运行
- ✅ 主程序
- ✅ 打包验证

---

### verify_release.sh - 验证打包产物

```bash
# 验证压缩包
./verify_release.sh <压缩包路径>

# 示例
./verify_release.sh aiagent-v1.0.0.tar.gz
```

**验证项目**：
- ✅ 文件完整性
- ✅ 目录结构
- ✅ 依赖安装
- ✅ 模块导入
- ✅ 程序运行
- ✅ 脚本权限

---

## 🔄 完整工作流

### 开发 → 发布 → 部署

```bash
# 1️⃣ 开发新功能
git checkout -b feature/new-module
# ... 编码 ...
git commit -m "feat: 新增功能模块"

# 2️⃣ 合并到主分支
git checkout main
git merge feature/new-module

# 3️⃣ 测试打包（可选）
./test_build.sh 1.0.0-test
./verify_release.sh aiagent-v1.0.0-test.tar.gz

# 4️⃣ 正式发版
./release.sh 1.0.0 "feat: 新增功能模块"

# ⏳ GitHub Actions 自动构建（约 2 分钟）

# 5️⃣ 服务器部署
ssh user@your-server
cd /path/to/aiagent
./deploy.sh v1.0.0

# 6️⃣ 验证部署
python main.py status
python main.py funtest --demo
```

**总耗时**：约 3-5 分钟 🚀

---

## 📊 版本管理

### 语义化版本号

```
v主版本.次版本.修订号

示例：
v0.1.0 → v0.2.0 → v1.0.0 → v1.1.0 → v2.0.0
  │        │        │        │        │
  │        │        │        │        └─ 不兼容的 API 变更
  │        │        │        └────────── 新功能（向下兼容）
  │        │        └───────────────────── 首个稳定版本
  │        └────────────────────────────── 新功能
  └─────────────────────────────────────── 初始开发版本
```

### Commit 消息规范

```bash
# 格式
<类型>(<范围>): <简短描述>

# 类型
feat:     新功能
fix:      Bug 修复
docs:     文档更新
style:    代码格式
refactor: 重构
perf:     性能优化
test:     测试
chore:    构建/工具

# 示例
feat(funtest): 新增趣味测试分析模块
fix(database): 修复数据库连接超时问题
docs: 更新 API 文档
perf(hotspot): 优化热点抓取性能
```

---

## 🔧 高级配置

### GitHub Actions 通知

在 `.github/workflows/release.yml` 最后添加企业微信通知：

```yaml
- name: Send WeChat notification
  if: success()
  run: |
    curl -X POST ${{ secrets.WECOM_WEBHOOK }} \
      -H 'Content-Type: application/json' \
      -d '{
        "msgtype": "markdown",
        "markdown": {
          "content": "## 🚀 AI Agent 新版本发布\n\n**版本**: ${{ github.ref_name }}\n\n[点击下载](https://github.com/${{ github.repository }}/releases/tag/${{ github.ref_name }})"
        }
      }'
```

在 GitHub 仓库设置中添加 Secret：`WECOM_WEBHOOK`

### systemd 服务配置

创建 `/etc/systemd/system/aiagent.service`：

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
sudo systemctl status aiagent.service
```

---

## 🐛 故障排查

### GitHub Actions 构建失败

```bash
# 1. 检查依赖
pip install -r requirements.txt

# 2. 本地测试
pytest tests/ -v

# 3. 查看 Actions 日志
# https://github.com/YOUR_USERNAME/AIAgent/actions
```

### 部署后服务无法启动

```bash
# 1. 查看服务状态
sudo systemctl status aiagent.service

# 2. 查看日志
sudo journalctl -u aiagent.service -f
tail -f /var/log/aiagent-deploy.log

# 3. 检查环境
cat /var/www/aiagent/.env

# 4. 手动测试
cd /var/www/aiagent
source venv/bin/activate
python main.py status
```

### 紧急回滚

```bash
# 方式 1: 重新部署旧版本（推荐）
./deploy.sh v1.0.0

# 方式 2: 从备份恢复（最快）
sudo systemctl stop aiagent.service
rm -rf /var/www/aiagent/*
LATEST_BACKUP=$(ls -t /var/www/backups/ | head -1)
cp -r /var/www/backups/$LATEST_BACKUP/* /var/www/aiagent/
sudo systemctl start aiagent.service
```

---

## 📚 相关文档

- **详细工作流**：[RELEASE_WORKFLOW.md](./RELEASE_WORKFLOW.md)
- **项目文档**：[README.md](./README.md)
- **Skill 文档**：[.codebuddy/skills/aiagent-release-deploy.md](./.codebuddy/skills/aiagent-release-deploy.md)

---

## ✅ 测试验证

### 测试结果

```bash
# 测试打包流程
./test_build.sh 0.1.0-test

📦 构建产物: aiagent-v0.1.0-test.tar.gz (41M)

🔍 验证结果：
  - 项目结构: ✅
  - Python 环境: ✅
  - 依赖安装: ✅
  - 语法检查: ✅
  - 主程序运行: ✅
  - 压缩包验证: ✅

# 验证打包产物
./verify_release.sh aiagent-v0.1.0-test.tar.gz

📋 验证结果：
  - 文件完整性: ✅
  - 目录结构: ✅
  - Python 依赖: ✅
  - 模块导入: ✅
  - 主程序运行: ✅

✅ 所有测试通过！
```

---

## 🎯 总结

这套工具提供了：

- ✅ **一键发版**：自动化测试、打包、推送
- ✅ **自动构建**：GitHub Actions 云端构建
- ✅ **快速部署**：从 Release 拉取，自动备份
- ✅ **测试验证**：完整的测试和验证流程
- ✅ **规范管理**：语义化版本、Conventional Commits
- ✅ **安全可靠**：备份机制、服务重启、日志记录

**全流程耗时 3-5 分钟**，让发版和部署变得简单高效！🎉

---

## 📞 支持

- 问题反馈：[GitHub Issues](https://github.com/YOUR_USERNAME/AIAgent/issues)
- 文档：[完整文档](./RELEASE_WORKFLOW.md)
- Skill：使用 CodeBuddy 触发 `发版`、`部署`、`打包` 等关键词
