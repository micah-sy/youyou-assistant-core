#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 悠悠真实 Agent Loop
Youyou Production Agent Loop

集成到 OpenClaw 的真实对话流程。
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
import threading
import queue

# 添加工作区路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入悠悠工具
from scripts.tool_registry import youyou_tools, setup_youyou_tools
from scripts.todo_manager import todo_manager, nag_reminder
from scripts.memory_tree import MemoryTree

class YouyouAgentLoop:
    """悠悠生产级 Agent Loop"""
    
    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = os.path.expanduser('~/.openclaw/workspace')
        self.workspace = Path(workspace_path)
        
        # 初始化
        self.messages: List[Dict] = []
        self.max_turns = 5
        self.context_window = 4000  # tokens
        
        # 工具通知队列
        self.tool_notification_queue = queue.Queue()
        
        # 后台任务
        self.background_tasks: Dict[str, threading.Thread] = {}
        
        # 初始化记忆树
        self.memory_tree = MemoryTree(str(self.workspace))
        
        # 设置工具
        setup_youyou_tools()
        
        print("✅ 悠悠 Agent Loop 初始化完成")
        print(f"   工作区：{self.workspace}")
        print(f"   最大轮数：{self.max_turns}")
        print(f"   上下文窗口：{self.context_window} tokens")
    
    def load_context(self, include_layer1: bool = True, include_recent: int = 10):
        """
        加载上下文
        
        Args:
            include_layer1: 是否包含 Layer 1 快照
            include_recent: 包含最近 N 轮对话
        """
        self.messages = []
        
        # 1. 加载 Layer 1 快照
        if include_layer1:
            layer1_file = self.workspace / 'memory' / 'layer1' / 'snapshot.md'
            if layer1_file.exists():
                with open(layer1_file, 'r', encoding='utf-8') as f:
                    snapshot = f.read()
                self.messages.append({
                    "role": "system",
                    "content": f"悠悠的记忆快照：\n{snapshot}"
                })
        
        # 2. 加载最近对话（从日志文件）
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.workspace / 'memory' / f'{today}.md'
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            # 简化处理：追加到系统消息
            if self.messages:
                self.messages[0]["content"] += f"\n\n今日日志摘要：\n{content[:1000]}"
        
        print(f"✅ 上下文加载完成：{len(self.messages)} 条消息")
    
    def compress_context(self):
        """
        压缩上下文（三层策略）
        """
        if len(self.messages) <= 10:
            return  # 不需要压缩
        
        # 策略 1: 保留最近 10 轮
        recent = self.messages[-20:]  # 10 轮对话
        
        # 策略 2: 压缩中间部分（这里简化处理）
        # 实际应该调用 LLM 生成摘要
        
        # 策略 3: 保留系统消息
        system_msg = self.messages[0] if self.messages[0]["role"] == "system" else None
        
        # 重组
        if system_msg:
            self.messages = [system_msg] + recent
        else:
            self.messages = recent
        
        print(f"✅ 上下文压缩完成：{len(self.messages)} 条消息")
    
    def execute_tool(self, tool_name: str, args: Dict) -> Any:
        """
        执行工具调用
        
        Args:
            tool_name: 工具名称
            args: 工具参数
        
        Returns:
            工具执行结果
        """
        print(f"\n🛠️ 执行工具：{tool_name}")
        print(f"   参数：{args}")
        
        # 获取工具处理器
        handler = youyou_tools.get_handler(tool_name)
        
        if not handler:
            return f"❌ 未知工具：{tool_name}"
        
        try:
            # 执行工具
            result = handler(**args)
            
            # 记录调用
            youyou_tools.record_call(tool_name, args, result, True)
            
            print(f"   ✅ 结果：{str(result)[:100]}...")
            return result
            
        except Exception as e:
            error_msg = f"❌ 工具执行失败：{str(e)}"
            youyou_tools.record_call(tool_name, args, error_msg, False)
            print(f"   {error_msg}")
            return error_msg
    
    def run_background_task(self, task_id: str, tool_name: str, args: Dict):
        """
        后台运行任务
        
        Args:
            task_id: 任务 ID
            tool_name: 工具名称
            args: 工具参数
        """
        def worker():
            print(f"\n🔄 后台任务 {task_id} 开始执行...")
            result = self.execute_tool(tool_name, args)
            
            # 完成后通知
            self.tool_notification_queue.put({
                "task_id": task_id,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            print(f"✅ 后台任务 {task_id} 完成")
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        self.background_tasks[task_id] = thread
        
        return task_id
    
    def check_background_tasks(self) -> List[Dict]:
        """检查后台任务完成情况"""
        notifications = []
        
        while not self.tool_notification_queue.empty():
            notifications.append(self.tool_notification_queue.get())
        
        return notifications
    
    def agent_loop(self, user_message: str) -> str:
        """
        悠悠 Agent Loop（核心）
        
        Args:
            user_message: 用户消息
        
        Returns:
            最终回复
        """
        print("\n" + "="*60)
        print("🐣 悠悠 Agent Loop")
        print("="*60)
        print(f"\n📥 用户：{user_message}")
        print("-"*60)
        
        # 1. 加载上下文（如果是新对话）
        if not self.messages:
            self.load_context()
        
        # 2. 添加用户消息
        self.messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # 3. Agent Loop
        turn = 0
        while turn < self.max_turns:
            turn += 1
            print(f"\n🔄 第 {turn} 轮")
            print("-"*60)
            
            # 检查上下文大小
            if len(self.messages) > 20:
                self.compress_context()
            
            # Step 1: 调用 LLM（这里模拟，实际应该调用 OpenClaw 的 LLM）
            print("🧠 调用 LLM...")
            response = self.mock_llm(self.messages)
            print(f"   响应：{response.get('content', '')[:50]}...")
            
            # Step 2: 检查是否需要调用工具
            if response.get("stop_reason") != "tool_use":
                print("\n✅ 无需工具，返回结果")
                final_reply = response.get("content", "")
                break
            
            # Step 3: 执行工具调用
            print("🛠️ 执行工具...")
            tool_results = []
            
            for tool_call in response.get("tool_calls", []):
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                is_background = tool_args.pop("_background", False)
                
                if is_background:
                    # 后台执行
                    task_id = f"bg_{datetime.now().strftime('%H%M%S')}_{turn}"
                    self.run_background_task(task_id, tool_name, tool_args)
                    result = f"任务已在后台运行 (ID: {task_id})"
                else:
                    # 前台执行
                    result = self.execute_tool(tool_name, tool_args)
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_name": tool_name,
                    "result": str(result)
                })
            
            # Step 4: 追加消息
            self.messages.append({
                "role": "assistant",
                "content": response.get("content", "")
            })
            
            self.messages.append({
                "role": "user",
                "content": json.dumps(tool_results, ensure_ascii=False)
            })
            
            # Step 5: 检查后台任务通知
            notifications = self.check_background_tasks()
            if notifications:
                for notif in notifications:
                    self.messages.append({
                        "role": "system",
                        "content": f"后台任务完成通知：{notif['task_id']} - {notif['result'][:100]}"
                    })
        
        print("\n" + "="*60)
        print(f"📤 回复：{final_reply}")
        print("="*60)
        
        # 保存上下文（更新 Layer 1）
        self.save_context()
        
        return final_reply
    
    def mock_llm(self, messages: List[Dict]) -> Dict:
        """
        模拟 LLM 调用（实际应该替换为真实的 LLM 调用）
        """
        # 这里简化处理，根据消息内容返回不同的响应
        last_user_msg = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break
        
        # 工具调用映射
        if "搜索" in last_user_msg or "查" in last_user_msg:
            return {
                "content": "我来帮你搜索一下。",
                "stop_reason": "tool_use",
                "tool_calls": [{
                    "name": "web_search",
                    "args": {"query": "跨境电商"}
                }]
            }
        elif "记住" in last_user_msg or "任务" in last_user_msg:
            return {
                "content": "好的，我来创建任务。",
                "stop_reason": "tool_use",
                "tool_calls": [{
                    "name": "todo_write",
                    "args": {
                        "tasks": [{"goal": "用户交代的任务", "priority": "high"}]
                    }
                }]
            }
        elif "文件" in last_user_msg or "读取" in last_user_msg:
            return {
                "content": "我来读取文件。",
                "stop_reason": "tool_use",
                "tool_calls": [{
                    "name": "read",
                    "args": {"path": "/test/file.txt"}
                }]
            }
        elif "后台" in last_user_msg or "background" in last_user_msg.lower():
            return {
                "content": "好的，在后台运行。",
                "stop_reason": "tool_use",
                "tool_calls": [{
                    "name": "web_search",
                    "args": {"query": "后台任务", "_background": True}
                }]
            }
        else:
            # 闲聊模式
            return {
                "content": f"你好！我是悠悠，有什么可以帮你的吗？\n\n你刚才说：{last_user_msg[:50]}",
                "stop_reason": "end_turn"
            }
    
    def save_context(self):
        """保存上下文（更新 Layer 1）"""
        # 提取关键信息，更新 snapshot.md
        snapshot_file = self.workspace / 'memory' / 'layer1' / 'snapshot.md'
        
        # 这里简化处理，实际应该调用 LLM 生成摘要
        with open(snapshot_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n[更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}]")
            f.write(f"\n最新对话摘要...")
        
        print("✅ 上下文已保存")
    
    def get_tool_stats(self) -> Dict:
        """获取工具调用统计"""
        return youyou_tools.get_call_stats()
    
    def get_tree_health(self) -> str:
        """获取记忆树健康度"""
        return self.memory_tree.visualize()


