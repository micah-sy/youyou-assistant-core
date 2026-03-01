#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ 悠悠工具注册表
Youyou Tool Registry

Adding a tool means adding one handler.
"""

import json
import os
from pathlib import Path
from typing import Callable, Dict, Any, Optional
from datetime import datetime

class ToolRegistry:
    """悠悠工具注册表"""
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.schemas: Dict[str, Dict] = {}
        self.call_history: list = []
        
    def register(self, name: str, handler: Callable, schema: Dict = None):
        """注册工具"""
        self.handlers[name] = handler
        if schema:
            self.schemas[name] = schema
        print(f"✅ 工具已注册：{name}")
        
    def unregister(self, name: str):
        """注销工具"""
        if name in self.handlers:
            del self.handlers[name]
        if name in self.schemas:
            del self.schemas[name]
        print(f"❌ 工具已注销：{name}")
        
    def get_handler(self, name: str) -> Optional[Callable]:
        """获取工具处理器"""
        return self.handlers.get(name)
        
    def has_tool(self, name: str) -> bool:
        """检查工具是否存在"""
        return name in self.handlers
        
    def list_tools(self) -> list:
        """列出所有工具"""
        return list(self.handlers.keys())
        
    def record_call(self, name: str, args: Dict, result: Any, success: bool):
        """记录工具调用"""
        self.call_history.append({
            "timestamp": datetime.now().isoformat(),
            "tool": name,
            "args": args,
            "success": success,
            "result_preview": str(result)[:100] if result else None
        })
        
    def get_call_stats(self) -> Dict:
        """获取调用统计"""
        if not self.call_history:
            return {"total": 0, "by_tool": {}}
        
        by_tool = {}
        for call in self.call_history:
            tool = call["tool"]
            by_tool[tool] = by_tool.get(tool, 0) + 1
        
        return {
            "total": len(self.call_history),
            "by_tool": by_tool,
            "recent": self.call_history[-10:]
        }


# 全局工具注册表实例
youyou_tools = ToolRegistry()

# 注册悠悠的核心工具
def setup_youyou_tools():
    """设置悠悠的工具"""
    
    # 文件操作工具
    from tools.file_tools import read_file, write_file, edit_file, list_files
    youyou_tools.register("read", read_file, {"type": "file_read"})
    youyou_tools.register("write", write_file, {"type": "file_write"})
    youyou_tools.register("edit", edit_file, {"type": "file_edit"})
    youyou_tools.register("list", list_files, {"type": "file_list"})
    
    # 命令执行工具
    from tools.command_tools import run_command, run_background
    youyou_tools.register("exec", run_command, {"type": "command_exec"})
    youyou_tools.register("exec_bg", run_background, {"type": "command_background"})
    
    # 网络工具
    from tools.web_tools import search_web, fetch_url
    youyou_tools.register("web_search", search_web, {"type": "web_search"})
    youyou_tools.register("web_fetch", fetch_url, {"type": "web_fetch"})
    
    # 记忆工具
    from tools.memory_tools import search_memory, get_memory, add_memory
    youyou_tools.register("memory_search", search_memory, {"type": "memory_search"})
    youyou_tools.register("memory_get", get_memory, {"type": "memory_get"})
    youyou_tools.register("memory_add", add_memory, {"type": "memory_add"})
    
    # 任务管理工具
    from tools.task_tools import todo_write, todo_complete, todo_list
    youyou_tools.register("todo_write", todo_write, {"type": "task_management"})
    youyou_tools.register("todo_complete", todo_complete, {"type": "task_management"})
    youyou_tools.register("todo_list", todo_list, {"type": "task_management"})
    
    # Agent 工具
    from tools.agent_tools import spawn_subagent, send_to_session
    youyou_tools.register("sessions_spawn", spawn_subagent, {"type": "agent_management"})
    youyou_tools.register("sessions_send", send_to_session, {"type": "agent_communication"})
    
    print(f"✅ 悠悠工具注册完成：{len(youyou_tools.list_tools())} 个工具")


# 工具调用装饰器
def tool_call(tool_name: str):
    """工具调用装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 记录调用
            youyou_tools.record_call(tool_name, {"args": args, "kwargs": kwargs}, None, True)
            
            # 执行
            try:
                result = func(*args, **kwargs)
                youyou_tools.record_call(tool_name, {"args": args, "kwargs": kwargs}, result, True)
                return result
            except Exception as e:
                youyou_tools.record_call(tool_name, {"args": args, "kwargs": kwargs}, str(e), False)
                raise
        return wrapper
    return decorator


if __name__ == "__main__":
    # 测试工具注册表
    print("🛠️ 悠悠工具注册表")
    print("=" * 50)
    
    setup_youyou_tools()
    
    print(f"\n已注册工具：{youyou_tools.list_tools()}")
    print(f"\n调用统计：{youyou_tools.get_call_stats()}")
