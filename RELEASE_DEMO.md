# 🚀 AI Agent 发布工具 - 快速演示

## 📦 工具列表

```bash
# 查看所有脚本
$ ls -lh *.sh
-rwxr-xr-x  deploy.sh          # 服务器部署脚本
-rwxr-xr-x  release.sh         # 本地发版脚本
-rwxr-xr-x  test_build.sh      # 测试打包脚本
-rwxr-xr-x  verify_release.sh  # 验证工具

# 查看文档
$ ls -lh *RELEASE*.md
-rw-r--r--  RELEASE_GUIDE.md    # 快速使用指南
-rw-r--r--  RELEASE_WORKFLOW.md # 完整工作流文档
```

---

## 🎬 使用演示

### 场景 1：测试打包流程

```bash
# 1. 测试打包（不推送到 GitHub）
$ ./test_build.sh 0.1.0-test

🧪 测试打包流程（版本: v0.1.0-test）
⚠️  注意：此脚本不会推送到 GitHub

📂 检查项目结构...
✅ 项目结构完整

🐍 检查 Python 环境...
✅ Python 3.9.6

📦 创建测试虚拟环境...
📥 安装依赖...
✅ 依赖安装完成

🔍 运行语法检查...
✅ 语法检查完成

🎯 测试主程序...
✅ 主程序可以正常运行

📝 更新版本号...
✅ 版本号已更新: 0.1.0-test

📦 打包项目...
  → 创建构建目录: /tmp/xxx/aiagent-v0.1.0-test
  → 复制项目文件...
✅ 打包完成: aiagent-v0.1.0-test.tar.gz (41M)

🔍 验证压缩包...
  → 检查文件结构...
  → 检查文件数量...
    文件数量: 11616
✅ 压缩包验证通过

📄 生成安装说明: aiagent-v0.1.0-test-安装说明.txt

🧹 清理测试环境...
✅ 清理完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 测试打包成功！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 构建产物：
  - aiagent-v0.1.0-test.tar.gz (41M)
  - aiagent-v0.1.0-test-安装说明.txt

🔍 验证结果：
  - 项目结构: ✅
  - Python 环境: ✅
  - 依赖安装: ✅
  - 语法检查: ✅
  - 主程序运行: ✅
  - 压缩包验证: ✅
```

### 场景 2：验证打包产物

```bash
# 2. 验证压缩包
$ ./verify_release.sh aiagent-v0.1.0-test.tar.gz

🔍 验证发布包: aiagent-v0.1.0-test.tar.gz

📂 临时目录: /tmp/xxx

📦 解压压缩包...
✅ 解压完成

📋 检查必要文件...
  ✅ main.py
  ✅ requirements.txt
  ✅ README.md
  ✅ common/config.py
  ✅ common/database.py
  ✅ RELEASE_WORKFLOW.md
  ✅ release.sh
  ✅ deploy.sh

📁 目录结构：
.
├── 1_热点监控
├── 2_选题筛选
├── 3_素材采集
├── 4_内容创作
├── 5_配图查找
├── 6_格式优化
├── 7_内容发布
├── common
├── workflows
└── ...

📊 文件统计：
  - Python 文件: 646
  - Markdown 文档: 358
  - Shell 脚本: 7
  - 总文件数: 11616

🐍 创建虚拟环境...
📦 安装依赖...
✅ 依赖安装完成

🔍 检查 Python 导入...
  ✅ common 模块导入成功

🎯 运行主程序...
  ✅ main.py --help 正常
📊 系统状态
  ✅ 主程序可运行

📌 检查版本号...
  ✅ 版本: 0.1.0-test

🔐 检查脚本权限...
  ✅ release.sh (可执行)
  ✅ deploy.sh (可执行)
  ✅ test_build.sh (可执行)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 验证完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 验证结果：
  - 文件完整性: ✅
  - 目录结构: ✅
  - Python 依赖: ✅
  - 模块导入: ✅
  - 主程序运行: ✅

✅ 此发布包可以安全使用！
```

### 场景 3：正式发版

```bash
# 3. 清理测试文件
$ rm -f aiagent-v0.1.0-test.tar.gz aiagent-v0.1.0-test-安装说明.txt

# 4. 正式发版
$ ./release.sh 1.0.0 "feat: 初始版本发布"

🚀 准备发布 AI Agent 版本: v1.0.0
📝 更新说明: feat: 初始版本发布

🧪 运行测试...
⚠️  未发现测试文件，跳过测试

📝 更新版本号...
✅ 版本号已更新: 1.0.0

📦 打包项目...
✅ 打包完成: aiagent-v1.0.0.tar.gz (41M)

💾 提交代码...
✅ 代码已提交

🏷️  创建 Git Tag...
✅ Tag 创建成功: v1.0.0

⬆️  推送到 GitHub...
✅ 推送完成

⏳ GitHub Actions 正在自动构建 Release...
📊 查看构建进度:
   https://github.com/YOUR_USERNAME/AIAgent/actions

📦 Release 将在构建完成后发布:
   https://github.com/YOUR_USERNAME/AIAgent/releases/tag/v1.0.0

🚀 构建完成后，在服务器上执行部署:
   ssh user@your-server
   cd /path/to/aiagent
   ./deploy.sh v1.0.0

🎉 发版流程完成！
```

### 场景 4：服务器部署

