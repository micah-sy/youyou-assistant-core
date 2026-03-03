# 技术栈

> 最后更新：2026-03-03

---

## 🤖 AI 框架

| 工具 | 版本 | 用途 |
|------|------|------|
| OpenClaw | v2026.3.2 | 主框架 |
| Node.js | v22.22.0 | 运行时 |
| bailian/qwen3.5-plus | - | AI 模型 |

---

## 🌐 通信集成

| 工具 | 状态 | 说明 |
|------|------|------|
| Telegram Bot | ✅ @Tellice555_bot | 主要交互界面 |
| Gateway | ✅ systemd 自动启动 | 端口 18789 |

---

## 🦎 反检测工具

| 工具 | 位置 | 状态 |
|------|------|------|
| playwright-bot-bypass | `tools/playwright-bot-bypass/` | ✅ 可用 |
| Camofox Browser | `skills/camofox-browser/` | ⚠️ 需配置 |
| jina-cli | 系统命令 | ✅ 可用 |

---

## 🧠 记忆系统

| 组件 | 位置 | 状态 |
|------|------|------|
| Layer 1 快照 | `memory/layer1/snapshot.md` | ✅ |
| Layer 2 活跃 | `memory/layer2/active/` | ✅ |
| Layer 3 文件 | `memory/preferences/` 等 | ✅ |
| EverMemOS | `EverMemOS/` | ⏳ 配置中 |
| 项目记忆 | `project-memory/` | ✅ 已创建 |

---

## 🛡️ 安全工具

| 工具 | 状态 | 说明 |
|------|------|------|
| 慢雾安全指南 | ⏳ 待部署 | v2.7 |
| Git 备份 | ✅ | `micah-sy/youyou-assistant-core` |
| 夜间审计 | ⏳ 待配置 | 13 项指标 |

---

## 📦 关键依赖

```bash
# Node.js 全局包
openclaw@2026.3.2
rebrowser-playwright

# Python 包 (EverMemOS)
fastapi
uvicorn
pymongo
elasticsearch
milvus
redis
```

---

## 🔧 配置文件

| 文件 | 位置 |
|------|------|
| OpenClaw 配置 | `~/.openclaw/openclaw.json` |
| systemd 服务 | `~/.config/systemd/user/openclaw-gateway.service` |
| SSH 密钥 | `~/.ssh/id_ed25519` |
| Git 远程 | `git@github.com:micah-sy/youyou-assistant-core.git` |

---

## 📊 系统资源

| 项目 | 用量 |
|------|------|
| 内存 | 3.8GB (已用 2.1GB) |
| 磁盘 | 79GB (已用 15GB) |
| 工作空间 | ~50MB |

---

## 🔑 API 密钥

| 服务 | 状态 |
|------|------|
| Bailian (通义千问) | ✅ 已配置 |
| Telegram Bot | ✅ 已配置 |
| GitHub | ✅ SSH 密钥 |
| Jina AI | ⚠️ 需要 API Key |
| Brave Search | ❌ 未配置 |

---
