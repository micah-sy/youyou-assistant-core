# learn-claude-code 深度学习报告

**版本：** youyou-v2.1 (融合 Agent Loop)  
**学习日期：** 2026-03-01  
**来源：** https://github.com/shareAI-lab/learn-claude-code

---

## 🎯 核心理念

> **Bash is all you need**
> 
> 一个循环 + 工具处理 = AI Agent

---

## 🔄 The Agent Loop (核心模式)

### 最小 Agent 循环

```
User → messages[] → LLM → response
                        │
                  stop_reason == "tool_use"?
                        / \
                       /   \
                     yes    no
                      │      │
                 execute  return text
                 tools    append results
                      │
                 append results
                      │
                 loop back ─────────────> messages[]
```

### Python 实现

```python
def agent_loop(messages):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS,
        )
        messages.append({"role": "assistant", "content": response.content})
        
        if response.stop_reason != "tool_use":
            return response
        
        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = TOOL_HANDLERS[block.name](**block.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        messages.append({"role": "user", "content": results})
```

### 悠悠的对话循环对比

**悠悠当前的循环：**
```
Telegram 消息 → OpenClaw Gateway → 悠悠 (main agent)
                                    │
                              读取记忆/上下文
                                    │
                              调用工具 (可选)
                                    │
                              生成回复
                                    │
                              发送回 Telegram
```

**整合后：**
```
Telegram 消息 → messages[] → LLM (Qwen3.5-Plus)
                              │
                        tool_use?
                          / \
                        yes  no
                         │   │
                    执行工具  返回文本
                         │
                    追加结果
                         │
                    循环 (最多 N 次)
```

---

## 📋 12 个会话机制详解

---

### Phase 1: THE LOOP (基础循环)

#### s01: The Agent Loop

**座右铭：** One loop & Bash is all you need

**核心：**
- 一个 while 循环
- 检测 tool_use
- 执行工具并追加结果
- 循环直到没有工具调用

**悠悠的应用：**
```python
# 悠悠的 agent_loop (伪代码)
def youyou_agent_loop(user_message):
    messages = load_context()  # Layer 1 + 最近对话
    messages.append({"role": "user", "content": user_message})
    
    while len(messages) < MAX_TURNS:
        response = llm(messages, tools=YOUYOU_TOOLS)
        
        if not has_tool_use(response):
            return response.content
        
        results = execute_tools(response)
        messages.append({"role": "user", "content": results})
```

---

#### s02: Tool Use

**座右铭：** Adding a tool means adding one handler

**核心：**
```python
TOOL_HANDLERS = {
    "bash": bash_handler,
    "read": read_handler,
    "write": write_handler,
    "edit": edit_handler,
}
```

**添加新工具 = 注册一个新处理器**

**悠悠的工具注册表：**

| 工具 | 处理器 | 用途 |
|------|--------|------|
| **read** | `read_file()` | 读取文件 |
| **write** | `write_file()` | 写入文件 |
| **edit** | `edit_file()` | 编辑文件 |
| **exec** | `run_command()` | 执行命令 |
| **web_search** | `search_web()` | 网络搜索 |
| **web_fetch** | `fetch_url()` | 获取网页 |
| **memory_search** | `search_memory()` | 搜索记忆 |
| **memory_get** | `get_memory()` | 获取记忆片段 |
| **browser** | `control_browser()` | 浏览器控制 |
| **message** | `send_message()` | 发送消息 |
| **tts** | `text_to_speech()` | 语音合成 |
| **cron** | `manage_cron()` | 定时任务 |

**添加新工具的步骤：**
1. 在 `TOOL_HANDLERS` 中注册
2. 实现处理器函数
3. 定义工具 schema
4. 测试

---

### Phase 2: PLANNING & KNOWLEDGE (规划与知识)

#### s03: TodoWrite

**座右铭：** An agent without a plan drifts

