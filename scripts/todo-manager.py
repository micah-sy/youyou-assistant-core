#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 悠悠任务管理工具
Youyou TodoWrite Tool

An agent without a plan drifts.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class TodoManager:
    """悠悠任务管理器"""
    
    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = os.path.expanduser('~/.openclaw/workspace')
        self.workspace = Path(workspace_path)
        self.tasks_file = self.workspace / 'memory' / 'context' / 'tasks.jsonl'
        self.legacy_file = self.workspace / 'memory' / 'context' / 'pending-tasks.md'
        
        # 确保目录存在
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        
    def todo_write(self, tasks: List[Dict]) -> Dict:
        """
        创建/更新任务列表
        
        Args:
            tasks: 任务列表，每个任务包含：
                   - goal: 任务目标
                   - priority: 优先级 (high/medium/low)
                   - deps: 依赖任务 ID 列表
                   - due: 截止时间 (可选)
                   - notes: 备注 (可选)
        
        Returns:
            创建的任务列表
        """
        created_tasks = []
        
        for task_data in tasks:
            task = {
                "id": f"t_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(created_tasks)}",
                "goal": task_data.get("goal", ""),
                "priority": task_data.get("priority", "medium"),
                "status": "pending",
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "deps": task_data.get("deps", []),
                "due": task_data.get("due"),
                "notes": task_data.get("notes"),
                "completed": None
            }
            
            self._append_task(task)
            created_tasks.append(task)
        
        return {
            "success": True,
            "tasks": created_tasks,
            "message": f"已创建 {len(created_tasks)} 个任务"
        }
    
    def todo_complete(self, task_id: str) -> Dict:
        """
        标记任务完成
        
        Args:
            task_id: 任务 ID
        
        Returns:
            操作结果
        """
        tasks = self._load_tasks()
        
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks[i]["status"] = "completed"
                tasks[i]["updated"] = datetime.now().isoformat()
                tasks[i]["completed"] = datetime.now().isoformat()
                self._save_tasks(tasks)
                
                return {
                    "success": True,
                    "message": f"任务已完成：{task['goal']}"
                }
        
        return {
            "success": False,
            "message": f"未找到任务：{task_id}"
        }
    
    def todo_list(self, status: str = None, priority: str = None) -> Dict:
        """
        列出任务
        
        Args:
            status: 筛选状态 (pending/in_progress/completed)
            priority: 筛选优先级 (high/medium/low)
        
        Returns:
            任务列表
        """
        tasks = self._load_tasks()
        
        # 筛选
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]
        
        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks.sort(key=lambda t: priority_order.get(t["priority"], 1))
        
        return {
            "success": True,
            "tasks": tasks,
            "count": len(tasks)
        }
    
    def todo_update(self, task_id: str, updates: Dict) -> Dict:
        """
        更新任务
        
        Args:
            task_id: 任务 ID
            updates: 更新内容
        
        Returns:
            操作结果
        """
        tasks = self._load_tasks()
        
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks[i].update(updates)
                tasks[i]["updated"] = datetime.now().isoformat()
                self._save_tasks(tasks)
                
                return {
                    "success": True,
                    "message": f"任务已更新：{task['goal']}"
                }
        
        return {
            "success": False,
            "message": f"未找到任务：{task_id}"
        }
    
    def todo_delete(self, task_id: str) -> Dict:
        """
        删除任务
        
        Args:
            task_id: 任务 ID
        
        Returns:
            操作结果
        """
        tasks = self._load_tasks()
        original_count = len(tasks)
        
        tasks = [t for t in tasks if t["id"] != task_id]
        
        if len(tasks) < original_count:
            self._save_tasks(tasks)
            return {
                "success": True,
                "message": f"任务已删除：{task_id}"
            }
        
        return {
            "success": False,
            "message": f"未找到任务：{task_id}"
        }
    
    def get_pending_tasks(self) -> List[Dict]:
        """获取待处理任务"""
        result = self.todo_list(status="pending")
        return result.get("tasks", [])
    
    def nag_reminder(self) -> str:
        """
        提醒未完成任务
        
        Returns:
            提醒消息
        """
        pending = self.get_pending_tasks()
        
        if not pending:
            return "✅ 没有待处理的任务！"
        
        high_priority = [t for t in pending if t["priority"] == "high"]
        
        if high_priority:
            reminder = "⚠️ 有以下高优先级任务待处理：\n\n"
            for task in high_priority[:5]:
                reminder += f"- {task['goal']} (创建：{task['created'][:10]})\n"
            return reminder
        
        return f"📋 有 {len(pending)} 个待处理任务"
    
    def _append_task(self, task: Dict):
        """追加任务到文件"""
        with open(self.tasks_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(task, ensure_ascii=False) + '\n')
    
    def _load_tasks(self) -> List[Dict]:
        """加载所有任务"""
        tasks = []
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            tasks.append(json.loads(line))
                        except:
                            pass
        
        # 兼容旧格式：从 pending-tasks.md 导入
        if not tasks and self.legacy_file.exists():
            tasks = self._import_legacy_tasks()
        
        return tasks
    
    def _save_tasks(self, tasks: List[Dict]):
        """保存所有任务"""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            for task in tasks:
                f.write(json.dumps(task, ensure_ascii=False) + '\n')
    
    def _import_legacy_tasks(self) -> List[Dict]:
        """从旧格式导入任务"""
        # TODO: 解析 pending-tasks.md 格式
        return []


# 全局任务管理器实例
todo_manager = TodoManager()


# 工具函数（供 ToolRegistry 调用）
def todo_write(tasks: List[Dict]) -> Dict:
    """TodoWrite 工具"""
    return todo_manager.todo_write(tasks)

def todo_complete(task_id: str) -> Dict:
    """TodoComplete 工具"""
    return todo_manager.todo_complete(task_id)

def todo_list(status: str = None, priority: str = None) -> Dict:
    """TodoList 工具"""
    return todo_manager.todo_list(status, priority)

def todo_update(task_id: str, updates: Dict) -> Dict:
    """TodoUpdate 工具"""
    return todo_manager.todo_update(task_id, updates)

def todo_delete(task_id: str) -> Dict:
    """TodoDelete 工具"""
    return todo_manager.todo_delete(task_id)

def get_pending_tasks() -> List[Dict]:
    """获取待处理任务"""
    return todo_manager.get_pending_tasks()

def nag_reminder() -> str:
    """任务提醒"""
    return todo_manager.nag_reminder()


if __name__ == "__main__":
    # 测试任务管理
    print("📋 悠悠任务管理工具")
    print("=" * 50)
    
    # 创建测试任务
    result = todo_write([
        {"goal": "测试任务 1", "priority": "high"},
        {"goal": "测试任务 2", "priority": "medium"},
        {"goal": "测试任务 3", "priority": "low"},
    ])
    print(f"创建任务：{result}")
    
    # 列出任务
    result = todo_list()
    print(f"\n所有任务：{result['count']} 个")
    for task in result['tasks']:
        print(f"  - [{task['priority']}] {task['goal']} ({task['status']})")
    
    # 提醒
    print(f"\n提醒：{nag_reminder()}")
