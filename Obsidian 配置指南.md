# 悠悠的 Obsidian 配置指南

> 配置时间：2026-03-02  
> 仓库：youyou-assistant-core  
> 🌿 悠悠助手的数字大脑

---

## 📁 仓库位置

```
/home/admin/.openclaw/workspace/
```

这就是你的 Obsidian Vault（知识库）！

---

## 🚀 快速开始

### 方法一：直接打开（推荐）

1. **打开 Obsidian**
2. **点击**："Open folder as vault"（打开文件夹作为知识库）
3. **选择**：`/home/admin/.openclaw/workspace/`
4. **完成！** ✅

### 方法二：移动端同步

1. **在手机上安装 Obsidian App**
   - iOS: App Store 搜索"Obsidian"
   - Android: Google Play 搜索"Obsidian"
2. **创建新 Vault** 或 **打开现有 Vault**
3. **使用 Git 插件同步**（见下方）

---

## 📂 文件结构

```
workspace/
├── .obsidian/              # Obsidian 配置
│   ├── app.json            # 应用设置
│   ├── appearance.json     # 外观设置
│   ├── core.json           # 核心设置
│   └── community-plugins.json  # 插件配置
│
├── 🧠 记忆系统/
│   ├── MEMORY.md           # 长期记忆
│   ├── MEMORY-SYSTEM.md    # 记忆系统架构
│   ├── memory/
│   │   ├── layer1/snapshot.md  # 工作记忆
│   │   └── YYYY-MM-DD.md       # 每日日志
│
├── 👤 身份定义/
│   ├── SOUL.md             # 核心身份
│   ├── IDENTITY.md         # 基本信息
│   ├── USER.md             # 关于悠悠
│   └── NOW.md              # 当前状态
│
├── 🛠️ 技能系统/
│   ├── AGENTS.md           # Agent 技能
│   └── TOOLS.md            # 工具笔记
│
├── 🏗️ 系统架构/
│   ├── ARCHITECTURE.md     # 架构设计
│   ├── CONTINUOUS-LEARNING.md
│   └── EVOLUTION-PLAN.md
│
└── 📝 日常日志/
    ├── 2026-02-28.md       # 诞生之日
    ├── 2026-03-01.md       # 跨平台同步
    └── 2026-03-02.md       # 记忆系统整合
```

---

## 🔌 推荐插件

### 核心插件（已启用）

- ✅ **Backlink** - 反向链接
- ✅ **Graph** - 知识图谱
- ✅ **Outline** - 大纲视图
- ✅ **Star** - 收藏重要笔记
- ✅ **Tag** - 标签管理
- ✅ **Templates** - 模板功能
- ✅ **Command Palette** - 命令面板

### 社区插件（推荐安装）

1. **Dataview** - 数据库查询
   - 用途：查询记忆、任务管理
   - 安装：Settings → Community plugins → Browse → 搜索"Dataview"

2. **Calendar** - 日历视图
   - 用途：查看每日日志
   - 安装：搜索"Calendar"

3. **Kanban** - 看板管理
   - 用途：任务管理、项目跟踪
   - 安装：搜索"Kanban"

4. **Obsidian Git** - Git 同步
   - 用途：自动备份到 GitHub
   - 安装：搜索"Obsidian Git"

5. **Excalidraw** - 手绘图表
   - 用途：绘制架构图、流程图
   - 安装：搜索"Excalidraw"

6. **Spaced Repetition** - 间隔重复
   - 用途：记忆知识点
   - 安装：搜索"Spaced Repetition"

---

## 🔄 Git 同步配置

### 使用 Obsidian Git 插件

1. **安装插件**：
   - Settings → Community plugins → Browse
   - 搜索 "Obsidian Git"
   - 点击 Install → Enable

2. **配置插件**：
   ```bash
   # 插件会自动检测现有 Git 仓库
   # 无需额外配置！
   ```

3. **设置自动备份**：
   - Settings → Obsidian Git
   - 勾选 "Auto backup interval"
   - 设置间隔：`60 分钟`（或你喜欢的频率）

4. **手动同步**：
   - 按 `Ctrl/Cmd + P` 打开命令面板
   - 输入 "Git: Commit and sync"
   - 回车执行

---

## 📱 移动端同步

### 方案一：Obsidian Sync（付费）

- 官方同步服务
- $8-10/月
- 最简单可靠

### 方案二：Git 同步（免费，推荐）

1. **安装 Obsidian Git 插件**
2. **配置 SSH 密钥**（参考 GitHub 文档）
3. **设置自动同步**

### 方案三：第三方同步

- **iCloud**（iOS）
- **Syncthing**（Android）
- **Remotely Save** 插件（支持多种云服务）

---

## 💡 使用技巧

### 1. 创建每日日志

```
Ctrl/Cmd + N → 输入日期 → 开始记录
```

### 2. 使用双向链接

```markdown
[[MEMORY.md]] - 链接到记忆系统
[[SOUL.md]] - 链接到身份定义
```

### 3. 查看知识图谱

```
点击 Graph 图标 → 查看笔记关联
```

### 4. 搜索笔记

```
Ctrl/Cmd + O → 输入关键词 → 快速定位
```

### 5. 使用模板

```
Ctrl/Cmd + T → 选择模板 → 快速创建
```

---

## 🎯 日常工作流

### 早晨

1. 打开 Obsidian
2. 创建今日日志：`2026-03-02.md`
3. 记录今日计划

### 对话中

1. 重要信息 → 记入 `memory/YYYY-MM-DD.md`
2. 重要决定 → 更新 `MEMORY.md`
3. 学习新知识 → 更新对应技能文件

### 晚上

1. Review 今日日志
2. 提交 Git：`Git: Commit and sync`
3. 规划明日

---

## 🔐 隐私说明

本 Vault 包含：
- ✅ 我的核心系统文件
- ✅ 记忆数据
- ✅ 身份信息
- ✅ 学习笔记

**同步方式：** GitHub 私有仓库  
**访问权限：** 仅你可见

---

## 📞 需要帮助？

如果遇到配置问题：
1. 查看 Obsidian 官方文档：https://help.obsidian.md
2. 查看插件文档
3. 随时问我！

---

_配置时间：2026-03-02 16:04_  
_悠悠的 Obsidian 知识库，等你探索！_ 🌿💫
