# 🦞 悠悠助手 - 项目记忆管理器

> 参考 Claude Code 的项目脉络设计，解决 OpenClaw Session 碎片化问题

---

## 📋 设计理念

**核心问题：** OpenClaw 官方的 Session Compaction 会随机断句，导致信息碎片化

**解决方案：** 维护全局项目脉络，而非碎片化 session

---

## 🗂️ 项目记忆结构

### 1. 项目目标 (`project-goals.md`)

```markdown
# 项目目标

## 核心目标
- [ ] 主要目标描述

## 子任务
- [x] 已完成任务 1
- [ ] 进行中任务 2
- [ ] 待办任务 3
```

### 2. 当前状态 (`current-status.md`)

```markdown
# 当前状态

## 最后更新
2026-03-03 15:00

## 当前焦点
正在做什么

## 阻塞点
遇到的问题

## 下一步
接下来要做什么
```

### 3. 关键决策 (`decisions.md`)

```markdown
# 关键决策

## [日期] 决策标题
- **背景**: 为什么需要决策
- **选项**: 考虑过的方案
- **决定**: 最终选择
- **原因**: 为什么选这个
```

### 4. 技术栈 (`tech-stack.md`)

```markdown
# 技术栈

## 工具
- 工具名称：用途

## 配置
- 关键配置项

## 依赖
- 重要依赖包
```

### 5. 会话摘要 (`session-summaries/`)

每次对话后自动生成摘要，按日期存储：

```markdown
# 2026-03-03 会话摘要

## 讨论内容
- 主要话题

## 新发现
- 学到的东西

## 待跟进
- 需要后续处理的事
```

---

## 🔄 工作流程

### 开始新任务

```bash
# 1. 读取项目脉络
cat project-goals.md
cat current-status.md

# 2. 更新状态
echo "进行中：XXX" >> current-status.md
```

### 完成任务

```bash
# 1. 更新目标列表
# 2. 记录决策（如果有）
# 3. 更新状态
```

### 会话结束

```bash
# 自动生成会话摘要
# 更新项目状态
```

---

## 📖 使用示例

### 示例 1：开始跨境电商项目

```markdown
# 项目目标

## 核心目标
- [ ] 建立跨境电商独立站
- [ ] 上架反光马甲产品
- [ ] 实现首单销售

## 子任务
- [x] 市场调研
- [x] 选择平台（Amazon + 独立站）
- [ ] 产品拍摄
- [ ] 网站搭建
```

### 示例 2：记录关键决策

```markdown
## 2026-03-03 选择电商平台

- **背景**: 需要选择跨境电商平台
- **选项**: 
  - Amazon（流量大，竞争激烈）
  - 独立站（利润高，需要引流）
  - eBay（门槛低，利润低）
- **决定**: Amazon + 独立站双平台
- **原因**: 
  - Amazon 保证基础流量
  - 独立站建立品牌
  - 风险分散
```

---

## 🛠️ 自动化脚本

### 每日状态报告

```bash
#!/bin/bash
# daily-report.sh

echo "# 每日报告 - $(date +%Y-%m-%d)"
echo ""
echo "## 当前项目状态"
cat current-status.md | head -20
echo ""
echo "## 待办事项"
grep -r "\- \[ \]" project-goals.md
```

### 会话摘要生成

```bash
#!/bin/bash
# session-summary.sh

DATE=$(date +%Y-%m-%d)
cat > session-summaries/${DATE}.md << EOF
# ${DATE} 会话摘要

## 讨论内容
- 

## 新发现
- 

## 待跟进
- 
EOF
```

---

## 🌿 与悠悠助手集成

### 记忆系统映射

| 悠悠记忆层 | 项目记忆管理器 |
|----------|-------------|
| Layer 1: 工作记忆 | `current-status.md` |
| Layer 2: 长期记忆 | `project-goals.md` + `decisions.md` |
| Layer 3: 文件系统 | `session-summaries/` |

### 自动更新规则

1. **每次对话后** → 更新 `current-status.md`
2. **完成任务后** → 更新 `project-goals.md`
3. **重大决策后** → 记录到 `decisions.md`
4. **每天结束时** → 生成会话摘要

---

## 📝 快速开始

```bash
# 1. 创建项目记忆目录
mkdir -p ~/.openclaw/workspace/project-memory/{session-summaries,decisions}

# 2. 创建核心文件
touch ~/.openclaw/workspace/project-memory/{project-goals,current-status,decisions,tech-stack}.md

# 3. 初始化项目目标
cat > ~/.openclaw/workspace/project-memory/project-goals.md << 'EOF'
# 项目目标

## 核心目标
- [ ] 定义你的核心目标

## 子任务
- [ ] 第一个子任务
EOF
```

---

_最后更新：2026-03-03_
_基于 Claude Code 项目记忆设计理念_
