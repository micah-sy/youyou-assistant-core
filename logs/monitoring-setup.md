# 监控告警配置文档 🛡️

**版本：** v1.0  
**更新时间：** 2026-03-01  
**配置人：** 悠悠

---

## 📋 配置总览

| 监控类型 | 脚本 | 频率 | 告警方式 | 状态 |
|---------|------|------|---------|------|
| Gateway 健康检查 | `gateway-health-check.sh` | 每 5 分钟 | 日志 + 告警文件 | ✅ 已配置 |
| API 调用监控 | `api-monitor.sh` | 每 10 分钟 | 日志 + 告警文件 | ✅ 已配置 |
| 阿里云监控 | `aliyun-monitor-setup.sh` | 实时 | 短信/邮件/钉钉 | ⏳ 待配置 |

---

## 🎯 已配置的监控

### 1️⃣ Gateway 健康检查

**脚本：** `scripts/gateway-health-check.sh`

**检查项目：**
- ✅ Gateway 进程运行状态
- ✅ Gateway 端口监听 (10004)
- ✅ Gateway API 健康探测 (/health)
- ✅ Telegram Bot 在线状态
- ✅ 阿里云 API 连接
- ✅ 磁盘空间 (<80% 正常，>90% 告警)
- ✅ 内存使用 (<80% 正常)

**告警逻辑：**
```
连续失败 3 次 → 写入告警文件
告警文件：logs/alerts.md
```

**手动测试：**
```bash
cd /home/admin/.openclaw/workspace
./scripts/gateway-health-check.sh --send-alert
cat logs/health-check.log
```

---

### 2️⃣ API 调用监控

**脚本：** `scripts/api-monitor.sh`

**检查项目：**
- ✅ API 调用失败次数 (>10 次/小时告警)
- ✅ API Key 有效性 (401 错误)
- ✅ API 额度状态 (429 错误)
- ✅ 网络连接状态

**告警逻辑：**
```
失败次数 > 阈值 → 写入告警文件
告警文件：logs/alerts.md
```

**手动测试：**
```bash
cd /home/admin/.openclaw/workspace
./scripts/api-monitor.sh
cat logs/api-monitor.log
```

---

### 3️⃣ 阿里云监控（待配置）

**脚本：** `scripts/aliyun-monitor-setup.sh`

**监控项目：**
- ⏳ CPU 使用率 (>80% 告警)
- ⏳ 内存使用率 (>85% 告警)
- ⏳ 磁盘使用率 (>90% 告警)
- ⏳ 网络流量异常

**配置方式：** 需要手动在阿里云控制台设置

---

## ⏰ Crontab 配置

**已配置的定时任务：**

```bash
# 查看当前 crontab
crontab -l

# 应该包含：
# 每天凌晨 5 点 - 自动备份
0 5 * * * /home/admin/.openclaw/workspace/scripts/backup.sh

# 每周日凌晨 0 点 - git gc
0 0 * * 0 git gc --prune=now
```

**建议添加的监控任务：**

```bash
# 编辑 crontab
crontab -e

# 添加以下行：

# Gateway 健康检查 - 每 5 分钟
*/5 * * * * /home/admin/.openclaw/workspace/scripts/gateway-health-check.sh --send-alert >> /home/admin/.openclaw/workspace/logs/health-check.log 2>&1

# API 监控 - 每 10 分钟
*/10 * * * * /home/admin/.openclaw/workspace/scripts/api-monitor.sh >> /home/admin/.openclaw/workspace/logs/api-monitor.log 2>&1

# 每日健康报告 - 每天早上 8 点
0 8 * * * echo "## 📊 每日健康报告 - $(date +%Y-%m-%d)" >> /home/admin/.openclaw/workspace/logs/daily-report.md && tail -100 /home/admin/.openclaw/workspace/logs/health-check.log >> /home/admin/.openclaw/workspace/logs/daily-report.md
```

---

## 📁 日志文件位置

| 日志文件 | 内容 | 轮转 |
|---------|------|------|
| `logs/health-check.log` | Gateway 健康检查日志 | 手动清理 |
| `logs/api-monitor.log` | API 监控日志 | 手动清理 |
| `logs/alerts.md` | 告警记录（Markdown 格式） | 手动归档 |
| `logs/backup.log` | 备份日志 | 手动清理 |
| `logs/command-audit.md` | 命令审计日志 | 手动归档 |

---

