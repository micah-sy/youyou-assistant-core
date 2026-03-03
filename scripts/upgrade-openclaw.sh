#!/bin/bash
# OpenClaw 升级脚本
# 用法：./upgrade-openclaw.sh

set -e

echo "🦞 检查 OpenClaw 更新..."

# 当前版本
CURRENT=$(openclaw --version 2>/dev/null || echo "unknown")
echo "当前版本：$CURRENT"

# 升级
echo "正在升级..."
npm install -g openclaw@latest

# 新版本
NEW=$(openclaw --version 2>/dev/null || echo "unknown")
echo "新版本：$NEW"

# 重启 Gateway
echo "重启 Gateway..."
systemctl --user restart openclaw-gateway

# 等待启动
sleep 3

# 检查状态
echo "检查状态..."
systemctl --user status openclaw-gateway --no-pager | head -10

echo ""
echo "✅ 升级完成！"
