# AI Agent 版本发布工作流

## 🎯 完整流程

### 推荐方案：GitHub Actions 自动化

```
本地开发 → 提交代码 → 打 Tag → 推送
                              ↓
                    GitHub Actions 自动构建
                              ↓
                    创建 Release + 上传构建产物
                              ↓
                    服务器 OpenClaw 拉取部署
```

---

## 📋 一、本地操作

### 方式 1️⃣：使用自动化脚本（推荐）

```bash
# 一键发版（测试、打包、打 Tag、推送）
./release.sh 1.0.0 "feat: 新增趣味测试分析功能"
```

**脚本自动完成**：
- ✅ 检查工作区状态
- ✅ 运行测试（如果有）
- ✅ 更新版本号
- ✅ 打包项目
- ✅ 提交代码 + 创建 Tag
- ✅ 推送到 GitHub
- ✅ 触发 GitHub Actions

---

### 方式 2️⃣：手动操作

```bash
# 1. 运行测试
pytest tests/ -v

# 2. 更新版本号
echo "__version__ = '1.0.0'" > common/__version__.py

# 3. 提交代码
git add .
git commit -m "feat: 新增趣味测试分析功能"

# 4. 打 Tag
git tag -a v1.0.0 -m "feat: 新增趣味测试分析功能

## 新增
- 趣味测试分析模块
- 小红书 MCP 集成
- 爆款选题报告生成

## 优化
- 优化数据库查询性能
- 改进关键词触发逻辑

## 修复
- 修复编码问题"

# 5. 推送
git push origin main --tags
```

---

## 🤖 二、GitHub Actions 自动构建

推送 Tag 后，GitHub Actions 自动执行：

1. ✅ 检出代码
2. ✅ 设置 Python 环境
3. ✅ 安装依赖 (`pip install -r requirements.txt`)
4. ✅ 运行测试 (`pytest`)
5. ✅ 打包项目 (`aiagent-v1.0.0.tar.gz`)
6. ✅ 生成 CHANGELOG（从 commit 提取）
7. ✅ 创建 GitHub Release 并上传压缩包

**查看构建进度**：
- https://github.com/YOUR_USERNAME/AIAgent/actions

**查看 Release**：
- https://github.com/YOUR_USERNAME/AIAgent/releases

---

## 🚀 三、服务器部署（OpenClaw）

### 方式 1️⃣：一键部署脚本（推荐）

```bash
# 在服务器上执行
./deploy.sh v1.0.0

# 或部署最新版本
./deploy.sh latest
```

**脚本自动完成**：
- ✅ 备份当前版本
- ✅ 从 GitHub Release 下载构建产物
- ✅ 解压到部署目录
- ✅ 保留 .env、data/ 和 logs/
- ✅ 安装 Python 依赖
- ✅ 执行数据库迁移
- ✅ 重启服务（systemd/supervisor/PM2）
- ✅ 记录部署日志

---

### 方式 2️⃣：手动部署

```bash
# 1. 备份
cp -r /var/www/aiagent /var/www/backups/aiagent_$(date +%Y%m%d_%H%M%S)

# 2. 下载
wget https://github.com/YOUR_USERNAME/AIAgent/releases/download/v1.0.0/aiagent-v1.0.0.tar.gz

# 3. 解压
tar -xzf aiagent-v1.0.0.tar.gz
cd aiagent-v1.0.0

# 4. 安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. 部署
cp -r * /var/www/aiagent/
cd /var/www/aiagent

# 6. 初始化
python main.py init

# 7. 重启服务
sudo systemctl restart aiagent.service
```

---

## 🔄 四、版本回滚

### 回滚到指定版本

```bash
# 方式1：使用部署脚本
./deploy.sh v1.0.0  # 重新部署旧版本

# 方式2：从备份恢复
sudo systemctl stop aiagent.service
rm -rf /var/www/aiagent/*
cp -r /var/www/backups/aiagent_backup_20260320_120000/* /var/www/aiagent/
sudo systemctl start aiagent.service
```

---

## 📊 五、版本管理最佳实践

### 语义化版本号

```
v0.1.0 → v0.2.0 → v1.0.0 → v1.1.0 → v2.0.0
  │        │        │        │        │
  │        │        │        │        └─ 重大更新（不兼容）
  │        │        │        └────────── 新功能（向下兼容）
  │        │        └───────────────────── 首个稳定版本
  │        └────────────────────────────── 新功能
  └─────────────────────────────────────── 初始开发版本
```

### Commit 消息规范

```
feat: 新增趣味测试分析模块
fix: 修复数据库连接问题
perf: 优化热点抓取性能
docs: 更新 API 文档
test: 新增单元测试
chore: 升级依赖版本
refactor: 重构配置模块
```

### Tag 消息模板

