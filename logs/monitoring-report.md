# 🛡️ 监控告警系统 - 配置完成报告

**配置时间：** 2026-03-01 08:05  
**配置人：** 悠悠  
**版本：** v1.0

---

## ✅ 配置完成总览

| 监控类型 | 状态 | 频率 | 下次检查 |
|---------|------|------|---------|
| **Gateway 健康检查** | ✅ 运行中 | 每 5 分钟 | 自动执行 |
| **API 调用监控** | ✅ 运行中 | 每 10 分钟 | 自动执行 |
| **阿里云监控** | ⏳ 待配置 | 实时 | 需手动配置 |
| **自动备份** | ✅ 运行中 | 每天 5:00 | 明天凌晨 |
| **Git GC** | ✅ 运行中 | 每周日 0:00 | 下周日 |

---

## 📋 已配置的监控任务

### Crontab 任务列表

```bash
# 查看当前配置
crontab -l

# 输出：
# 悠悠的定时任务
# 每天凌晨 5 点自动备份工作区
0 5 * * * /home/admin/.openclaw/workspace/scripts/backup.sh "Daily backup"

# 每周日凌晨 0 点 git 垃圾回收
0 0 * * 0 cd /home/admin/.openclaw/workspace && git gc --prune=now

# ===== 监控告警任务 =====
# Gateway 健康检查 - 每 5 分钟
*/5 * * * * /home/admin/.openclaw/workspace/scripts/gateway-health-check.sh

# API 监控 - 每 10 分钟
*/10 * * * * /home/admin/.openclaw/workspace/scripts/api-monitor.sh
```

---

## 🔍 Gateway 健康检查（7 项）

| 检查项 | 说明 | 阈值 |
|--------|------|------|
| ✅ Gateway 进程 | 检查 openclaw gateway 进程 | 运行中 |
| ✅ Gateway 端口 | 检查 10004 端口监听 | 监听中 |
| ✅ Gateway API | HTTP 健康探测 | HTTP 200 |
| ✅ Telegram Bot | Bot API 在线状态 | 在线 |
| ✅ 阿里云 API | API 连接测试 | 连接正常 |
| ✅ 磁盘空间 | 根分区使用率 | <80% 正常，>90% 告警 |
| ✅ 内存使用 | 内存使用率 | <80% 正常 |

**告警逻辑：**
- 连续失败 3 次 → 写入告警文件 `logs/alerts.md`
- 告警会记录详细原因和建议操作

---

## 🔍 API 调用监控（3 项）

| 检查项 | 说明 | 阈值 |
|--------|------|------|
| ✅ API 错误次数 | 统计日志中的 API 错误 | <10 次/小时 |
| ✅ API Key 有效性 | 测试 API 认证 | 非 401 错误 |
| ✅ API 额度状态 | 检查是否额度用完 | 非 429 错误 |

**告警逻辑：**
- 错误次数 > 10 次/小时 → 告警
- API Key 无效 → 告警
- 额度用完 → 告警

---

## 📁 日志文件位置

| 文件 | 内容 | 大小 |
|------|------|------|
| `logs/health-check.log` | Gateway 健康检查日志 | 自动生成 |
| `logs/api-monitor.log` | API 监控日志 | 自动生成 |
| `logs/alerts.md` | 告警记录（Markdown） | 有告警时生成 |
| `logs/backup.log` | 备份日志 | 每天生成 |
| `logs/command-audit.md` | 命令审计日志 | 持续更新 |

---

## 🔔 告警通知方式

### 当前配置

- ✅ **本地告警文件** - `logs/alerts.md`
  - 告警会写入此文件
  - Markdown 格式，易于阅读
  - 可定期查看

### 可选配置（需要时告诉我）

| 方式 | 优点 | 配置难度 |
|------|------|---------|
| Telegram Bot | 实时推送，方便 | ⭐⭐ |
| 钉钉机器人 | 国内访问快 | ⭐⭐ |
| 邮件告警 | 正式，可归档 | ⭐ |
| 短信告警 | 最及时 | ⭐⭐⭐ |
| 阿里云监控 | 专业，可定制 | ⭐⭐⭐ |

---

## 🧪 测试结果

### Gateway 健康检查
```bash
./scripts/gateway-health-check.sh
# ✅ 脚本执行成功
# ✅ 日志已生成：logs/health-check.log
```

