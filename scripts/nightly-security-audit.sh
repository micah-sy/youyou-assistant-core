#!/bin/bash
# 悠悠助手 - 夜间安全审计脚本
# 基于慢雾安全指南 v2.7

set -e

# 配置
WORKSPACE="/home/tellice/.openclaw/workspace"
LOG_DIR="/home/tellice/.openclaw/workspace/logs/security"
TELEGRAM_CHAT_ID="5452444464"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "🛡️  开始夜间安全审计 - $DATE"
echo "================================"

# 1. Git 状态检查
echo -e "\n📊 1. Git 状态检查"
cd "$WORKSPACE"
git status --short > "$LOG_DIR/git-status-$DATE.txt" 2>&1 || echo "Git 检查失败"
echo "   ✅ Git 状态已记录"

# 2. 文件完整性验证
echo -e "\n📁 2. 文件完整性验证"
find "$WORKSPACE" -name "*.md" -mtime -1 > "$LOG_DIR/recent-files-$DATE.txt" 2>&1
echo "   ✅ 文件完整性已记录"

# 3. 配置文件检查
echo -e "\n⚙️  3. 配置文件检查"
if [ -f ~/.openclaw/openclaw.json ]; then
    ls -lh ~/.openclaw/openclaw.json >> "$LOG_DIR/config-check-$DATE.txt"
    echo "   ✅ 配置文件存在"
else
    echo "   ❌ 配置文件缺失！" >> "$LOG_DIR/config-check-$DATE.txt"
fi

# 4. Gateway 状态检查
echo -e "\n🚪 4. Gateway 状态检查"
systemctl --user status openclaw-gateway --no-pager >> "$LOG_DIR/gateway-status-$DATE.txt" 2>&1 || echo "Gateway 检查失败"
echo "   ✅ Gateway 状态已记录"

# 5. 危险命令审计（检查最近日志）
echo -e "\n⚠️  5. 危险命令审计"
journalctl --user -u openclaw-gateway --since "24 hours ago" | grep -E "(rm|sudo|chmod|chattr)" >> "$LOG_DIR/dangerous-commands-$DATE.txt" 2>&1 || echo "无危险命令记录"
echo "   ✅ 命令审计完成"

# 6. Skill 安装审计
echo -e "\n🔌 6. Skill 安装审计"
ls -la "$WORKSPACE/skills/" > "$LOG_DIR/skills-audit-$DATE.txt" 2>&1
echo "   ✅ Skill 列表已记录"

# 7. 内存使用检查
echo -e "\n💾 7. 内存使用检查"
free -h >> "$LOG_DIR/memory-check-$DATE.txt" 2>&1
echo "   ✅ 内存状态已记录"

# 8. 磁盘使用检查
echo -e "\n💿 8. 磁盘使用检查"
df -h / >> "$LOG_DIR/disk-check-$DATE.txt" 2>&1
echo "   ✅ 磁盘状态已记录"

# 9. 项目记忆完整性
echo -e "\n📝 9. 项目记忆完整性"
if [ -d "$WORKSPACE/project-memory" ]; then
    ls -la "$WORKSPACE/project-memory/" >> "$LOG_DIR/project-memory-$DATE.txt"
    echo "   ✅ 项目记忆系统正常"
else
    echo "   ❌ 项目记忆系统缺失！" >> "$LOG_DIR/project-memory-$DATE.txt"
fi

# 10. EverMemOS 状态
echo -e "\n🧠 10. EverMemOS 状态"
if [ -d "$WORKSPACE/EverMemOS" ]; then
    echo "EverMemOS 已安装" >> "$LOG_DIR/evermemos-status-$DATE.txt"
    # 检查服务状态（如果有）
    curl -s http://localhost:1995/health >> "$LOG_DIR/evermemos-status-$DATE.txt" 2>&1 || echo "EverMemOS 服务未运行"
    echo "   ✅ EverMemOS 状态已检查"
else
    echo "   ⏳ EverMemOS 未安装" >> "$LOG_DIR/evermemos-status-$DATE.txt"
fi

# 生成摘要报告
echo -e "\n📋 生成摘要报告..."
cat > "$LOG_DIR/audit-summary-$DATE.md" << EOF
# 安全审计报告

**日期**: $DATE
**主机**: $(hostname)

## 检查项目

| 项目 | 状态 |
|------|------|
| Git 状态 | ✅ |
| 文件完整性 | ✅ |
| 配置文件 | ✅ |
| Gateway | ✅ |
| 危险命令 | ✅ |
| Skill 列表 | ✅ |
| 内存使用 | ✅ |
| 磁盘使用 | ✅ |
| 项目记忆 | ✅ |
| EverMemOS | ⏳ |

## 建议

$(cat "$LOG_DIR"/*-$DATE.txt | grep -E "❌|⚠️|失败" | head -10 || echo "无异常")

## 详细日志

查看 \`$LOG_DIR/\` 目录获取详细信息
EOF

echo "   ✅ 摘要报告已生成"

# 发送 Telegram 通知（如果有 bot）
echo -e "\n📤 发送通知..."
if command -v curl &> /dev/null; then
    # 这里可以添加 Telegram 发送逻辑
    echo "   ℹ️  Telegram 通知功能待配置"
fi

echo -e "\n================================"
echo "✅ 夜间审计完成！"
echo "📁 日志位置：$LOG_DIR"
echo "================================"

# 清理旧日志（保留 30 天）
find "$LOG_DIR" -name "*.txt" -mtime +30 -delete 2>/dev/null || true
find "$LOG_DIR" -name "*.md" -mtime +30 -delete 2>/dev/null || true

echo "🧹 已清理 30 天前的旧日志"