```bash
git tag -a v1.0.0 -m "v1.0.0 - 趣味测试分析功能上线

## 新增 (Features)
- 趣味测试分析模块
- 小红书 MCP 集成
- 爆款选题报告生成
- 关键词触发功能

## 优化 (Improvements)
- 优化数据库查询性能
- 改进关键词触发逻辑
- 优化报告生成速度

## 修复 (Fixes)
- 修复中文编码问题
- 修复数据库锁问题

## 技术变更 (Technical)
- 升级到 Python 3.9
- 新增 pytest 测试框架
- 集成 GitHub Actions"
```

---

## 📦 六、项目打包说明

### 打包内容

包含：
- ✅ 所有 Python 源码
- ✅ requirements.txt
- ✅ README.md 和文档
- ✅ 配置文件示例（.env.example）

排除：
- ❌ .git/
- ❌ __pycache__/ 和 *.pyc
- ❌ cache/ 和 logs/
- ❌ data/*.db（数据库文件）
- ❌ node_modules/（如果有 web 项目）

### .gitignore 推荐配置

```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# 数据和缓存
cache/
logs/
data/*.db
*.log

# 环境配置
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Web 项目
web_site/node_modules/
web_site/dist/
```

---

## 🔔 七、自动化通知（可选）

### 企业微信机器人通知

在 `.github/workflows/release.yml` 中添加：

```yaml
- name: Send WeChat notification
  if: success()
  run: |
    curl -X POST ${{ secrets.WECOM_WEBHOOK }} \
      -H 'Content-Type: application/json' \
      -d '{
        "msgtype": "markdown",
        "markdown": {
          "content": "## 🚀 AI Agent 新版本发布\n\n**版本**: ${{ github.ref_name }}\n**提交数**: ${{ steps.changelog.outputs.COMMIT_COUNT }}\n\n[点击下载](https://github.com/${{ github.repository }}/releases/tag/${{ github.ref_name }})"
        }
      }'
```

在 GitHub 仓库设置中添加 Secret：`WECOM_WEBHOOK`

---

## 📋 八、服务配置示例

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

## 🎯 九、快速开始

### 首次设置

```bash
# 1. 赋予脚本执行权限
chmod +x release.sh deploy.sh

# 2. 配置 GitHub Actions（如果还没有）
mkdir -p .github/workflows
# 已经创建好了 .github/workflows/release.yml

# 3. 将 deploy.sh 上传到服务器
scp deploy.sh user@your-server:/path/to/aiagent/

# 4. 在服务器上配置服务（systemd/supervisor）
# 参考上面的服务配置示例

# 5. 修改脚本中的配置
# - release.sh: 第 79 行，替换 GitHub 仓库地址
# - deploy.sh: 第 8 行，替换 GitHub 仓库地址
# - deploy.sh: 第 9-10 行，配置部署和备份目录
```

### 发布第一个版本

```bash
# 1. 本地发版
./release.sh 0.1.0 "feat: 初始版本"

# 2. 等待 GitHub Actions 构建完成（约 1-2 分钟）
# 访问 https://github.com/YOUR_USERNAME/AIAgent/actions

# 3. 在服务器部署
ssh user@your-server
cd /path/to/aiagent
./deploy.sh v0.1.0

# 4. 验证部署
python main.py status
```

---

## 💡 十、常见问题

### Q1: GitHub Actions 构建失败？

**检查**：
- requirements.txt 是否包含所有依赖
- Python 版本是否正确（3.9+）
- 是否有语法错误

### Q2: 部署后服务启动失败？

**检查**：
- .env 配置是否正确
- 数据库文件是否存在
- Python 虚拟环境是否激活
- 日志文件：`tail -f /var/log/aiagent-deploy.log`

### Q3: 如何测试发布流程？

```bash
# 使用测试标签（不会触发 Actions）
git tag test-v1.0.0
git push origin test-v1.0.0

# 本地测试打包
tar -xzf aiagent-v1.0.0.tar.gz
cd aiagent-v1.0.0
pip install -r requirements.txt
python main.py status
```

---

## 🚀 十一、完整工作流示例

```bash
# 1. 开发新功能
git checkout -b feature/funtest-analyzer
# ... 开发 ...
git commit -m "feat: 新增趣味测试分析"

# 2. 合并到主分支
git checkout main
git merge feature/funtest-analyzer

# 3. 运行测试
pytest tests/ -v

# 4. 一键发版
./release.sh 0.2.0 "feat: 新增趣味测试分析功能"

# 5. 等待 GitHub Actions 构建（~2 分钟）

# 6. 服务器部署
ssh user@your-server
cd /path/to/aiagent
./deploy.sh v0.2.0

# 7. 验证部署
python main.py status
python main.py funtest --demo
```

**全流程耗时**：
- 本地构建：~30 秒
- GitHub Actions：~2 分钟
- 服务器部署：~1 分钟
- **总计**：~3.5 分钟 🚀

---

搞定！🎉
