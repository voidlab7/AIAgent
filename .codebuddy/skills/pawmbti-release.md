# PawMBTI 网站打包发版 Skill

将 PawMBTI 网站项目构建、提交到 GitHub 并创建新的 Release 版本。

## 触发条件

当用户提到以下关键词或场景时使用此 Skill：
- `打包上传` / `打包发版` / `发版` / `发布版本`
- `上传到 GitHub` / `推送到 GitHub` / `push 到 GitHub`
- `升级 release` / `更新版本` / `新版本` / `升级版本`
- `pawmbti 发版` / `网站发版` / `前端发版`
- 用户提到需要将 PawMBTI 网站改动提交并创建新的 GitHub Release 时

## 项目配置

| 配置项 | 值 |
|--------|-----|
| 项目路径 | `/Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti` |
| GitHub 仓库 | `https://github.com/voidlab7/web_site.git` |
| GitHub 用户 | `voidlab7` |
| 仓库名 | `web_site` |
| 远程方式 | HTTPS（通过 credential helper 自动认证） |
| 版本文件 | `package.json` 中的 `version` 字段 |
| 构建命令 | `npm run build`（即 `tsc -b && vite build`） |
| 构建产物 | `dist/` 目录 |
| 线上部署路径 | `/var/www/pawmbti/`（通过 scp-upload skill 上传） |
| SSH Key 指纹 | `$SSH_KEY_FINGERPRINT` |

## 版本号规范

采用语义化版本号 `vX.Y.Z`：

| 变更类型 | 升级位 | 示例 |
|---------|--------|------|
| Bug 修复、小调整 | 修订号 Z | v1.2.0 → v1.2.1 |
| 新功能、新页面 | 次版本 Y | v1.2.0 → v1.3.0 |
| 重大架构变更 | 主版本 X | v1.2.0 → v2.0.0 |

## 使用流程

### 第一步：确认发版信息

向用户确认以下信息（如未指定则自动推断）：

1. **版本号** — 读取当前 `package.json` 中的 version 和最新 git tag，自动建议下一个版本号
2. **更新说明** — 从 `git diff` 和 `git status` 推断改动内容，生成 commit message
3. **版本类型** — 根据改动内容自动判断是 patch/minor/major

```bash
# 获取当前版本信息
cd /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti
cat package.json | grep '"version"'
git tag --sort=-v:refname | head -3
git status
git diff --stat
```

### 第二步：构建项目

```bash
cd /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti
npm run build
```

确认构建成功（无报错）。如果有 TypeScript 或 ESLint 错误，先修复再继续。

### 第三步：升级版本号

修改 `package.json` 中的 `version` 字段到新版本号：

```bash
# 使用 replace_in_file 工具修改 package.json
# "version": "1.2.0" → "version": "1.3.0"
```

### 第四步：提交代码

```bash
cd /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti

# 暂存所有改动
git add -A

# 查看待提交文件
git status

# 提交（使用 Conventional Commits 格式）
git commit -m "<type>(pawmbti): v<版本号> <简短描述>

## 新增
- <列出新增功能>

## 变更
- <列出变更项>

## 修复
- <列出修复项>"
```

**Commit 类型参考**：
- `feat`: 新功能、新页面
- `fix`: Bug 修复
- `refactor`: 重构
- `style`: 样式/UI 调整
- `perf`: 性能优化
- `chore`: 构建/配置变更

### 第五步：创建 Tag

```bash
cd /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti

git tag -a v<版本号> -m "v<版本号> - <简短描述>

## 新增
- <列出新增功能>

## 变更
- <列出变更项>

## 修复
- <列出修复项>"
```

### 第六步：推送到 GitHub

```bash
cd /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti

# 推送代码和 tag（requires_approval = true）
git push origin main --tags
```

**注意**：此命令必须设置 `requires_approval = true`，让用户确认后再执行。

### 第七步：创建 GitHub Release

尝试以下方式（按优先级）：

#### 方式 1：GitHub CLI（gh）

