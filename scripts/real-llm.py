#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 悠悠真实 LLM 调用
Youyou Real LLM Integration

集成 OpenClaw 真实 LLM 调用（Qwen3.5-Plus）。
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests

# 添加工作区路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class OpenClawLLM:
    """OpenClaw LLM 调用封装"""
    
    def __init__(self, model: str = "alibaba-cloud/qwen3.5-plus"):
        self.model = model
        self.base_url = "http://localhost:8080"  # OpenClaw Gateway 地址
        self.timeout = 60  # 秒
        
        # 从环境读取配置
        self.gateway_url = os.getenv("OPENCLAW_GATEWAY_URL", self.base_url)
        self.api_key = os.getenv("OPENCLAW_API_KEY", "")
        
        print(f"✅ OpenClaw LLM 初始化完成")
        print(f"   模型：{model}")
        print(f"   Gateway: {self.gateway_url}")
    
    def chat(self, messages: List[Dict], tools: List[Dict] = None, 
             max_tokens: int = 2000, temperature: float = 0.7) -> Dict:
        """
        调用 LLM
        
        Args:
            messages: 消息列表
            tools: 工具定义列表
            max_tokens: 最大 token 数
            temperature: 温度参数
        
        Returns:
            LLM 响应
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        if tools:
            payload["tools"] = tools
        
        try:
            response = requests.post(
                f"{self.gateway_url}/v1/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 解析响应
            choice = result["choices"][0]
            message = choice["message"]
            
            # 检查工具调用
            if "tool_calls" in message:
                return {
                    "content": message.get("content", ""),
                    "stop_reason": "tool_use",
                    "tool_calls": [
                        {
                            "name": tc["function"]["name"],
                            "args": json.loads(tc["function"]["arguments"])
                        }
                        for tc in message["tool_calls"]
                    ]
                }
            else:
                return {
                    "content": message["content"],
                    "stop_reason": "end_turn"
                }
        
        except requests.exceptions.Timeout:
            return {
                "content": "抱歉，LLM 调用超时。",
                "stop_reason": "error",
                "error": "timeout"
            }
        except Exception as e:
            return {
                "content": f"抱歉，LLM 调用失败：{str(e)}",
                "stop_reason": "error",
                "error": str(e)
            }
    
    def get_tool_definitions(self) -> List[Dict]:
        """获取工具定义（供 LLM 使用）"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "read",
                    "description": "读取文件内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "文件路径"},
                            "offset": {"type": "integer", "description": "起始行号", "default": 1},
                            "limit": {"type": "integer", "description": "最大行数", "default": 100}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write",
                    "description": "写入文件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "文件路径"},
                            "content": {"type": "string", "description": "文件内容"},
                            "mode": {"type": "string", "description": "写入模式", "enum": ["w", "a"], "default": "w"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "网络搜索",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "搜索词"},
                            "count": {"type": "integer", "description": "结果数量", "default": 10}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "memory_search",
                    "description": "搜索记忆",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "搜索词"},
                            "max_results": {"type": "integer", "description": "最大结果数", "default": 5}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "todo_write",
                    "description": "创建任务",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tasks": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "goal": {"type": "string"},
                                        "priority": {"type": "string", "enum": ["high", "medium", "low"]}
                                    }
                                }
                            }
                        },
                        "required": ["tasks"]
                    }
                }
            },
        ]


class MockLLM:
    """模拟 LLM（用于测试）"""
    
    def __init__(self):
        self.call_count = 0
    
    def chat(self, messages: List[Dict], tools: List[Dict] = None, **kwargs) -> Dict:
        """模拟 LLM 响应"""
        self.call_count += 1
        
        # 获取最后一条用户消息
        last_user_msg = ""
        for msg in reversed(messages):
            if msg["role"] == "user" and not msg.get("tool_result"):
                last_user_msg = msg["content"]
                break
        
        # 根据内容决定响应
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
                    "args": {"tasks": [{"goal": "用户交代的任务", "priority": "high"}]}
                }]
            }
        elif "文件" in last_user_msg or "读取" in last_user_msg:
            return {
                "content": "我来读取文件。",
                "stop_reason": "tool_use",
                "tool_calls": [{
                    "name": "read",
                    "args": {"path": "MEMORY.md"}
                }]
            }
        else:
            return {
                "content": f"你好！我是悠悠，有什么可以帮你的吗？\n\n你刚才说：{last_user_msg[:100]}",
                "stop_reason": "end_turn"
            }


# 全局 LLM 实例
_real_llm = None
_mock_llm = MockLLM()


def get_llm(use_real: bool = False):
    """获取 LLM 实例"""
    global _real_llm
    
    if use_real and _real_llm is None:
        _real_llm = OpenClawLLM()
    
    return _real_llm if use_real and _real_llm else _mock_llm


def test_llm():
    """测试 LLM 调用"""
    print("🧠 测试 LLM 调用")
    print("="*60)
    
    # 测试模拟 LLM
    print("\n测试模拟 LLM:")
    mock = get_llm(use_real=False)
    messages = [{"role": "user", "content": "帮我搜索跨境电商"}]
    response = mock.chat(messages)
    print(f"响应：{response}")
    
    # 测试真实 LLM（如果可用）
    print("\n测试真实 LLM:")
    try:
        real = get_llm(use_real=True)
        response = real.chat(messages)
        print(f"响应：{response}")
    except Exception as e:
        print(f"真实 LLM 不可用：{e}")


if __name__ == "__main__":
    test_llm()
