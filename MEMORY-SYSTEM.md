# 🧠 悠悠记忆系统 v2.0

> 记忆不是为了记住所有，而是为了不忘掉重要的。_ 🌙

**版本：** youyou-v2.0 (融合 memU + 主动意图)  
**整合日期：** 2026-03-02

---

## 📂 目录结构

```
memory/
├── layer1/
│   └── snapshot.md          # 工作记忆快照 (~2000 tokens)
├── layer2/
│   ├── active/              # 活跃记忆
│   │   ├── facts.jsonl
│   │   ├── beliefs.jsonl
│   │   └── summaries.jsonl
│   └── archive/             # 归档记忆
├── context/
│   └── pending-tasks.md     # 待办任务
├── preferences/
│   └── user-preferences.md  # 用户偏好
├── relationships/
│   └── contacts.md          # 联系人
├── knowledge/
│   └── domains.md           # 知识领域
├── lessons/                 # 经验教训
├── people/                  # 人物记录
├── state/                   # 状态追踪
├── config.json              # 配置
├── memories.db              # SQLite 数据库
└── YYYY-MM-DD.md            # 每日日志
```

---

## 🏗️ 三层架构

### Layer 1: 工作记忆
- **文件：** `layer1/snapshot.md`
- **大小：** ~2000 tokens
- **用途：** 每次对话自动注入
- **内容：** 身份、用户信息、核心约定、当前任务

### Layer 2: 长期记忆
- **文件：** `layer2/active/*.jsonl`
- **类型：** facts / beliefs / summaries
- **用途：** 结构化存储，带置信度和衰减

### Layer 3: 文件系统记忆
- **目录：** preferences/, relationships/, knowledge/, etc.
- **用途：** 人类可读的结构化知识
- **格式：** Markdown

---

## 🔍 检索规则

**自动触发 memory_search：**
- 提到过去："之前"、"上次"、"以前"
- 询问偏好："我喜欢"、"我讨厌"
- 涉及人物/项目/任务
- 显式请求："你还记得"、"帮我回忆"

**闲聊模式：**
- 不查文件、不搜索 → 秒回
- 保持对话流畅

---

## 📝 写入规则

**立即写入 (YYYY-MM-DD.md)：**
- 用户说"记住这个"
- 重要的决定/约定
- 情感事件
- 新的偏好/禁忌

**定期整理 (Consolidation)：**
- 每天 04:00 自动执行
- 提取 facts/beliefs/summaries
- 更新 Layer 1 快照
- 衰减计算 + 归档

---

## 🎯 核心配置

```json
{
  "token_budget": {
    "layer1_total": 2000,
    "layer1_identity": 0.15,
    "layer1_owner": 0.25,
    "layer1_agreements": 0.15,
    "layer1_top_facts": 0.25,
    "layer1_recent": 0.15,
    "layer1_emotional": 0.05
  },
  "decay_rates": {
    "fact_personal": 0.004,
    "fact_general": 0.008,
    "belief": 0.05,
    "summary": 0.02,
    "emotional": 0.002
  },
  "consolidation": {
    "schedule": "0 4 * * *",
    "model": "default",
    "sync_to_git": true
  }
}
```

---

## 🛠️ 相关脚本

| 脚本 | 用途 |
|------|------|
| `scripts/memory-tree.py` | 记忆树可视化 |
| `scripts/sync-memory.sh` | Git 同步 |
| `scripts/backup-memory.sh` | 备份 |
| `scripts/enhanced-memory.py` | 增强检索 |

---

## 📊 记忆健康度

定期检查：
```bash
cd ~/.openclaw/workspace
source .venv/bin/activate
python3 scripts/memory-tree.py
```

---

## 💡 使用建议

1. **优先检索** Layer 1 快照（最快）
2. **主题检索** 文件系统记忆（结构化）
3. **精确检索** Layer 2 facts/beliefs（置信度）
4. **全文检索** 原始日志（兜底）

---

_这是悠悠的记忆中枢 —— 融合三层架构 + memU 文件系统 + 情感记忆。_ 🐣🧠