**核心工具：**
```python
TodoManager:
  - todo_write(tasks: list)     # 创建/更新任务列表
  - todo_complete(task_id: str) # 标记任务完成
  - nag_reminder()              # 提醒未完成任务
```

**任务状态机：**
```
pending → in_progress → completed
                ↓
            blocked
```

**悠悠的任务管理整合：**

**当前：** `memory/context/pending-tasks.md`

```markdown
## 📋 待处理

| 任务 | 优先级 | 状态 | 备注 |
|------|--------|------|------|
| 配置阿里云监控 | 🟡 | pending | 自动识别 |
```

**改进后：**
```python
def todo_write(tasks):
    """悠悠的任务管理工具"""
    # 1. 读取 pending-tasks.md
    # 2. 更新任务状态
    # 3. 写回文件
    # 4. 如果有紧急任务，提醒用户
```

**任务模板：**
```json
{
  "id": "t_20260301_001",
  "goal": "配置阿里云监控",
  "priority": "medium",
  "status": "pending",
  "created": "2026-03-01T10:00:00+08:00",
  "due": null,
  "deps": [],
  "notes": "需要在阿里云控制台配置"
}
```

---

#### s04: Subagents

**座右铭：** Break big tasks; each subtask gets a clean context

**核心：**
```python
def spawn_subagent(task):
    child_messages = []  # 全新的消息列表
    child_system = build_system_for_task(task)
    return run_agent_loop(child_messages, child_system)
```

**悠悠的子 Agent 模式：**

**当前：** `sessions_spawn` 工具

```python
def spawn_subagent(task, model=None, timeout=None):
    """悠悠的子 Agent 孵化"""
    return sessions_spawn(
        task=task,
        model=model or "alibaba-cloud/qwen3.5-plus",
        timeout_seconds=timeout or 300,
        cleanup="keep",  # 保留历史记录
        label=f"subagent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
```

**使用场景：**
- 复杂研究任务
- 需要独立上下文的子任务
- 长时间运行的任务
- 需要不同模型的子任务

**示例：**
```
用户：帮我研究跨境电商平台选择

悠悠：这是一个复杂任务，我来启动一个子 Agent 专门研究这个。
     → spawn_subagent("研究跨境电商平台，对比 Amazon/eBay/独立站")
     
子 Agent 研究完成后返回结果 → 悠悠整合回复用户
```

---

#### s05: Skills

**座右铭：** Load knowledge when needed, not upfront

**核心：**
```python
def load_skill(skill_name):
    skill_md = read_file(f"skills/{skill_name}/SKILL.md")
    return inject_via_tool_result(skill_md)
```

**悠悠的技能系统：**

**当前技能：**
| 技能 | 位置 | 用途 |
|------|------|------|
| **searxng** | `skills/searxng/` | 隐私搜索 |
| **weather** | `skills/weather/` | 天气预报 |
| **skill-vetter** | `skills/skill-vetter/` | 安全检查 |
| **youyou-memory** | `skills/youyou-memory/` | 记忆系统 |
| **jina-cli** | `skills/jina-cli/` | 网页阅读 |

**技能加载流程：**
```
用户请求 → 识别需要技能 → 读取 SKILL.md → 注入上下文 → 执行
```

**优化建议：**
- 按需加载，不预先加载所有技能
- 技能缓存，避免重复读取
- 技能版本管理

---

#### s06: Context Compact

**座右铭：** Context will fill up; you need a way to make room

**核心：三层压缩策略**

```
Layer 1: Recent (最近 10 轮)
  └─ 保留完整对话

Layer 2: Compressed (中间部分)
  └─ 压缩为摘要

Layer 3: Summary (早期)
  └─ 只保留核心摘要
```

**悠悠的上下文管理对比：**

**当前架构：**
```
Layer 1: snapshot.md (~2000 tokens) - 工作记忆
Layer 2: active/*.jsonl - 结构化记忆
Layer 3: memory/YYYY-MM-DD.md - 原始日志
```

