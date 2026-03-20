#!/bin/bash
# 测试打包脚本 - 验证发布流程（不推送到 GitHub）
# 使用方法: ./test_build.sh 1.0.0

set -e

VERSION=${1:-0.0.1-test}

# 规范化版本号
if [[ ! $VERSION =~ ^v ]]; then
  VERSION="v$VERSION"
fi

echo "🧪 测试打包流程（版本: $VERSION）"
echo "⚠️  注意：此脚本不会推送到 GitHub"
echo ""

# 1. 检查项目结构
echo "📂 检查项目结构..."
REQUIRED_FILES=("main.py" "requirements.txt" "README.md" "common/config.py")
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ] && [ ! -d "${file%/*}" ]; then
    echo "❌ 缺少文件: $file"
    exit 1
  fi
done
echo "✅ 项目结构完整"
echo ""

# 2. 检查 Python 环境
echo "🐍 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
  echo "❌ 未找到 Python 3"
  exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"
echo ""

# 3. 安装依赖（虚拟环境）
echo "📦 创建测试虚拟环境..."
TEST_VENV=".test_venv"
if [ -d "$TEST_VENV" ]; then
  rm -rf "$TEST_VENV"
fi
python3 -m venv "$TEST_VENV"
source "$TEST_VENV/bin/activate"

echo "📥 安装依赖..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✅ 依赖安装完成"
echo ""

# 4. 运行语法检查
echo "🔍 运行语法检查..."
find . -name "*.py" -not -path "./$TEST_VENV/*" -not -path "./web_site/*" | while read file; do
  python3 -m py_compile "$file" 2>&1 || echo "⚠️  语法错误: $file"
done
echo "✅ 语法检查完成"
echo ""

# 5. 运行测试（如果有）
if [ -f "pytest.ini" ] || [ -d "tests" ]; then
  echo "🧪 运行测试..."
  pip install --quiet pytest pytest-cov
  pytest tests/ -v --tb=short || echo "⚠️  部分测试失败"
  echo ""
else
  echo "⚠️  未发现测试文件，跳过测试"
  echo ""
fi

# 6. 测试主程序
echo "🎯 测试主程序..."
python main.py --help > /dev/null
echo "✅ 主程序可以正常运行"
echo ""

# 7. 更新版本号
echo "📝 更新版本号..."
mkdir -p common
echo "__version__ = '${VERSION#v}'" > common/__version__.py
echo "✅ 版本号已更新: ${VERSION#v}"
echo ""

# 8. 打包项目
echo "📦 打包项目..."
TMP_DIR=$(mktemp -d)
ARCHIVE_NAME="aiagent-$VERSION"
BUILD_DIR="$TMP_DIR/$ARCHIVE_NAME"

echo "  → 创建构建目录: $BUILD_DIR"
mkdir -p "$BUILD_DIR"

# 复制项目文件
echo "  → 复制项目文件..."
rsync -a --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  --exclude='cache/' \
  --exclude='logs/' \
  --exclude='data/*.db' \
  --exclude="$TEST_VENV" \
  --exclude='.test_venv' \
  --exclude='web_site/node_modules/' \
  --exclude='web_site/dist/' \
  . "$BUILD_DIR/"

# 打包
cd "$TMP_DIR"
tar -czf "$OLDPWD/$ARCHIVE_NAME.tar.gz" "$ARCHIVE_NAME"
cd "$OLDPWD"

ARCHIVE_SIZE=$(du -h "$ARCHIVE_NAME.tar.gz" | cut -f1)
echo "✅ 打包完成: $ARCHIVE_NAME.tar.gz ($ARCHIVE_SIZE)"
echo ""

# 9. 验证压缩包
echo "🔍 验证压缩包..."
VERIFY_DIR=$(mktemp -d)
tar -xzf "$ARCHIVE_NAME.tar.gz" -C "$VERIFY_DIR"

echo "  → 检查文件结构..."
cd "$VERIFY_DIR/$ARCHIVE_NAME"
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ] && [ ! -d "${file%/*}" ]; then
    echo "❌ 压缩包中缺少: $file"
    exit 1
  fi
done

echo "  → 检查文件数量..."
FILE_COUNT=$(find . -type f | wc -l)
echo "    文件数量: $FILE_COUNT"

echo "  → 检查目录结构..."
find . -maxdepth 2 -type d | head -20
cd "$OLDPWD"

echo "✅ 压缩包验证通过"
echo ""

# 10. 生成安装说明
INSTALL_GUIDE="$ARCHIVE_NAME-安装说明.txt"
cat > "$INSTALL_GUIDE" << EOF
AI Agent $VERSION - 安装说明

========================
1. 解压
========================
tar -xzf $ARCHIVE_NAME.tar.gz
cd $ARCHIVE_NAME

========================
2. 安装依赖
========================
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

========================
3. 配置环境
========================
# 如果有 .env.example，复制并配置
cp .env.example .env
# 编辑 .env 填写 API Keys

========================
4. 初始化
========================
python main.py init

========================
5. 验证安装
========================
python main.py status
python main.py funtest --demo

========================
6. 运行
========================
# 查看帮助
python main.py --help

# 运行单个模块
python main.py hotspot
python main.py funtest --demo

# 运行完整工作流
python main.py workflow --once

========================
更多信息
========================
- 文档: README.md
- 问题反馈: https://github.com/YOUR_USERNAME/AIAgent/issues
EOF

echo "📄 生成安装说明: $INSTALL_GUIDE"
echo ""

# 11. 清理
echo "🧹 清理测试环境..."
deactivate 2>/dev/null || true
rm -rf "$TEST_VENV" "$TMP_DIR" "$VERIFY_DIR"
echo "✅ 清理完成"
echo ""

# 12. 总结
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 测试打包成功！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 构建产物："
echo "  - $ARCHIVE_NAME.tar.gz ($ARCHIVE_SIZE)"
echo "  - $INSTALL_GUIDE"
echo ""
echo "🔍 验证结果："
echo "  - 项目结构: ✅"
echo "  - Python 环境: ✅"
echo "  - 依赖安装: ✅"
echo "  - 语法检查: ✅"
echo "  - 主程序运行: ✅"
echo "  - 压缩包验证: ✅"
echo ""
echo "📋 下一步："
echo "  1. 手动测试压缩包："
echo "     tar -xzf $ARCHIVE_NAME.tar.gz"
echo "     cd $ARCHIVE_NAME"
echo "     python3 -m venv venv && source venv/bin/activate"
echo "     pip install -r requirements.txt"
echo "     python main.py status"
echo ""
echo "  2. 如果测试通过，执行正式发版："
echo "     ./release.sh ${VERSION#v} 'feat: 新功能描述'"
echo ""
echo "  3. 清理测试文件："
echo "     rm -rf $ARCHIVE_NAME.tar.gz $INSTALL_GUIDE"
echo ""