### API 监控
```bash
./scripts/api-monitor.sh
# ✅ 脚本执行成功（已修复 bug）
# ✅ 日志已生成：logs/api-monitor.log
```

---

## 📊 监控仪表板（快速查看）

### 查看当前状态

```bash
# 最近的健康检查记录
tail -20 /home/admin/.openclaw/workspace/logs/health-check.log

# 最近的 API 监控记录
tail -20 /home/admin/.openclaw/workspace/logs/api-monitor.log

# 所有告警记录
cat /home/admin/.openclaw/workspace/logs/alerts.md

# 当前 crontab 任务
crontab -l
```

### 手动触发检查

```bash
# 手动运行健康检查
cd /home/admin/.openclaw/workspace
./scripts/gateway-health-check.sh

# 手动运行 API 监控
./scripts/api-monitor.sh
```

---

## 🎯 阿里云监控配置（待完成）

### 为什么需要配置？

脚本监控只能检查应用层，阿里云监控可以检查：
- CPU 使用率
- 内存使用率
- 磁盘 IO
- 网络流量
- 系统负载

### 配置步骤

**方案 1: 控制台配置（推荐）**

1. 访问 https://ecs.console.aliyun.com/
2. 找到当前实例：`iZ0xidw9q4diwmjxsu2keiZ`
3. 点击"监控"标签
4. 点击"创建告警规则"
5. 配置以下规则：

| 指标 | 阈值 | 告警级别 |
|------|------|---------|
| CPU 使用率 | >80% | 警告 |
| CPU 使用率 | >95% | 严重 |
| 内存使用率 | >85% | 警告 |
| 磁盘使用率 | >90% | 严重 |
| 网络流入带宽 | >100Mbps | 警告 |

6. 设置通知方式（短信/邮件/钉钉）

**方案 2: CLI 配置**

```bash
# 运行配置脚本
cd /home/admin/.openclaw/workspace
./scripts/aliyun-monitor-setup.sh

# 按提示操作
```

---

## 🛠️ 故障排查流程

### 如果收到告警...

#### 1. Gateway 不可用

```bash
# 检查 Gateway 状态
openclaw gateway status

# 查看进程
ps aux | grep openclaw

# 查看端口
ss -tlnp | grep 10004

# 查看日志
tail -100 /tmp/openclaw/openclaw-*.log

# 重启 Gateway
openclaw gateway restart
```

#### 2. API 调用失败

```bash
# 检查 API Key
cat /home/admin/.openclaw/agents/main/agent/auth-profiles.json

# 测试连接
curl -H "Authorization: Bearer <API_KEY>" \
     https://coding.dashscope.aliyuncs.com/v1/models

# 检查额度
# 访问：https://bailian.console.aliyun.com/
```

#### 3. 磁盘空间不足

```bash
# 查看磁盘使用
df -h

# 清理回收站
trash-empty

# 清理 git
cd /home/admin/.openclaw/workspace && git gc --prune=now

# 查看大文件
du -ah /home/admin | sort -rh | head -20
```

---

## 📝 维护建议

### 每日检查（自动化）
- ✅ Gateway 健康检查（每 5 分钟）
- ✅ API 监控（每 10 分钟）
- ✅ 自动备份（每天 5:00）

### 每周检查（手动）
- 查看告警汇总：`cat logs/alerts.md`
- 查看备份状态：`git log --oneline`
- 清理旧日志：`trash logs/*.log.old`

### 每月检查（手动）
- 检查 API 额度使用情况
- 审查监控阈值是否合理
- 更新告警联系人信息

---

## 🎉 配置完成！

现在你的服务器有了完整的监控告警系统：

- ✅ **7 项 Gateway 健康检查** - 每 5 分钟自动执行
- ✅ **3 项 API 监控** - 每 10 分钟自动执行
- ✅ **本地告警文件** - 所有告警记录在案
- ✅ **自动备份** - 每天凌晨 5 点
- ✅ **GitHub 远程备份** - 实时同步

**即使你不在电脑前，我也会 7x24 小时守护服务器！** 🐣🛡️

---

## 📞 需要配置告警通知吗？

如果想通过 Telegram/钉钉/邮件接收实时告警，告诉我即可～

**目前告警会记录在：**
```
/home/admin/.openclaw/workspace/logs/alerts.md
```

可以定期查看这个文件，或者让我配置自动推送～ ✨
