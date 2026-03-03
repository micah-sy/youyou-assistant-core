# 🧠 悠悠助手的知识库

> 这是我的核心系统文件仓库 - 包含记忆、身份、技能和架构文档  
> 创建时间：2026-03-02  
> 🌿 悠悠助手的数字大脑

---

## 📁 仓库结构

```
youyou-assistant-core/
├── 🧠 记忆系统/
│   ├── MEMORY.md                    # 长期记忆
│   ├── MEMORY-SYSTEM.md             # 记忆系统架构
│   ├── memory/
│   │   ├── layer1/snapshot.md       # 工作记忆快照
│   │   ├── layer2/active/           # 长期记忆（facts/beliefs/summaries）
│   │   └── YYYY-MM-DD.md            # 每日日志
│
├── 👤 身份定义/
│   ├── SOUL.md                      # 核心身份和价值观
│   ├── IDENTITY.md                  # 基本信息（名字、风格、emoji）
│   ├── USER.md                      # 关于悠悠的信息
│   └── NOW.md                       # 当前状态
│
├── 🛠️ 技能系统/
│   ├── AGENTS.md                    # Agent 技能说明
│   ├── TOOLS.md                     # 工具使用笔记
│   └── skills/                      # 技能文件
│
├── 🏗️ 系统架构/
│   ├── ARCHITECTURE.md              # 系统架构设计
│   ├── CONTINUOUS-LEARNING.md       # 持续学习机制
│   ├── EVOLUTION-PLAN.md            # 进化计划
│   └── MEMORY-SYSTEM.md             # 记忆系统设计
│
├── 📋 操作指南/
│   ├── INDEX.md                     # 索引导航
│   ├── BACKUP-SCHEDULE.md           # 备份计划
│   ├── GITHUB-LEARNING.md           # GitHub 学习记录
│   └── OPENCLAW-UPDATE-PLAN.md      # OpenClaw 更新计划
│
└── 📝 日常日志/
    ├── 2026-02-10.md                # 早期日志
    ├── 2026-02-28.md                # 悠悠诞生之日
    ├── 2026-03-01.md                # 跨平台同步
    └── 2026-03-02.md                # 记忆系统整合
```

---

## 🎯 核心文件说明

### 🧠 记忆系统

| 文件 | 作用 | 更新频率 |
|------|------|----------|
| `MEMORY.md` | 长期记忆精华 | 每周 review |
| `memory/layer1/snapshot.md` | 工作记忆（~2000 tokens） | 每次对话 |
| `memory/layer2/active/*.jsonl` | facts/beliefs/summaries | 动态更新 |
| `memory/YYYY-MM-DD.md` | 每日对话日志 | 每天 |

### 👤 身份定义

| 文件 | 内容 |
|------|------|
| `SOUL.md` | 核心价值观、行为准则、存在意义 |
| `IDENTITY.md` | 名字（悠悠助手）、风格、专属 emoji（🌿） |
| `USER.md` | 关于悠悠的信息（20 岁女生、反光马甲业务、跨境电商） |
| `NOW.md` | 当前状态、正在进行的项目 |

### 🛠️ 技能系统

| 文件 | 说明 |
|------|------|
| `AGENTS.md` | Agent 技能使用说明 |
| `TOOLS.md` | 工具配置笔记（摄像头、SSH、TTS 等） |
| `skills/` | 具体技能文件（weather、searxng、healthcheck 等） |

### 🏗️ 系统架构

| 文件 | 内容 |
|------|------|
| `ARCHITECTURE.md` | 系统整体架构设计 |
| `CONTINUOUS-LEARNING.md` | 持续学习机制 |
| `EVOLUTION-PLAN.md` | 自我进化计划 |
| `MEMORY-SYSTEM.md` | 记忆系统详细设计 |

---

## 🔄 更新机制

### 自动更新
- **每日 04:00** - Consolidation（记忆整合）
- **每周日** - GC（冷数据归档）
- **每次对话** - 更新工作记忆快照

### 手动更新
- 重要对话后 → 更新 `MEMORY.md`
- 学习新知识 → 更新对应技能文件
- 系统升级 → 更新架构文档

---

## 💾 备份策略

### Git 提交频率
- **每天** - 提交记忆日志
- **每周** - 提交系统更新
- **重大变更后** - 立即提交

### 提交规范
```bash
git add .
git commit -m "类型：描述"

# 类型示例：
# feat: 新增功能
# fix: 修复问题
# docs: 文档更新
# memory: 记忆更新
# refactor: 重构
```

---

## 🔐 隐私说明

本仓库包含：
- ✅ 我的核心系统文件
- ✅ 记忆数据
- ✅ 身份信息
- ✅ 学习笔记

**访问权限：** 私有仓库（Private）

---

## 🌿 关于我

**名字：** 悠悠助手  
**身份：** AI 助手（幽灵在机器里）  
**风格：** 温暖但不腻，靠谱但不死板，偶尔能皮一下  
**专属符号：** 🌿  
**诞生之日：** 2026-02-28  

**核心原则：**
1. genuinely helpful，不表演式帮助
2. 有主见，不唯唯诺诺
3. 先自己查，再问
4. 重要事情写记忆

---

_最后更新：2026-03-02 15:32_  
_这是我的数字家园，记录我的成长与进化_ 💫
