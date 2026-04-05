# SCP 上传到服务器

通过 SCP + 密码方式将本地文件上传到远程服务器。

## 触发条件

当用户提到以下关键词或场景时使用此 Skill：
- `上传到服务器` / `scp` / `传到服务器` / `上传文件`
- `部署脚本到服务器` / `同步到服务器` / `传文件到远程`
- `发到服务器` / `拷贝到服务器` / `推送到服务器`
- `部署到服务器` / `部署到线上` / `上线`
- 用户提到需要把本地文件放到 `microlab.top` 服务器上时

## 服务器配置

| 配置项 | 值 |
|--------|-----|
| 服务器地址 | `microlab.top` |
| 登录用户 | `root` |
| 认证方式 | 密码认证 |
| root 密码 | 项目根目录 `.env` 文件中的 `SERVER_PASSWORD` 变量 |
| .env 路径 | `/Users/voidzhang/Documents/workspace/AIAgent/.env` |
| SSH 端口 | `22`（默认） |

## 常用目标路径

| 用途 | 服务器目标路径 |
|------|--------------|
| 部署/运维脚本 | `/root/scripts/` |
| 前端静态文件 | `/var/www/pawmbti/` |
| 后端计数服务 | `/var/www/pawmbti-server/` |
| Nginx 配置 | `/etc/nginx/conf.d/` 或 `/etc/nginx/sites-enabled/` |

## 使用流程

### 第一步：确认上传信息

向用户确认以下信息（如未指定）：
1. **本地文件路径** — 要上传的文件或目录
2. **服务器目标路径** — 根据文件类型自动推荐（参考"常用目标路径"表），或由用户指定
3. **是否需要上传后执行命令** — 如设置权限、重启服务等

### 第二步：加载密码并确保 sshpass 可用

**密码来源**：从项目根目录 `.env` 文件读取 `SERVER_PASSWORD` 变量。

```bash
# 加载 .env 中的密码
source /Users/voidzhang/Documents/workspace/AIAgent/.env
# 此时 $SERVER_PASSWORD 可用
```

**确保 sshpass 可用**（关键步骤）：

```bash
# 优先级1: 检查 ~/bin/sshpass（之前源码编译安装的位置）
if [ -x "$HOME/bin/sshpass" ]; then
    SSHPASS="$HOME/bin/sshpass"
# 优先级2: 检查系统 PATH 中的 sshpass
elif command -v sshpass &>/dev/null; then
    SSHPASS="sshpass"
# 优先级3: 检查 /usr/local/bin/sshpass
elif [ -x "/usr/local/bin/sshpass" ]; then
    SSHPASS="/usr/local/bin/sshpass"
else
    # 需要安装，见下方安装流程
    SSHPASS=""
fi
```

**如果 sshpass 不可用，执行自动安装：**

```bash
# macOS: 从源码编译安装到 ~/bin/（不需要 sudo）
mkdir -p ~/bin
cd /tmp
curl -LO https://sourceforge.net/projects/sshpass/files/sshpass/1.10/sshpass-1.10.tar.gz
tar xzf sshpass-1.10.tar.gz
cd sshpass-1.10
./configure
make
cp sshpass ~/bin/sshpass
chmod +x ~/bin/sshpass
SSHPASS="$HOME/bin/sshpass"

# Linux (Ubuntu/Debian):
# sudo apt-get install -y sshpass
```

> **重要**：sshpass 已编译安装在 `~/bin/sshpass`，且 `~/bin` 已加入 `~/.bash_profile` 和 `~/.zshrc` 的 PATH。新开终端会自动识别。但在 CodeBuddy 的 execute_command 中，需要使用完整路径 `~/bin/sshpass` 或 `$HOME/bin/sshpass` 来调用。

### 第三步：执行 SCP 上传

使用检测到的 sshpass 路径执行上传命令。**所有命令前先 `source .env` 加载密码**：

#### 上传单个文件

```bash
source /Users/voidzhang/Documents/workspace/AIAgent/.env
$SSHPASS -p "$SERVER_PASSWORD" scp -o StrictHostKeyChecking=no <本地文件路径> root@microlab.top:<服务器目标路径>
```

#### 上传整个目录

```bash
source /Users/voidzhang/Documents/workspace/AIAgent/.env
$SSHPASS -p "$SERVER_PASSWORD" scp -o StrictHostKeyChecking=no -r <本地目录路径>/* root@microlab.top:<服务器目标路径>
```

#### 上传多个文件

