#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ 悠悠异步 IO 优化
Youyou Async IO Optimization

使用 asyncio 和 aiohttp 实现高性能异步工具执行。
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor
import functools

# 添加工作区路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class AsyncToolExecutor:
    """异步工具执行器"""
    
    def __init__(self, max_concurrency: int = 10):
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.executor = ThreadPoolExecutor(max_workers=max_concurrency)
        self.call_history = []
        
        print(f"✅ 异步工具执行器初始化完成")
        print(f"   最大并发：{max_concurrency}")
    
    async def execute_tool_async(self, tool_name: str, handler: Callable, 
                                  args: Dict, timeout: int = 30) -> Any:
        """
        异步执行工具
        
        Args:
            tool_name: 工具名称
            handler: 工具处理器函数
            args: 工具参数
            timeout: 超时时间（秒）
        
        Returns:
            工具执行结果
        """
        async with self.semaphore:
            try:
                # 将同步函数包装为异步
                loop = asyncio.get_event_loop()
                func = functools.partial(handler, **args)
                
                # 异步执行
                result = await asyncio.wait_for(
                    loop.run_in_executor(self.executor, func),
                    timeout=timeout
                )
                
                # 记录调用
                self.call_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "tool": tool_name,
                    "status": "success",
                    "duration": 0  # TODO: 计算实际耗时
                })
                
                return result
                
            except asyncio.TimeoutError:
                self.call_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "tool": tool_name,
                    "status": "timeout",
                    "error": f"超时（{timeout}秒）"
                })
                return f"❌ 工具执行超时（{timeout}秒）"
                
            except Exception as e:
                self.call_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "tool": tool_name,
                    "status": "error",
                    "error": str(e)
                })
                return f"❌ 工具执行失败：{str(e)}"
    
    async def execute_multiple_tools(self, tool_calls: List[Dict]) -> List[Dict]:
        """
        并发执行多个工具
        
        Args:
            tool_calls: 工具调用列表
                       [{"name": "web_search", "args": {"query": "..."}}, ...]
        
        Returns:
            工具结果列表
        """
        # 导入工具处理器
        from scripts.production_tools import (
            search_web, read_file, write_file,
            memory_search, todo_write
        )
        
        TOOL_HANDLERS = {
            "web_search": search_web,
            "read": read_file,
            "write": write_file,
            "memory_search": memory_search,
            "todo_write": todo_write,
        }
        
        # 创建任务
        tasks = []
        for call in tool_calls:
            tool_name = call.get("name")
            tool_args = call.get("args", {})
            
            if tool_name in TOOL_HANDLERS:
                handler = TOOL_HANDLERS[tool_name]
                task = self.execute_tool_async(tool_name, handler, tool_args)
                tasks.append(task)
        
        # 并发执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 整理结果
        tool_results = []
        for i, result in enumerate(results):
            tool_results.append({
                "tool_name": tool_calls[i]["name"],
                "result": str(result) if not isinstance(result, Exception) else f"❌ {str(result)}"
            })
        
        return tool_results
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = len(self.call_history)
        success = sum(1 for c in self.call_history if c["status"] == "success")
        timeout = sum(1 for c in self.call_history if c["status"] == "timeout")
        error = sum(1 for c in self.call_history if c["status"] == "error")
        
        return {
            "total": total,
            "success": success,
            "timeout": timeout,
            "error": error,
            "success_rate": f"{(success/total*100) if total > 0 else 0:.1f}%"
        }


class AsyncAgentLoop:
    """异步 Agent Loop"""
    
    def __init__(self, max_concurrency: int = 10):
        self.executor = AsyncToolExecutor(max_concurrency)
        self.max_turns = 5
        
        print(f"✅ 异步 Agent Loop 初始化完成")
    
    async def agent_loop(self, user_message: str) -> str:
        """
        异步 Agent Loop
        
        Args:
            user_message: 用户消息
        
        Returns:
            最终回复
        """
        print(f"\n📥 用户：{user_message}")
        
        messages = [{"role": "user", "content": user_message}]
        
        turn = 0
        while turn < self.max_turns:
            turn += 1
            print(f"\n🔄 第 {turn} 轮")
            
            # 调用 LLM（模拟）
            response = await self.mock_llm(messages)
            print(f"   LLM: {response.get('content', '')[:50]}...")
            
            # 检查工具调用
            if response.get("stop_reason") != "tool_use":
                print(f"✅ 完成：{response.get('content', '')}")
                return response.get("content", "")
            
            # 并发执行工具
            tool_calls = response.get("tool_calls", [])
            print(f"🛠️ 并发执行 {len(tool_calls)} 个工具...")
            
            tool_results = await self.executor.execute_multiple_tools(tool_calls)
            
            # 追加结果
            messages.append({
                "role": "user",
                "content": json.dumps(tool_results, ensure_ascii=False)
            })
        
        return "抱歉，处理超时。"
    
    async def mock_llm(self, messages: List[Dict]) -> Dict:
        """模拟 LLM 调用"""
        # 简化处理
        last_msg = messages[-1]["content"]
        
        # 多工具调用测试
        if "搜索" in last_msg and "文件" in last_msg:
            return {
                "content": "我来同时执行多个任务。",
                "stop_reason": "tool_use",
                "tool_calls": [
                    {"name": "web_search", "args": {"query": "跨境电商"}},
                    {"name": "read", "args": {"path": "MEMORY.md"}},
                    {"name": "memory_search", "args": {"query": "业务"}}
                ]
            }
        elif "搜索" in last_msg:
            return {
                "content": "我来搜索一下。",
                "stop_reason": "tool_use",
                "tool_calls": [
                    {"name": "web_search", "args": {"query": "跨境电商"}}
                ]
            }
        else:
            return {
                "content": "你好！我是悠悠。",
                "stop_reason": "end_turn"
            }


async def test_async_performance():
    """测试异步性能"""
    print("⚡ 异步性能测试")
    print("="*60)
    
    # 测试 1: 单个工具
    print("\n测试 1: 单个工具执行")
    agent = AsyncAgentLoop(max_concurrency=5)
    start = datetime.now()
    result = await agent.agent_loop("搜索跨境电商")
    end = datetime.now()
    print(f"耗时：{(end - start).total_seconds():.3f}秒")
    
    # 测试 2: 并发多个工具
    print("\n测试 2: 并发多个工具")
    start = datetime.now()
    result = await agent.agent_loop("搜索跨境电商并读取文件和记忆")
    end = datetime.now()
    print(f"耗时：{(end - start).total_seconds():.3f}秒")
    
    # 显示统计
    print("\n📊 执行统计:")
    stats = agent.executor.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")


def run_dashboard_async():
    """运行异步仪表盘"""
    import subprocess
    
    # 启动仪表盘
    dashboard_script = Path(__file__).parent / 'dashboard.py'
    subprocess.Popen([sys.executable, str(dashboard_script)])
    
    print("📊 仪表盘已启动")
    print("   地址：http://localhost:5000")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='悠悠异步 IO 优化')
    parser.add_argument('--test', action='store_true', help='运行性能测试')
    parser.add_argument('--dashboard', action='store_true', help='启动仪表盘')
    
    args = parser.parse_args()
    
    if args.test:
        asyncio.run(test_async_performance())
    elif args.dashboard:
        run_dashboard_async()
    else:
        print("用法:")
        print("  python3 async-optimizer.py --test      # 性能测试")
        print("  python3 async-optimizer.py --dashboard # 启动仪表盘")
