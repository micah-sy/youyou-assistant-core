#!/bin/bash
# 悠悠监控仪表盘 - 按需启动脚本

cd ~/.openclaw/workspace

echo "🐣 悠悠监控仪表盘"
echo "━━━━━━━━━━━━━━━━━━"

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行：uv venv --python 3.11"
    exit 1
fi

# 激活虚拟环境
source .venv/bin/activate

# 启动仪表盘
echo "📊 启动中..."
python3 scripts/dashboard.py

echo ""
echo "✅ 仪表盘已停止"