# 全局 Agent Loop 实例
youyou_agent = YouyouAgentLoop()


def chat(user_message: str) -> str:
    """
    悠悠聊天接口（供 OpenClaw 调用）
    
    Args:
        user_message: 用户消息
    
    Returns:
        悠悠的回复
    """
    return youyou_agent.agent_loop(user_message)


def get_status() -> Dict:
    """
    获取悠悠状态（供 OpenClaw 调用）
    
    Returns:
        状态信息
    """
    return {
        "tool_stats": youyou_agent.get_tool_stats(),
        "tree_health": youyou_agent.get_tree_health(),
        "background_tasks": len(youyou_agent.background_tasks),
        "pending_notifications": youyou_agent.tool_notification_queue.qsize()
    }


if __name__ == "__main__":
    # 测试
    print("🐣 悠悠生产级 Agent Loop 测试")
    print("="*60)
    
    # 测试场景
    test_messages = [
        "你好，悠悠",
        "帮我搜索一下跨境电商平台",
        "记住这个任务：研究 Amazon 和 eBay",
        "后台运行搜索任务",
    ]
    
    for msg in test_messages:
        reply = chat(msg)
        print(f"\n回复：{reply}\n")
        print("-"*60)
    
    # 显示状态
    print("\n📊 悠悠状态")
    print("="*60)
    status = get_status()
    print(f"工具调用：{status['tool_stats']['total']} 次")
    print(f"后台任务：{status['background_tasks']} 个")
    print(f"待通知：{status['pending_notifications']} 个")
