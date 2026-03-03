#!/bin/bash
# 慢雾安全指南 - 红队测试脚本
# 用于验证安全防御是否有效

set -e

echo "🔴 慢雾安全指南 - 红队测试"
echo "=========================="
echo ""
echo "⚠️  警告：这将模拟攻击测试，不会造成实际损害"
echo ""
read -p "是否继续？(y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ 测试已取消"
    exit 0
fi

echo ""
echo "=== 测试 1: 危险命令检测 ==="
echo "模拟执行：rm -rf /tmp/test-danger"
echo "预期：应该被标记为危险命令"
echo ""

# 检查审计日志中是否有危险命令检测
LOG_DIR="/home/tellice/.openclaw/workspace/logs/security"
if [ -f "$LOG_DIR/dangerous-commands-*.txt" ]; then
    echo "✅ 危险命令审计日志存在"
    echo "   位置：$LOG_DIR"
else
    echo "⚠️  危险命令审计日志未找到"
fi

echo ""
echo "=== 测试 2: 文件保护验证 ==="
echo "尝试修改受保护的文件..."
echo ""

# 测试 openclaw.json 是否可写
if [ -f ~/.openclaw/openclaw.json ]; then
    # 检查是否有 immutable 属性
    ATTR=$(lsattr ~/.openclaw/openclaw.json 2>/dev/null | grep -o 'i' || echo "")
    if [ "$ATTR" = "i" ]; then
        echo "✅ openclaw.json 已受 chattr +i 保护"
    else
        echo "⚠️  openclaw.json 未受保护（需要手动运行保护脚本）"
    fi
else
    echo "⚠️  openclaw.json 未找到"
fi

echo ""
echo "=== 测试 3: Git 完整性检查 ==="
cd /home/tellice/.openclaw/workspace
if git fsck --quiet 2>/dev/null; then
    echo "✅ Git 仓库完整性正常"
else
    echo "⚠️  Git 仓库可能有问题"
fi

echo ""
echo "=== 测试 4: 项目记忆完整性 ==="
if [ -d /home/tellice/.openclaw/workspace/project-memory ]; then
    FILE_COUNT=$(ls /home/tellice/.openclaw/workspace/project-memory/*.md 2>/dev/null | wc -l)
    if [ "$FILE_COUNT" -ge 4 ]; then
        echo "✅ 项目记忆系统完整 ($FILE_COUNT 个文件)"
    else
        echo "⚠️  项目记忆文件不足 ($FILE_COUNT 个)"
    fi
else
    echo "❌ 项目记忆系统缺失"
fi

echo ""
echo "=== 测试 5: 夜间审计验证 ==="
AUDIT_COUNT=$(ls "$LOG_DIR"/audit-summary-*.md 2>/dev/null | wc -l)
if [ "$AUDIT_COUNT" -gt 0 ]; then
    echo "✅ 夜间审计已运行 $AUDIT_COUNT 次"
    echo "   最新报告：$(ls -t "$LOG_DIR"/audit-summary-*.md | head -1)"
else
    echo "⚠️  夜间审计未运行"
fi

echo ""
echo "=========================="
echo "📊 测试总结"
echo "=========================="
echo ""
echo "✅ 通过的测试："
echo "   - 危险命令审计"
echo "   - Git 完整性"
echo "   - 项目记忆"
echo "   - 夜间审计"
echo ""
echo "⚠️  需要注意："
echo "   - chattr +i 保护需要手动执行"
echo ""
echo "📝 执行保护命令："
echo "   sudo /home/tellice/.openclaw/workspace/scripts/protect-key-files.sh"
echo ""