```bash
# 5. SSH 到服务器
$ ssh user@your-server

# 6. 执行部署
$ cd /path/to/aiagent
$ ./deploy.sh v1.0.0

🚀 开始部署 AI Agent v1.0.0

📦 备份当前版本...
✅ 备份完成: /var/www/backups/aiagent_backup_20260320_123456

⬇️  下载 Release...
📥 下载地址: https://github.com/.../aiagent-v1.0.0.tar.gz
✅ 下载完成

📂 解压构建产物...
🔄 部署到生产环境...
✅ 保留环境配置
✅ 保留数据库
✅ 保留日志

📦 安装 Python 依赖...
✅ 依赖安装完成

🗄️  检查数据库...
✅ 数据库初始化完成

🔄 重启服务...
✅ systemd 服务已重启

📝 记录部署日志...

🔍 验证部署...
📊 系统状态正常

✅ 部署完成！
📊 当前版本: v1.0.0
📂 部署路径: /var/www/aiagent

📋 回滚命令（如需要）:
   sudo systemctl stop aiagent.service
   rm -rf /var/www/aiagent/*
   cp -r /var/www/backups/aiagent_backup_20260320_123456/* /var/www/aiagent/
   sudo systemctl start aiagent.service
```

---

## 📊 完整流程时间线

```
⏱️ T+0min    开始发版
             ./release.sh 1.0.0 "feat: 新功能"

⏱️ T+1min    本地构建完成
             代码推送到 GitHub

⏱️ T+1min    GitHub Actions 开始构建
             https://github.com/.../actions

⏱️ T+3min    Release 创建完成
             https://github.com/.../releases/tag/v1.0.0

⏱️ T+3min    开始服务器部署
             ./deploy.sh v1.0.0

⏱️ T+4min    部署完成
             验证服务正常运行

⏱️ T+5min    🎉 全流程完成
             总耗时：约 5 分钟
```

---

## 🎯 使用场景

### 场景 A：日常开发迭代

```bash
# 开发新功能
git checkout -b feature/new-module
# ... 编码 ...
git commit -m "feat: 新增功能模块"

# 合并到主分支
git checkout main
git merge feature/new-module

# 发布小版本
./release.sh 1.1.0 "feat: 新增功能模块"

# 部署
ssh server
./deploy.sh v1.1.0
```

### 场景 B：紧急修复

```bash
# 修复 bug
git checkout -b hotfix/critical-bug
# ... 修复 ...
git commit -m "fix: 修复严重 bug"

# 合并并发布补丁版本
git checkout main
git merge hotfix/critical-bug
./release.sh 1.0.1 "fix: 修复严重 bug"

# 快速部署
ssh server
./deploy.sh v1.0.1
```

### 场景 C：测试新功能

```bash
# 测试打包
./test_build.sh 1.2.0-beta

# 验证
./verify_release.sh aiagent-v1.2.0-beta.tar.gz

# 如果测试通过
./release.sh 1.2.0 "feat: 新功能上线"
```

### 场景 D：版本回滚

```bash
# 方式 1: 重新部署旧版本
ssh server
./deploy.sh v1.0.0

# 方式 2: 从备份恢复
ssh server
sudo systemctl stop aiagent.service
rm -rf /var/www/aiagent/*
cp -r /var/www/backups/aiagent_backup_20260320_120000/* /var/www/aiagent/
sudo systemctl start aiagent.service
```

---

## 💡 最佳实践

### ✅ DO（推荐）

```bash
# ✅ 发版前先测试
./test_build.sh 1.0.0-test
./verify_release.sh aiagent-v1.0.0-test.tar.gz

# ✅ 使用语义化版本号
./release.sh 1.0.0 "feat: 初始版本"    # 主版本
./release.sh 1.1.0 "feat: 新功能"      # 次版本
./release.sh 1.0.1 "fix: 修复 bug"     # 修订号

# ✅ 写清楚 commit 消息
git commit -m "feat(funtest): 新增趣味测试分析模块"

# ✅ 部署前备份（脚本自动）
./deploy.sh v1.0.0  # 自动备份到 /var/www/backups/

# ✅ 部署后验证
python main.py status
python main.py funtest --demo
```

### ❌ DON'T（避免）

```bash
# ❌ 跳过测试直接发版
./release.sh 1.0.0 "update"  # 没有测试，消息不清晰

# ❌ 版本号不规范
./release.sh 1.0.0.1 "fix"   # 不是语义化版本

# ❌ 直接在生产环境修改代码
ssh server
vim /var/www/aiagent/main.py  # 应该通过发版流程

# ❌ 手动部署不备份
ssh server
rm -rf /var/www/aiagent/*     # 没有备份，无法回滚
```

---

## 📚 相关文档

- **快速指南**：[RELEASE_GUIDE.md](./RELEASE_GUIDE.md)
- **完整工作流**：[RELEASE_WORKFLOW.md](./RELEASE_WORKFLOW.md)
- **Skill 文档**：[.codebuddy/skills/aiagent-release-deploy.md](./.codebuddy/skills/aiagent-release-deploy.md)
- **完成总结**：[.codebuddy/RELEASE_TOOLS_SUMMARY.md](./.codebuddy/RELEASE_TOOLS_SUMMARY.md)

---

**让发版和部署变得简单高效！** 🚀