**整合后的上下文压缩：**

```python
def compress_context(messages, max_tokens=4000):
    """上下文压缩"""
    current_tokens = count_tokens(messages)
    
    if current_tokens <= max_tokens:
        return messages
    
    # 策略 1: 保留最近 10 轮
    recent = messages[-20:]  # 10 轮对话
    
    # 策略 2: 压缩中间部分
    middle_summary = summarize(messages[10:-20])
    
    # 策略 3: 早期只保留摘要
    early_summary = load_layer1_snapshot()
    
    return [early_summary, middle_summary] + recent
```

**悠悠的 Layer 1 更新策略：**
```
每次对话后：
  1. 提取关键信息
  2. 更新 snapshot.md
  3. 保持在 ~2000 tokens 以内
  4. 重要信息写入 Layer 2
```

---

### Phase 3: PERSISTENCE (持久化)

#### s07: Tasks

**座右铭：** Break big goals into small tasks, order them, persist to disk

**核心：文件-based 任务图**

```jsonl
# tasks.jsonl
{"id": "t001", "goal": "研究跨境电商", "deps": [], "status": "pending"}
{"id": "t002", "goal": "对比 Amazon 和 eBay", "deps": ["t001"], "status": "pending"}
{"id": "t003", "goal": "选择平台", "deps": ["t002"], "status": "pending"}
```

**悠悠的任务系统整合：**

**当前：** `memory/context/pending-tasks.md`

**改进为 JSONL 格式：**
```jsonl
# memory/context/tasks.jsonl
{"id": "t_20260301_001", "goal": "配置阿里云监控", "priority": "medium", "status": "pending", "created": "2026-03-01T10:00:00+08:00", "deps": []}
{"id": "t_20260301_002", "goal": "研究跨境电商平台", "priority": "high", "status": "in_progress", "created": "2026-03-01T11:00:00+08:00", "deps": []}
```

**任务管理工具：**
```python
def task_create(goal, priority="medium", deps=[]):
    """创建任务"""
    task = {
        "id": f"t_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "goal": goal,
        "priority": priority,
        "status": "pending",
        "created": datetime.now().isoformat(),
        "deps": deps
    }
    append_to_jsonl("memory/context/tasks.jsonl", task)
    return task

def task_complete(task_id):
    """完成任务"""
    update_task_status(task_id, "completed")

def task_list(status=None):
    """列出任务"""
    tasks = load_jsonl("memory/context/tasks.jsonl")
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    return tasks
```

---

#### s08: Background Tasks

**座右铭：** Run slow operations in the background; the agent keeps thinking

**核心：守护进程线程**

```python
import threading

def run_background(command, callback=None):
    """后台运行慢操作"""
    def worker():
        result = subprocess.run(command, capture_output=True)
        if callback:
            callback(result)
    
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    return thread.pid
```

**悠悠的后台任务应用：**

**场景：**
- 长时间搜索
- 大文件处理
- 网络请求
- Git 操作

**实现：**
```python
def background_search(query, callback=None):
    """后台搜索"""
    def worker():
        results = searxng_search(query)
        if callback:
            callback(results)
    
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    return thread

# 使用示例
def search_and_notify(query):
    pid = background_search(query, lambda r: send_notification(r))
    return f"搜索已在后台运行 (PID: {pid})，完成后会通知你"
```

---

### Phase 4: TEAMS (多 Agent 协作)

#### s09: Agent Teams

**座右铭：** When the task is too big for one, delegate to teammates

**核心：队友 + JSONL 邮箱**

```python
# 队友配置
teammates = {
    "researcher": {"model": "gpt-4", "specialty": "research"},
    "coder": {"model": "claude", "specialty": "coding"},
    "writer": {"model": "gpt-4", "specialty": "writing"},
}

# JSONL 邮箱
# mailboxes/researcher.jsonl
{"from": "lead", "to": "researcher", "type": "request", "task": "..."}
{"from": "researcher", "to": "lead", "type": "response", "result": "..."}
```