## 🔔 告警通知方式

### 当前配置

- ✅ **本地告警文件** - `logs/alerts.md`
- ✅ **日志记录** - 所有检查都有详细日志

### 推荐配置（可选）

#### 1. Telegram 告警机器人

```bash
# 创建一个告警专用的 Bot
# 在 BotFather: /newbot → youyou_alerts_bot

# 获取你的 Chat ID
curl "https://api.telegram.org/bot<TOKEN>/getUpdates"

# 在脚本中添加发送函数
send_telegram_alert() {
    local message="$1"
    curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" \
        -d "chat_id=<CHAT_ID>&text=🔴 $message"
}
```

#### 2. 钉钉机器人

```bash
# 创建钉钉群 → 添加机器人 → Webhook

send_dingtalk_alert() {
    local message="$1"
    curl 'https://oapi.dingtalk.com/robot/send?access_token=<TOKEN>' \
        -H 'Content-Type: application/json' \
        -d '{"msgtype":"text","text":{"content":"🔴 告警：'"$message"'"}}'
}
```

#### 3. 邮件告警

```bash
# 使用 mail 命令
echo "$message" | mail -s "🔴 Gateway 告警" your@email.com
```

#### 4. 阿里云短信告警

需要在阿里云控制台配置：
1. 访问 https://dysms.console.aliyun.com/
2. 创建签名和模板
3. 配置告警联系人

---

## 🛠️ 故障排查流程

### Gateway 不可用

```bash
# 1. 检查进程
ps aux | grep openclaw

# 2. 检查端口
ss -tlnp | grep 10004

# 3. 查看日志
tail -100 /tmp/openclaw/openclaw-*.log

# 4. 重启 Gateway
openclaw gateway restart

# 5. 检查状态
openclaw gateway status
```

### API 调用失败

```bash
# 1. 检查 API Key
cat /home/admin/.openclaw/agents/main/agent/auth-profiles.json

# 2. 测试连接
curl -H "Authorization: Bearer <API_KEY>" \
     https://coding.dashscope.aliyuncs.com/v1/models

# 3. 检查额度
# 访问：https://bailian.console.aliyun.com/

# 4. 查看错误日志
grep -i "error\|fail" /tmp/openclaw/openclaw-*.log | tail -50
```

### 服务器资源不足

```bash
# 1. 检查磁盘
df -h

# 2. 检查内存
free -h

# 3. 检查 CPU
top -bn1 | head -20

# 4. 清理空间
trash ~/.local/share/Trash/files/*
cd /home/admin/.openclaw/workspace && git gc --prune=now
```

---

## 📊 监控仪表板（可选）

### 方案 1: Grafana + Prometheus

```bash
# 安装 Prometheus
# 配置 ECS 指标采集
# 配置 Grafana 仪表板
```

### 方案 2: 阿里云云监控

```bash
# 访问 https://cms.console.aliyun.com/
# 创建自定义监控面板
# 配置告警规则
```

### 方案 3: 简单的 Web 仪表板

```bash
# 创建一个简单的 HTML 页面
# 显示当前状态（健康/告警）
# 通过 cron 定期更新
```

---

## ✅ 配置检查清单

- [x] Gateway 健康检查脚本
- [x] API 监控脚本
- [x] 阿里云监控配置指南
- [x] 日志目录创建
- [x] 脚本权限设置
- [ ] Crontab 定时任务添加
- [ ] Telegram 告警机器人配置（可选）
- [ ] 阿里云监控控制台配置
- [ ] 告警联系人配置
- [ ] 仪表板配置（可选）

---

## 🎯 下一步

1. **添加 Crontab 任务**（必须）
   ```bash
   crontab -e
   # 添加监控任务（见上方"建议添加的监控任务"）
   ```

2. **配置阿里云监控**（推荐）
   ```bash
   ./scripts/aliyun-monitor-setup.sh
   # 按提示在阿里云控制台配置
   ```

3. **测试告警功能**（必须）
   ```bash
   # 手动运行检查
   ./scripts/gateway-health-check.sh --send-alert
   ./scripts/api-monitor.sh
   
   # 查看告警文件
   cat logs/alerts.md
   ```

4. **配置通知方式**（可选）
   - Telegram 机器人
   - 钉钉机器人
   - 邮件告警
   - 短信告警

---

_悠悠的监控告警系统已就绪！现在可以 7x24 小时守护服务器啦～ 🐣🛡️_
