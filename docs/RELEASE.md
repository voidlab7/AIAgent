# AIAgent 发版与部署指南

> 完整的版本发布、打包、部署流程。脚本 + CI/CD 全自动化，全流程约 3-5 分钟。

---

## 工具概览

| 工具 | 文件 | 用途 |
|------|------|------|
| 🚀 发版脚本 | `release.sh` | 本地一键发版（测试、打包、推送） |
| 📤 部署脚本 | `deploy.sh` | 服务器一键部署（下载、安装、重启） |
| 🧪 测试打包 | `test_build.sh` | 测试打包流程（不推送） |
| 🔍 验证工具 | `verify_release.sh` | 验证打包产物完整性 |
| 🤖 自动构建 | `.github/workflows/release.yml` | GitHub Actions 自动构建 Release |

---

## 快速开始

### 正式发版（推荐）

```bash
# 一键发版：测试 → 打包 → 打 Tag → 推送 → 触发 CI
./release.sh 1.0.0 "feat: 新增功能模块"

# 等待 GitHub Actions 构建完成（约 2 分钟）
# https://github.com/YOUR_USERNAME/AIAgent/actions

# 在服务器上部署
ssh user@your-server
cd /path/to/aiagent
./deploy.sh v1.0.0
```

### 测试打包（不推送）

```bash
./test_build.sh 0.1.0-test
./verify_release.sh aiagent-v0.1.0-test.tar.gz
rm -f aiagent-v0.1.0-test.tar.gz aiagent-v0.1.0-test-安装说明.txt
```

---

## 完整发布流程

```
本地开发 → 提交代码 → 打 Tag → 推送
                              ↓
                    GitHub Actions 自动构建
                              ↓
                    创建 Release + 上传 tar.gz
                              ↓
                    服务器执行 deploy.sh 部署
```

**时间线：**
- T+0min：`./release.sh` 开始发版
- T+1min：本地构建完成，代码推送到 GitHub
- T+3min：GitHub Actions 构建完，Release 创建
- T+5min：服务器部署完成 ✅

---

## 命令参考

### release.sh — 本地发版

```bash
./release.sh <版本号> "<更新说明>"

# 示例
./release.sh 1.0.0 "feat: 初始版本"
./release.sh 1.1.0 "feat: 新增热点监控模块"
./release.sh 1.0.1 "fix: 修复数据库连接问题"
```

**自动完成**：检查工作区 → 运行测试 → 更新版本号 → 打包 → 提交 + Tag → 推送到 GitHub

### deploy.sh — 服务器部署

```bash
./deploy.sh v1.0.0   # 部署指定版本
./deploy.sh latest   # 部署最新版本
```

**自动完成**：备份当前版本 → 从 GitHub Release 下载 → 解压部署 → 保留 .env/data/logs → 安装依赖 → 重启服务

**配置项**（在脚本顶部修改）：
```bash
REPO="YOUR_USERNAME/AIAgent"      # GitHub 仓库
DEPLOY_DIR="/var/www/aiagent"     # 部署目录
BACKUP_DIR="/var/www/backups"     # 备份目录
```

---

## 版本管理规范

### 语义化版本号

```
v主版本.次版本.修订号

v1.0.0 → 首个稳定版本
v1.1.0 → 新功能（向下兼容）
v1.0.1 → Bug 修复
v2.0.0 → 不兼容的重大变更
```

### Commit 消息规范

```
<类型>(<范围>): <简短描述>

feat:     新功能
fix:      Bug 修复
docs:     文档更新
refactor: 重构
perf:     性能优化
test:     测试
chore:    构建/工具
```

示例：`feat(funtest): 新增趣味测试分析模块`

---

## 故障排查

### GitHub Actions 构建失败
```bash
pip install -r requirements.txt  # 检查依赖
pytest tests/ -v                 # 本地测试
# 查看 Actions 日志：https://github.com/YOUR_USERNAME/AIAgent/actions
```

### 部署后服务无法启动
```bash
sudo systemctl status aiagent.service
sudo journalctl -u aiagent.service -f
tail -f /var/log/aiagent-deploy.log
```

### 紧急回滚
```bash
# 方式 1：重新部署旧版本（推荐）
./deploy.sh v1.0.0

# 方式 2：从备份恢复
sudo systemctl stop aiagent.service
LATEST_BACKUP=$(ls -t /var/www/backups/ | head -1)
cp -r /var/www/backups/$LATEST_BACKUP/* /var/www/aiagent/
sudo systemctl start aiagent.service
```

---

## systemd 服务配置（参考）

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

```bash
sudo systemctl daemon-reload
sudo systemctl enable aiagent.service
sudo systemctl start aiagent.service
```
