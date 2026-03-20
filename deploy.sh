#!/bin/bash
# AI Agent 项目 - OpenClaw 部署脚本
# 使用方法: ./deploy.sh v1.0.0

set -e  # 遇到错误立即退出

VERSION=${1:-latest}  # 默认部署最新版本
REPO="YOUR_USERNAME/AIAgent"  # 替换为你的 GitHub 仓库
DEPLOY_DIR="/var/www/aiagent"  # 部署目录
BACKUP_DIR="/var/www/backups"  # 备份目录
VENV_DIR="$DEPLOY_DIR/venv"  # 虚拟环境目录

echo "🚀 开始部署 AI Agent $VERSION"

# 1. 创建备份
echo "📦 备份当前版本..."
BACKUP_NAME="aiagent_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

if [ -d "$DEPLOY_DIR" ]; then
  cp -r $DEPLOY_DIR $BACKUP_DIR/$BACKUP_NAME
  echo "✅ 备份完成: $BACKUP_DIR/$BACKUP_NAME"
else
  echo "⚠️  首次部署，跳过备份"
  mkdir -p $DEPLOY_DIR
fi

# 2. 下载构建产物
echo "⬇️  下载 Release..."
TMP_DIR=$(mktemp -d)
cd $TMP_DIR

if [ "$VERSION" = "latest" ]; then
  # 下载最新 Release
  DOWNLOAD_URL=$(curl -s https://api.github.com/repos/$REPO/releases/latest | grep "browser_download_url.*tar.gz" | cut -d '"' -f 4)
  VERSION=$(curl -s https://api.github.com/repos/$REPO/releases/latest | grep '"tag_name":' | cut -d '"' -f 4)
else
  # 下载指定版本
  DOWNLOAD_URL="https://github.com/$REPO/releases/download/$VERSION/aiagent-$VERSION.tar.gz"
fi

echo "📥 下载地址: $DOWNLOAD_URL"
wget -q --show-progress $DOWNLOAD_URL -O aiagent.tar.gz

if [ ! -f aiagent.tar.gz ]; then
  echo "❌ 下载失败！"
  exit 1
fi

# 3. 解压并部署
echo "📂 解压构建产物..."
tar -xzf aiagent.tar.gz
cd aiagent-$VERSION

echo "🔄 部署到生产环境..."
# 保留 .env、data/ 和 logs/ 目录
if [ -f "$DEPLOY_DIR/.env" ]; then
  cp "$DEPLOY_DIR/.env" .env
  echo "✅ 保留环境配置"
fi

if [ -d "$DEPLOY_DIR/data" ]; then
  rm -rf data
  cp -r "$DEPLOY_DIR/data" .
  echo "✅ 保留数据库"
fi

if [ -d "$DEPLOY_DIR/logs" ]; then
  rm -rf logs
  cp -r "$DEPLOY_DIR/logs" .
  echo "✅ 保留日志"
fi

# 部署新代码
rm -rf $DEPLOY_DIR/*
cp -r * $DEPLOY_DIR/
cp -r .* $DEPLOY_DIR/ 2>/dev/null || true

# 4. 安装依赖
echo "📦 安装 Python 依赖..."
cd $DEPLOY_DIR

# 激活或创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
  echo "🔧 创建虚拟环境..."
  python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 依赖安装完成"

# 5. 数据库迁移（如果需要）
echo "🗄️  检查数据库..."
python main.py init

# 6. 重启服务（根据你的部署方式）
echo "🔄 重启服务..."

# 方式 1: systemd
if systemctl is-active --quiet aiagent.service; then
  sudo systemctl restart aiagent.service
  echo "✅ systemd 服务已重启"
# 方式 2: supervisor
elif command -v supervisorctl &> /dev/null; then
  sudo supervisorctl restart aiagent
  echo "✅ supervisor 服务已重启"
# 方式 3: PM2（如果是 Node.js 混合项目）
elif command -v pm2 &> /dev/null; then
  pm2 restart aiagent
  echo "✅ PM2 服务已重启"
else
  echo "⚠️  未检测到服务管理器，请手动重启服务"
fi

# 7. 清理临时文件
cd /
rm -rf $TMP_DIR

# 8. 记录部署日志
echo "📝 记录部署日志..."
LOG_FILE="/var/log/aiagent-deploy.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 部署成功: $VERSION" >> $LOG_FILE

# 9. 验证部署
echo "🔍 验证部署..."
cd $DEPLOY_DIR
source $VENV_DIR/bin/activate
python main.py status

echo ""
echo "✅ 部署完成！"
echo "📊 当前版本: $VERSION"
echo "📂 部署路径: $DEPLOY_DIR"
echo ""
echo "📋 回滚命令（如需要）:"
echo "   sudo systemctl stop aiagent.service  # 停止服务"
echo "   rm -rf $DEPLOY_DIR/*"
echo "   cp -r $BACKUP_DIR/$BACKUP_NAME/* $DEPLOY_DIR/"
echo "   sudo systemctl start aiagent.service  # 启动服务"