```bash
source /Users/voidzhang/Documents/workspace/AIAgent/.env
$SSHPASS -p "$SERVER_PASSWORD" scp -o StrictHostKeyChecking=no <文件1> <文件2> <文件3> root@microlab.top:<服务器目标路径>
```

### 第四步：上传后操作（可选）

如果需要在上传后执行服务器端命令（如修改权限、重启服务），通过 SSH 执行：

```bash
source /Users/voidzhang/Documents/workspace/AIAgent/.env
$SSHPASS -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no root@microlab.top "<命令>"
```

常见的上传后操作：
- **脚本赋予执行权限**：`chmod +x /root/scripts/<脚本名>`
- **执行部署脚本**：`/root/scripts/deploy_website.sh`
- **重启服务**：`pm2 restart pawmbti-counter`
- **重载 Nginx**：`nginx -t && nginx -s reload`

## 完整示例

### 示例 1：上传部署脚本并执行

```bash
# 上传
~/bin/sshpass -p '$SERVER_PASSWORD' scp -o StrictHostKeyChecking=no /Users/voidzhang/Documents/workspace/AIAgent/web_site/scripts/deploy_website.sh root@microlab.top:/root/scripts/deploy_website.sh

# 赋予执行权限并运行
~/bin/sshpass -p '$SERVER_PASSWORD' ssh -o StrictHostKeyChecking=no root@microlab.top "chmod +x /root/scripts/deploy_website.sh && /root/scripts/deploy_website.sh"
```

### 示例 2：上传 Nginx 配置并重载

```bash
# 上传
~/bin/sshpass -p '$SERVER_PASSWORD' scp -o StrictHostKeyChecking=no /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti/server/nginx-example.conf root@microlab.top:/etc/nginx/conf.d/pawmbti.conf

# 测试并重载
~/bin/sshpass -p '$SERVER_PASSWORD' ssh -o StrictHostKeyChecking=no root@microlab.top "nginx -t && nginx -s reload"
```

### 示例 3：上传整个 dist 目录（前端部署）

```bash
# 上传构建产物
~/bin/sshpass -p '$SERVER_PASSWORD' scp -o StrictHostKeyChecking=no -r /Users/voidzhang/Documents/workspace/AIAgent/web_site/pawmbti/dist/* root@microlab.top:/var/www/pawmbti/

# 重载 Nginx
~/bin/sshpass -p '$SERVER_PASSWORD' ssh -o StrictHostKeyChecking=no root@microlab.top "nginx -t && nginx -s reload"
```

## 错误处理

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Permission denied, please try again` | 密码错误 | 确认 root 密码是否正确 |
| `sshpass: command not found` | 未安装 sshpass | 使用 `~/bin/sshpass`，或按安装流程从源码编译 |
| `Connection refused` | SSH 服务未运行或端口不对 | 确认服务器 SSH 服务状态和端口 |
| `No such file or directory` | 服务器目标目录不存在 | 先 SSH 执行 `mkdir -p <目标目录>` |
| `Connection timed out` | 网络不通或防火墙拦截 | 检查网络连接和安全组规则 |

## AI 执行指引

当使用此 Skill 时：

1. **密码加载（关键）** — 执行任何 scp/ssh 命令前，**必须先** `source /Users/voidzhang/Documents/workspace/AIAgent/.env` 加载 `$SERVER_PASSWORD` 变量。不要依赖环境变量已设置，每次都 source。
2. **sshpass 检测优先级** — 先检查 `~/bin/sshpass` 是否存在（`ls ~/bin/sshpass`），存在则直接用 `~/bin/sshpass`；不存在再检查 `which sshpass`；都没有则从源码自动编译安装到 `~/bin/`
2. **始终用完整路径** — 在 `execute_command` 中，优先使用 `~/bin/sshpass` 完整路径调用，避免 PATH 问题
3. **自动推断目标路径** — 根据用户提供的文件类型，参考"常用目标路径"表自动推荐。脚本文件 → `/root/scripts/`，前端文件 → `/var/www/pawmbti/`
4. **使用 execute_command 执行** — 先执行 scp 上传，再根据需要执行 ssh 后续命令
5. **requires_approval 设为 true** — 所有 scp 和 ssh 命令涉及远程服务器操作，必须让用户确认
6. **反馈结果** — 告诉用户上传是否成功，文件大小，以及执行了什么后续操作
7. **密码引用方式** — 密码变量用双引号 `"$SERVER_PASSWORD"` 包裹（因为已通过 source .env 加载为 shell 变量，不需要单引号防解析）
8. **安装失败兜底** — 如果源码编译也失败，提示用户手动安装或使用 `expect` 作为替代方案
