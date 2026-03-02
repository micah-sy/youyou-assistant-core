#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 悠悠 Agent Loop 测试
Youyou Agent Loop Demo

One loop & Bash is all you need.
"""

import json
from datetime import datetime

# 模拟工具处理器
def mock_read_file(path: str) -> str:
    """模拟读取文件"""
    return f"📄 读取文件：{path}\n内容：这是测试文件内容..."

def mock_write_file(path: str, content: str) -> str:
    """模拟写入文件"""
    return f"✅ 写入文件：{path}\n内容长度：{len(content)} 字符"

def mock_search_web(query: str) -> str:
    """模拟网络搜索"""
    return f"🔍 搜索结果：'{query}'\n找到 10 条相关结果..."

def mock_memory_search(query: str) -> str:
    """模拟记忆搜索"""
    return f"🧠 记忆搜索：'{query}'\n找到 3 条相关记忆..."

def mock_todo_write(tasks: list) -> str:
    """模拟任务创建"""
    return f"📋 创建任务：{len(tasks)} 个\n任务：{[t['goal'] for t in tasks]}"

# 工具注册表
TOOL_HANDLERS = {
    "read": mock_read_file,
    "write": mock_write_file,
    "web_search": mock_search_web,
    "memory_search": mock_memory_search,
    "todo_write": mock_todo_write,
}

# 模拟 LLM 响应
class MockLLM:
    def __init__(self):
        self.call_count = 0
    
    def generate(self, messages: list, tools: list) -> dict:
        """模拟 LLM 生成响应"""
        self.call_count += 1
        user_message = messages[-1]["content"] if messages else ""
        
        # 根据用户消息模拟不同的工具调用
        if self.call_count == 1:
            if "搜索" in user_message or "查" in user_message:
                return {
                    "content": "我来帮你搜索一下。",
                    "stop_reason": "tool_use",
                    "tool_calls": [{
                        "name": "web_search",
                        "args": {"query": "跨境电商平台"}
                    }]
                }
            elif "记住" in user_message or "任务" in user_message:
                return {
                    "content": "好的，我来创建任务。",
                    "stop_reason": "tool_use",
                    "tool_calls": [{
                        "name": "todo_write",
                        "args": {"tasks": [{"goal": "测试任务", "priority": "high"}]}
                    }]
                }
            elif "文件" in user_message:
                return {
                    "content": "我来读取文件。",
                    "stop_reason": "tool_use",
                    "tool_calls": [{
                        "name": "read",
                        "args": {"path": "/test/file.txt"}
                    }]
                }
        
        # 第二次调用，返回最终结果
        return {
            "content": f"✅ 完成！这是搜索结果和总结...",
            "stop_reason": "end_turn"
        }

# Agent Loop 实现
def youyou_agent_loop(user_message: str, max_turns: int = 5):
    """
    悠悠 Agent Loop
    
    User → messages[] → LLM → tool_use? → execute → loop
    """
    print("\n" + "="*60)
    print("🐣 悠悠 Agent Loop 测试")
    print("="*60)
    print(f"\n📥 用户输入：{user_message}")
    print("-"*60)
    
    # 初始化消息列表
    messages = []
    messages.append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    # 初始化 LLM
    llm = MockLLM()
    
    # Agent Loop
    turn = 0
    while turn < max_turns:
        turn += 1
        print(f"\n🔄 第 {turn} 轮循环")
        print("-"*60)
        
        # Step 1: 调用 LLM
        print("🧠 调用 LLM...")
        response = llm.generate(messages, list(TOOL_HANDLERS.keys()))
        print(f"   响应：{response['content'][:50]}...")
        print(f"   stop_reason: {response['stop_reason']}")
        
        # Step 2: 检查是否需要调用工具
        if response["stop_reason"] != "tool_use":
            print("\n✅ 无需调用工具，返回结果")
            print("="*60)
            print(f"📤 最终回复：{response['content']}")
            print("="*60)
            return response["content"]
        
        # Step 3: 执行工具调用
        print("🛠️ 执行工具调用...")
        tool_results = []
        
        for tool_call in response.get("tool_calls", []):
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            print(f"   工具：{tool_name}")
            print(f"   参数：{tool_args}")
            
            # 调用工具处理器
            if tool_name in TOOL_HANDLERS:
                handler = TOOL_HANDLERS[tool_name]
                result = handler(**tool_args)
                print(f"   结果：{result[:80]}...")
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_name": tool_name,
                    "result": result
                })
            else:
                print(f"   ❌ 未知工具：{tool_name}")
        
        # Step 4: 将工具结果追加到消息
        messages.append({
            "role": "assistant",
            "content": response["content"]
        })
        
        messages.append({
            "role": "user",
            "content": json.dumps(tool_results, ensure_ascii=False)
        })
        
        print(f"   ✅ 工具结果已追加到消息")
    
    print("\n⚠️ 达到最大循环次数")
    return "抱歉，处理超时。"


# 测试场景
def run_tests():
    """运行测试场景"""
    
    print("\n" + "="*60)
    print("🧪 测试场景 1: 网络搜索")
    print("="*60)
    youyou_agent_loop("帮我搜索一下跨境电商平台有哪些")
    
    print("\n\n" + "="*60)
    print("🧪 测试场景 2: 创建任务")
    print("="*60)
    youyou_agent_loop("记住这个任务：研究 Amazon 和 eBay 的区别")
    
    print("\n\n" + "="*60)
    print("🧪 测试场景 3: 读取文件")
    print("="*60)
    youyou_agent_loop("读取配置文件")
    
    print("\n\n" + "="*60)
    print("🧪 测试场景 4: 多轮对话（无工具调用）")
    print("="*60)
    youyou_agent_loop("你好，悠悠")


if __name__ == "__main__":
    run_tests()
    
    print("\n\n" + "="*60)
    print("✅ Agent Loop 测试完成")
    print("="*60)
    print("\n核心流程：")
    print("1. 📥 用户消息 → messages[]")
    print("2. 🧠 LLM 生成响应")
    print("3. 🔍 检测 tool_use?")
    print("   - 是 → 🛠️ 执行工具 → 追加结果 → 循环")
    print("   - 否 → 📤 返回结果 → 结束")
    print("4. 🔄 重复直到完成或达到最大轮数")
    print("\n核心理念：One loop & Bash is all you need 🔄")
    print("="*60 + "\n")