```bash
cd /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti

# 先检查认证状态
gh auth status

# 创建 Release
gh release create v<版本号> \
  --title "v<版本号> - <简短描述>" \
  --notes "## 🐱 PawMBTI v<版本号>

### ✨ 新增
- <列出新增功能>

### 🔄 变更
- <列出变更项>

### 🐛 修复
- <列出修复项>

### 📱 访问地址
- 速测版：https://microlab.top/quick
- 深度版：https://microlab.top/pro
- 主站：https://microlab.top"
```

#### 方式 2：GitHub API + SSH Key

如果 gh CLI 未认证，使用 GitHub API（需要 token）：

```bash
# 提示用户手动到 GitHub 页面创建 Release
echo "请访问以下链接手动创建 Release："
echo "https://github.com/voidlab7/web_site/releases/new?tag=v<版本号>"
```

#### 方式 3：引导用户手动创建

如果以上方式都不可用，输出 Release 信息供用户手动填写：

```
📋 Release 信息：
- Tag: v<版本号>
- Title: v<版本号> - <简短描述>
- URL: https://github.com/voidlab7/web_site/releases/new?tag=v<版本号>
```

### 第八步（可选）：部署到线上服务器

如果用户同时需要部署，调用 **scp-upload** Skill 上传构建产物：

```bash
# 使用 sshpass + scp 上传 dist 到服务器
~/bin/sshpass -p '$SERVER_PASSWORD' scp -o StrictHostKeyChecking=no -r /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti/dist/* root@microlab.top:/var/www/pawmbti/
```

## 完整示例

### 示例：从开发到发版的完整流程

```bash
# 1. 查看当前状态
cd /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti
git status
cat package.json | grep '"version"'
git tag --sort=-v:refname | head -3

# 2. 构建
npm run build

# 3. 升级版本号（使用 replace_in_file 工具）
# "version": "1.2.0" → "version": "1.3.0"

# 4. 提交
git add -A
git commit -m "feat(pawmbti): v1.3.0 新增分享功能

## 新增
- 结果页分享到微信功能
- 分享海报生成

## 变更
- 优化结果页布局"

# 5. 打 Tag
git tag -a v1.3.0 -m "v1.3.0 - 新增分享功能

## 新增
- 结果页分享到微信功能
- 分享海报生成

## 变更
- 优化结果页布局"

# 6. 推送（requires_approval = true）
git push origin main --tags

# 7. 创建 Release
gh release create v1.3.0 \
  --title "v1.3.0 - 新增分享功能" \
  --notes "## 🐱 PawMBTI v1.3.0
  
### ✨ 新增
- 结果页分享到微信功能
- 分享海报生成

### 🔄 变更
- 优化结果页布局

### 📱 访问地址
- 速测版：https://microlab.top/quick
- 深度版：https://microlab.top/pro"

# 8.（可选）部署到线上
~/bin/sshpass -p '$SERVER_PASSWORD' scp -o StrictHostKeyChecking=no -r dist/* root@microlab.top:/var/www/pawmbti/
```

## 版本历史参考

| 版本 | 日期 | 主要内容 |
|------|------|---------|
| v1.0.0 | - | 初始版本 |
| v1.0.1 | - | 版本信息显示 + 部署脚本 |
| v1.1.0 | - | 多路由架构 + 深度版测试 |
| v1.2.0 | 2026-03-23 | 添加 /quick 和 /pro 独立主入口页面 |

## AI 执行指引

当使用此 Skill 时：

1. **自动推断版本号** — 读取当前 package.json 版本和最新 tag，根据改动类型（feat→minor, fix→patch）建议新版本号
2. **自动生成 commit message** — 从 `git diff --stat` 和改动文件推断更新内容，使用 Conventional Commits 格式
3. **构建优先** — 在提交前先执行 `npm run build` 确保构建通过
4. **push 需要审批** — `git push` 命令设置 `requires_approval = true`
5. **创建 Release 需要审批** — `gh release create` 命令设置 `requires_approval = true`
6. **记录版本历史** — 发版完成后，更新工作记忆（.codebuddy/memory/）记录版本信息
7. **失败处理** — 如果 gh CLI 不可用，提供手动创建 Release 的 URL 和信息
8. **可选部署** — 提示用户是否需要同时部署到线上服务器，如需则调用 scp-upload skill