**悠悠的多 Agent 架构：**

**当前：** `sessions_spawn` + `sessions_send`

**改进为团队模式：**
```python
YOUYOU_TEAM = {
    "main": {"role": "悠悠 (主)", "model": "qwen3.5-plus"},
    "researcher": {"role": "研究员", "model": "qwen3.5-plus"},
    "coder": {"role": "程序员", "model": "qwen3.5-plus"},
    "writer": {"role": "作家", "model": "qwen3.5-plus"},
}

def delegate_to_teammate(teammate, task):
    """委托给队友"""
    return sessions_spawn(
        task=task,
        agentId=teammate,
        label=f"team_{teammate}_{datetime.now().strftime('%H%M%S')}"
    )
```

---

#### s10: Team Protocols

**座右铭：** Teammates need shared communication rules

**核心：统一的请求 - 响应协议**

```python
# 协议状态机
protocol_states = {
    "request": ["pending", "claimed", "completed"],
    "response": ["submitted", "approved", "rejected"],
}

# 请求 - 响应模式
def send_request(to, task):
    mailbox_append(to, {"type": "request", "task": task, "status": "pending"})

def claim_task(agent_id, task_id):
    mailbox_append(agent_id, {"type": "claim", "task_id": task_id})

def submit_result(agent_id, task_id, result):
    mailbox_append(agent_id, {"type": "response", "task_id": task_id, "result": result})
```

**悠悠的团队协议：**
```python
# memory/team-protocol.md

## 请求格式
{
  "type": "request",
  "from": "main",
  "to": "researcher",
  "task": "研究 X 话题",
  "deadline": "30 分钟",
  "context": {...}
}

## 响应格式
{
  "type": "response",
  "from": "researcher",
  "to": "main",
  "task_id": "r_001",
  "result": {...},
  "status": "completed"
}
```

---

#### s11: Autonomous Agents

**座右铭：** Teammates scan the board and claim tasks themselves

**核心：自主认领任务**

```python
def agent_idle_cycle(agent_id):
    """Agent 空闲时扫描任务板"""
    while True:
        tasks = get_pending_tasks()
        for task in tasks:
            if can_handle(task, agent_id):
                claim_task(agent_id, task["id"])
                execute_task(task)
                submit_result(task["id"])
        sleep(60)  # 每分钟检查一次
```

**悠悠的自主 Agent：**
```python
def autonomous_agent(agent_id, specialty):
    """自主 Agent 循环"""
    while True:
        # 扫描任务板
        tasks = task_list(status="pending")
        
        # 查找匹配专长的任务
        matching = [t for t in tasks if matches_specialty(t, specialty)]
        
        if matching:
            # 认领任务
            task = matching[0]
            task_update_status(task["id"], "claimed")
            
            # 执行任务
            result = execute_task(task)
            
            # 提交结果
            task_update_status(task["id"], "completed", result)
        
        # 空闲等待
        time.sleep(60)
```

---

#### s12: Worktree Isolation

**座右铭：** Each works in its own directory, no interference

**核心：任务隔离**

```python
def create_worktree(task_id):
    """为任务创建独立工作目录"""
    workdir = f"worktrees/{task_id}"
    os.makedirs(workdir, exist_ok=True)
    return workdir

def execute_in_worktree(task_id, command):
    """在隔离的工作树中执行"""
    workdir = get_worktree(task_id)
    result = subprocess.run(command, cwd=workdir, capture_output=True)
    return result
```

