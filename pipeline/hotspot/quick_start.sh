#!/bin/bash
# 小红书热门文章抓取 - 快速启动脚本

PROJECT_ROOT="/Users/voidzhang/Documents/workspace/AIAgent"
cd "$PROJECT_ROOT"

echo "=================================================="
echo "小红书热门文章自动抓取"
echo "=================================================="

# 检查 Python 环境
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: python -m venv .venv"
    exit 1
fi

source .venv/bin/activate

# 检查依赖
echo ""
echo "检查依赖..."
pip list | grep schedule > /dev/null || {
    echo "安装 schedule..."
    pip install schedule
}

# 检查 RedNote MCP
echo ""
echo "检查 RedNote MCP..."
if command -v rednote-mcp &> /dev/null; then
    echo "✓ RedNote MCP 已安装"
else
    echo "⚠️  RedNote MCP 未安装"
    echo "   安装命令: npm install -g rednote-mcp"
    echo "   登录命令: rednote-mcp init"
    echo ""
    read -p "是否继续使用模拟数据? (y/n): " choice
    if [ "$choice" != "y" ]; then
        exit 1
    fi
fi

# 创建必要的目录
mkdir -p logs
mkdir -p reports/xiaohongshu

echo ""
echo "=================================================="
echo "选择操作:"
echo "=================================================="
echo "1) 立即执行一次（测试）"
echo "2) 启动定时任务（每天凌晨 2 点）"
echo "3) 自定义关键词执行"
echo "4) 查看配置"
echo "5) 查看最新报告"
echo "6) 退出"
echo "=================================================="

read -p "请选择 (1-6): " choice

case $choice in
    1)
        echo ""
        echo "执行一次抓取..."
        python 1_热点监控/scheduler.py --once
        ;;
    2)
        echo ""
        echo "启动定时任务..."
        echo "日志文件: logs/hotspot.log"
        echo "按 Ctrl+C 停止"
        nohup python 1_热点监控/scheduler.py > logs/hotspot.log 2>&1 &
        echo "✓ 后台进程已启动 (PID: $!)"
        echo "查看日志: tail -f logs/hotspot.log"
        ;;
    3)
        read -p "输入关键词（逗号分隔）: " keywords
        echo ""
        echo "执行自定义关键词抓取..."
        python 1_热点监控/scheduler.py --once --keywords "$keywords"
        ;;
    4)
        echo ""
        echo "当前配置:"
        cat 1_热点监控/config.json
        ;;
    5)
        echo ""
        today=$(date +%Y-%m-%d)
        report_file="reports/xiaohongshu/hot_$today.md"
        if [ -f "$report_file" ]; then
            echo "今日报告:"
            cat "$report_file"
        else
            echo "今日暂无报告"
        fi
        ;;
    6)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac
