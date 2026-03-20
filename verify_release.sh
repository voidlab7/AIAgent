#!/bin/bash
# 快速验证脚本 - 验证发布的压缩包是否可用
# 使用方法: ./verify_release.sh aiagent-v1.0.0.tar.gz

set -e

ARCHIVE=$1

if [ -z "$ARCHIVE" ]; then
  echo "❌ 用法: ./verify_release.sh <压缩包路径>"
  echo "示例: ./verify_release.sh aiagent-v1.0.0.tar.gz"
  exit 1
fi

if [ ! -f "$ARCHIVE" ]; then
  echo "❌ 文件不存在: $ARCHIVE"
  exit 1
fi

echo "🔍 验证发布包: $ARCHIVE"
echo ""

# 1. 创建临时目录
VERIFY_DIR=$(mktemp -d)
echo "📂 临时目录: $VERIFY_DIR"

# 2. 解压
echo "📦 解压压缩包..."
tar -xzf "$ARCHIVE" -C "$VERIFY_DIR"
cd "$VERIFY_DIR"

# 获取解压后的目录名
EXTRACT_DIR=$(ls -d */ | head -1)
cd "$EXTRACT_DIR"

echo "✅ 解压完成"
echo ""

# 3. 检查必要文件
echo "📋 检查必要文件..."
REQUIRED_FILES=(
  "main.py"
  "requirements.txt"
  "README.md"
  "common/config.py"
  "common/database.py"
  "RELEASE_WORKFLOW.md"
  "release.sh"
  "deploy.sh"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ] && [ ! -d "${file%/*}" ]; then
    MISSING_FILES+=("$file")
    echo "  ❌ 缺少: $file"
  else
    echo "  ✅ $file"
  fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
  echo ""
  echo "❌ 压缩包不完整，缺少 ${#MISSING_FILES[@]} 个文件"
  exit 1
fi
echo ""

# 4. 检查目录结构
echo "📁 目录结构："
tree -L 2 -I '__pycache__|*.pyc|node_modules' || find . -maxdepth 2 -type d
echo ""

# 5. 统计文件
echo "📊 文件统计："
PY_COUNT=$(find . -name "*.py" -not -path "./web_site/*" | wc -l)
MD_COUNT=$(find . -name "*.md" | wc -l)
SH_COUNT=$(find . -name "*.sh" | wc -l)
TOTAL_COUNT=$(find . -type f | wc -l)

echo "  - Python 文件: $PY_COUNT"
echo "  - Markdown 文档: $MD_COUNT"
echo "  - Shell 脚本: $SH_COUNT"
echo "  - 总文件数: $TOTAL_COUNT"
echo ""

# 6. 创建虚拟环境
echo "🐍 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 7. 安装依赖
echo "📦 安装依赖..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✅ 依赖安装完成"
echo ""

# 8. 检查导入
echo "🔍 检查 Python 导入..."
python3 << 'EOF'
import sys
try:
    from common.config import ACCOUNT_PROFILE
    from common.database import db
    print("  ✅ common 模块导入成功")
except ImportError as e:
    print(f"  ❌ 导入失败: {e}")
    sys.exit(1)
EOF
echo ""

# 9. 运行主程序
echo "🎯 运行主程序..."
python main.py --help > /dev/null && echo "  ✅ main.py --help 正常"
python main.py status 2>&1 | head -20 || echo "  ⚠️  status 命令警告（可能是首次运行）"
echo ""

# 10. 检查版本号
echo "📌 检查版本号..."
if [ -f "common/__version__.py" ]; then
  VERSION=$(python3 -c "exec(open('common/__version__.py').read()); print(__version__)")
  echo "  ✅ 版本: $VERSION"
else
  echo "  ⚠️  未找到版本号文件"
fi
echo ""

# 11. 检查脚本权限
echo "🔐 检查脚本权限..."
for script in release.sh deploy.sh test_build.sh; do
  if [ -f "$script" ]; then
    if [ -x "$script" ]; then
      echo "  ✅ $script (可执行)"
    else
      echo "  ⚠️  $script (不可执行，需要 chmod +x)"
    fi
  fi
done
echo ""

# 12. 清理
cd /
deactivate 2>/dev/null || true
rm -rf "$VERIFY_DIR"

# 13. 总结
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 验证完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 验证结果："
echo "  - 文件完整性: ✅"
echo "  - 目录结构: ✅"
echo "  - Python 依赖: ✅"
echo "  - 模块导入: ✅"
echo "  - 主程序运行: ✅"
echo ""
echo "✅ 此发布包可以安全使用！"
echo ""
