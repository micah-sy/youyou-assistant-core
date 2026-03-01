#!/bin/bash
# 🌤️ 悠悠的每日天气推送脚本
# 用法：./scripts/daily-weather.sh

set -e

# 获取用户 QQ OpenID
QQ_OPENID="8B28BE9D5828C43FCED5999970E998D2"
DATE=$(date '+%Y-%m-%d %H:%M')

echo "[$DATE] 开始发送天气推送..." >> /home/admin/.openclaw/logs/weather.log

# 获取天气信息
WEATHER=$(curl -s "wttr.in/?format=%l:+%c+%t+%h+%w" 2>/dev/null || echo "天气数据获取失败")

echo "[$DATE] 天气数据：$WEATHER" >> /home/admin/.openclaw/logs/weather.log

# 使用 OpenClaw 发送 QQ 消息
# 注意：需要通过 OpenClaw 的 message 工具发送，这里只是记录日志
# 实际发送由 OpenClaw 的 cron 系统处理

cat > /tmp/weather-message.txt << WEOF
🌤️ 悠悠的每日天气推送

$WEATHER

穿衣建议：根据天气情况调整着装哦～
WEOF

echo "[$DATE] 天气推送完成" >> /home/admin/.openclaw/logs/weather.log
