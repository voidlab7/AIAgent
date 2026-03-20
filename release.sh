#!/bin/bash
# AI Agent 项目 - 本地发版脚本
# 使用方法: ./release.sh 1.0.0 "feat: 新增趣味测试分析功能"

set -e

VERSION=$1
MESSAGE=$2

if [ -z "$VERSION" ] || [ -z "$MESSAGE" ]; then
  echo "❌ 用法: ./release.sh <版本号> <更新说明>"
  echo "示例: ./release.sh 1.0.0 'feat: 新增趣味测试分析功能'"
  exit 1
fi

# 规范化版本号（添加 v 前缀）
if [[ ! $VERSION =~ ^v ]]; then
  VERSION="v$VERSION"
fi

echo "🚀 准备发布 AI Agent 版本: $VERSION"
echo "📝 更新说明: $MESSAGE"
echo ""

# 1. 检查工作区是否干净
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️  工作区有未提交的修改，是否继续？(y/n)"
  read -r response
  if [ "$response" != "y" ]; then
    echo "❌ 已取消发布"
    exit 1
  fi
fi

# 2. 运行测试（可选）
echo "🧪 运行测试..."
if [ -f "pytest.ini" ] || [ -d "tests" ]; then
  python -m pytest tests/ -v --tb=short || {
    echo "⚠️  测试失败，是否继续发布？(y/n)"
    read -r response
    if [ "$response" != "y" ]; then
      echo "❌ 已取消发布"
      exit 1
    fi
  }
else
  echo "⚠️  未发现测试文件，跳过测试"
fi
echo ""

# 3. 更新版本号到 __version__.py（如果存在）
if [ -f "common/__version__.py" ]; then
  echo "📝 更新版本号..."
  echo "__version__ = '${VERSION#v}'" > common/__version__.py
  git add common/__version__.py
fi

# 4. 打包项目
echo "📦 打包项目..."
# 创建临时目录
TMP_DIR=$(mktemp -d)
ARCHIVE_NAME="aiagent-$VERSION"

# 复制项目文件（排除缓存和临时文件）
rsync -av --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  --exclude='cache/' \
  --exclude='logs/' \
  --exclude='data/*.db' \
  --exclude='web_site/node_modules/' \
  --exclude='web_site/dist/' \
  . "$TMP_DIR/$ARCHIVE_NAME/"

# 打包
cd "$TMP_DIR"
tar -czf "$ARCHIVE_NAME.tar.gz" "$ARCHIVE_NAME"
mv "$ARCHIVE_NAME.tar.gz" "$OLDPWD/"
cd "$OLDPWD"
rm -rf "$TMP_DIR"

ARCHIVE_SIZE=$(du -h "$ARCHIVE_NAME.tar.gz" | cut -f1)
echo "✅ 打包完成: $ARCHIVE_NAME.tar.gz ($ARCHIVE_SIZE)"
echo ""

# 5. 提交代码（如果有未提交的修改）
if [ -n "$(git status --porcelain)" ]; then
  echo "💾 提交代码..."
  git add .
  git commit -m "$MESSAGE"
  echo "✅ 代码已提交"
  echo ""
fi

# 6. 创建 Tag
echo "🏷️  创建 Git Tag..."
git tag -a $VERSION -m "$MESSAGE"
echo "✅ Tag 创建成功: $VERSION"
echo ""

# 7. 推送到 GitHub
echo "⬆️  推送到 GitHub..."
git push origin main --tags

echo "✅ 推送完成"
echo ""

# 8. 等待 GitHub Actions 构建（如果配置了）
echo "⏳ GitHub Actions 正在自动构建 Release..."
echo "📊 查看构建进度:"
echo "   https://github.com/YOUR_USERNAME/AIAgent/actions"
echo ""
echo "📦 Release 将在构建完成后发布:"
echo "   https://github.com/YOUR_USERNAME/AIAgent/releases/tag/$VERSION"
echo ""

# 9. 提示部署命令
echo "🚀 构建完成后，在服务器上执行部署:"
echo "   ssh user@your-server"
echo "   cd /path/to/aiagent"
echo "   ./deploy.sh $VERSION"
echo ""

# 10. 显示快速验证命令
echo "📋 本地快速验证:"
echo "   tar -xzf $ARCHIVE_NAME.tar.gz"
echo "   cd $ARCHIVE_NAME"
echo "   pip install -r requirements.txt"
echo "   python main.py status"
echo ""

echo "🎉 发版流程完成！"
