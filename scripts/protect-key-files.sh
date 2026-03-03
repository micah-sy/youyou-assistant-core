#!/bin/bash
# 保护关键文件脚本（需要 root 权限）

echo "🛡️  保护关键配置文件"
echo "===================="
echo ""

# 检查是否 root
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 sudo 运行此脚本"
    echo "   sudo $0"
    exit 1
fi

echo "✅ 以 root 权限运行"
echo ""

# 保护文件
echo "正在保护文件..."

chattr +i /home/tellice/.openclaw/openclaw.json 2>&1 && echo "✅ openclaw.json 已保护" || echo "⚠️  openclaw.json 保护失败"

chattr +i /home/tellice/.config/systemd/user/openclaw-gateway.service 2>&1 && echo "✅ gateway.service 已保护" || echo "⚠️  gateway.service 保护失败"

chattr +i /home/tellice/.openclaw/workspace/.git/config 2>&1 && echo "✅ .git/config 已保护" || echo "⚠️  .git/config 保护失败"

echo ""
echo "验证保护状态："
lsattr /home/tellice/.openclaw/openclaw.json
lsattr /home/tellice/.config/systemd/user/openclaw-gateway.service
lsattr /home/tellice/.openclaw/workspace/.git/config

echo ""
echo "===================="
echo "✅ 保护完成！"
echo ""
echo "📝 解锁方法："
echo "   sudo chattr -i /path/to/file"
echo ""