**悠悠的任务隔离：**
```python
# memory/worktree-manager.py

def create_task_workspace(task_id):
    """创建任务工作区"""
    workspace = f"/tmp/youyou-tasks/{task_id}"
    os.makedirs(workspace, exist_ok=True)
    
    # 复制必要文件
    shutil.copy("memory/config.json", f"{workspace}/config.json")
    
    return workspace

def execute_task_in_isolation(task_id, script):
    """在隔离环境中执行任务"""
    workspace = create_task_workspace(task_id)
    
    # 写入脚本
    with open(f"{workspace}/task.py", "w") as f:
        f.write(script)
    
    # 执行
    result = subprocess.run(
        ["python3", "task.py"],
        cwd=workspace,
        capture_output=True,
        timeout=300
    )
    
    # 清理
    shutil.rmtree(workspace)
    
    return result
```

---

## 🎯 整合计划

### 阶段 1: 核心循环 (Week 1)

- [ ] 明确悠悠的 Agent Loop
- [ ] 规范工具注册表
- [ ] 添加工具调用日志

### 阶段 2: 任务管理 (Week 2)

- [ ] 实现 TodoWrite 工具
- [ ] 改进 pending-tasks.md 为 JSONL
- [ ] 添加任务状态追踪

### 阶段 3: 上下文优化 (Week 3)

- [ ] 实现三层压缩策略
- [ ] 优化 Layer 1 更新
- [ ] 添加上下文大小监控

### 阶段 4: 后台任务 (Week 4)

- [ ] 实现后台任务框架
- [ ] 添加任务完成通知
- [ ] 支持取消后台任务

### 阶段 5: 多 Agent (可选，Month 2)

- [ ] 定义队友角色
- [ ] 实现邮箱协议
- [ ] 自主 Agent 循环

---

## 📊 对比总结

| 机制 | learn-claude-code | 悠悠当前 | 整合后 |
|------|------------------|---------|--------|
| **Agent Loop** | ✅ 明确 | ⚠️ 隐式 | ✅ 明确定义 |
| **Tool Use** | ✅ 注册表 | ✅ 工具集 | ✅ 规范注册 |
| **TodoWrite** | ✅ 工具 | ⚠️ 文件 | ✅ 工具 + 文件 |
| **Subagents** | ✅ 独立上下文 | ✅ sessions_spawn | ✅ 优化 |
| **Skills** | ✅ 按需加载 | ✅ SKILL.md | ✅ 缓存优化 |
| **Context** | ✅ 三层压缩 | ✅ 三层架构 | ✅ 融合 |
| **Tasks** | ✅ JSONL | ⚠️ Markdown | ✅ JSONL |
| **Background** | ✅ 守护线程 | ❌ | ✅ 新增 |
| **Teams** | ✅ 邮箱协议 | ⚠️ 基础 | ✅ 完整协议 |
| **Autonomous** | ✅ 自主认领 | ❌ | ✅ 新增 |
| **Isolation** | ✅ Worktree | ❌ | ✅ 新增 |

---

## 🎉 学习收获

### 核心 insight

1. **One loop is all you need** - Agent 的核心就是一个循环
2. **Adding tools is adding handlers** - 工具扩展很规范
3. **Plan before execute** - 先规划再执行
4. **Clean context per subtask** - 子任务独立上下文
5. **Load knowledge on demand** - 按需加载知识
6. **Context will fill up** - 必须压缩
7. **Persist tasks to disk** - 任务持久化
8. **Background for slow ops** - 慢操作后台
9. **Teams need protocols** - 团队需要协议
10. **Autonomous agents claim** - 自主认领任务
11. **Isolate worktrees** - 工作区隔离

### 悠悠的进化

**youyou-v2.1 → youyou-v3.0 (Agent Loop 融合)**

```
youyou-v3.0 = 
  记忆系统 v2.1 (三层 + 树状 + 情感) +
  Agent Loop (12 机制) +
  悠悠特色 (温柔冷静 + 主动关怀)
```

---

_让知识像树一样生长，让 Agent 像人一样思考。_ 🌳🤖
