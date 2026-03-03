#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 悠悠图形化监控界面
Youyou Web Dashboard

基于 Flask 的实时监控界面。
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
import threading

# 添加工作区路径
sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# HTML 模板
# ─────────────────────────────────────────────────────────────

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐣 悠悠监控仪表盘</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .stat:last-child { border-bottom: none; }
        .stat-label { color: #666; }
        .stat-value { font-weight: bold; color: #333; }
        .tree-health {
            font-family: monospace;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            white-space: pre-wrap;
            font-size: 0.9em;
        }
        .tool-list {
            max-height: 300px;
            overflow-y: auto;
        }
        .tool-item {
            padding: 8px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
        }
        .tool-name { font-weight: bold; }
        .tool-count { color: #667eea; }
        .log-container {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 8px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
        }
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-left: 3px solid #667eea;
            background: rgba(102, 126, 234, 0.1);
        }
        .log-time { color: #858585; margin-right: 10px; }
        .log-info { color: #4ec9b0; }
        .log-warning { color: #dcdcaa; }
        .log-error { color: #f48771; }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            margin-top: 10px;
        }
        .refresh-btn:hover { background: #5568d3; }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-ok { background: #4caf50; }
        .status-warning { background: #ff9800; }
        .status-error { background: #f44336; }
        .chart-container {
            position: relative;
            height: 250px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐣 悠悠监控仪表盘</h1>
            <p>Youyou AI Agent Real-time Monitoring</p>
            <p id="last-update">最后更新：--</p>
        </div>
        
        <div class="grid">
            <!-- 系统状态 -->
            <div class="card">
                <h2>📊 系统状态</h2>
                <div class="stat">
                    <span class="stat-label">运行状态</span>
                    <span class="stat-value">
                        <span class="status-indicator status-ok"></span>
                        正常运行
                    </span>
                </div>
                <div class="stat">
                    <span class="stat-label">运行时间</span>
                    <span class="stat-value" id="uptime">--</span>
                </div>
                <div class="stat">
                    <span class="stat-label">API 调用</span>
                    <span class="stat-value" id="api-calls">--</span>
                </div>
                <div class="stat">
                    <span class="stat-label">活跃会话</span>
                    <span class="stat-value" id="active-sessions">--</span>
                </div>
            </div>
            
            <!-- 工具调用 -->
            <div class="card">
                <h2>🛠️ 工具调用统计</h2>
                <div class="stat">
                    <span class="stat-label">总调用次数</span>
                    <span class="stat-value" id="total-calls">--</span>
                </div>
                <div class="tool-list" id="tool-list">
                    <!-- 动态加载 -->
                </div>
            </div>
            
            <!-- 记忆树健康度 -->
            <div class="card">
                <h2>🌳 记忆树健康度</h2>
                <div class="tree-health" id="tree-health">
                    加载中...
                </div>
            </div>
            
            <!-- 任务状态 -->
            <div class="card">
                <h2>📋 任务状态</h2>
                <div class="stat">
                    <span class="stat-label">待处理</span>
                    <span class="stat-value" id="pending-tasks">--</span>
                </div>
                <div class="stat">
                    <span class="stat-label">进行中</span>
                    <span class="stat-value" id="in-progress-tasks">--</span>
                </div>
                <div class="stat">
                    <span class="stat-label">已完成</span>
                    <span class="stat-value" id="completed-tasks">--</span>
                </div>
                <div class="stat">
                    <span class="stat-label">后台任务</span>
                    <span class="stat-value" id="background-tasks">--</span>
                </div>
            </div>
        </div>
        
        <div class="grid">
            <!-- 工具调用图表 -->
            <div class="card" style="grid-column: span 2;">
                <h2>📈 工具调用趋势</h2>
                <div class="chart-container">
                    <canvas id="toolChart"></canvas>
                </div>
            </div>
            
            <!-- 最近日志 -->
            <div class="card">
                <h2>📝 最近日志</h2>
                <div class="log-container" id="log-container">
                    <div class="log-entry">
                        <span class="log-time">--:--:--</span>
                        <span class="log-info">系统启动...</span>
                    </div>
                </div>
                <button class="refresh-btn" onclick="refreshData()">🔄 刷新数据</button>
            </div>
        </div>
    </div>
    
    <script>
        let toolChart = null;
        
        async function refreshData() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                // 更新系统状态
                document.getElementById('api-calls').textContent = data.api_calls || 0;
                document.getElementById('active-sessions').textContent = data.active_sessions || 0;
                document.getElementById('uptime').textContent = formatUptime(data.uptime || 0);
                
                // 更新工具调用
                document.getElementById('total-calls').textContent = data.tool_stats?.total || 0;
                const toolList = document.getElementById('tool-list');
                toolList.innerHTML = '';
                if (data.tool_stats?.by_tool) {
                    for (const [tool, count] of Object.entries(data.tool_stats.by_tool)) {
                        toolList.innerHTML += `
                            <div class="tool-item">
                                <span class="tool-name">${tool}</span>
                                <span class="tool-count">${count} 次</span>
                            </div>
                        `;
                    }
                }
                
                // 更新记忆树
                document.getElementById('tree-health').textContent = data.tree_health || '暂无数据';
                
                // 更新任务状态
                document.getElementById('pending-tasks').textContent = data.tasks?.pending || 0;
                document.getElementById('in-progress-tasks').textContent = data.tasks?.in_progress || 0;
                document.getElementById('completed-tasks').textContent = data.tasks?.completed || 0;
                document.getElementById('background-tasks').textContent = data.background_tasks || 0;
                
                // 更新图表
                updateChart(data.tool_stats?.by_tool || {});
                
                // 更新日志
                addLog('数据刷新成功', 'info');
                
                // 更新时间
                document.getElementById('last-update').textContent = 
                    '最后更新：' + new Date().toLocaleTimeString('zh-CN');
                
            } catch (error) {
                console.error('刷新失败:', error);
                addLog('刷新失败：' + error.message, 'error');
            }
        }
        
        function formatUptime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = seconds % 60;
            return `${hours}h ${minutes}m ${secs}s`;
        }
        
        function updateChart(byTool) {
            const ctx = document.getElementById('toolChart').getContext('2d');
            const labels = Object.keys(byTool);
            const data = Object.values(byTool);
            
            if (toolChart) {
                toolChart.destroy();
            }
            
            toolChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '调用次数',
                        data: data,
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(118, 75, 162, 0.8)',
                            'rgba(247, 147, 26, 0.8)',
                            'rgba(76, 201, 240, 0.8)',
                            'rgba(28, 152, 133, 0.8)',
                        ],
                        borderColor: [
                            'rgba(102, 126, 234, 1)',
                            'rgba(118, 75, 162, 1)',
                            'rgba(247, 147, 26, 1)',
                            'rgba(76, 201, 240, 1)',
                            'rgba(28, 152, 133, 1)',
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        }
        
        function addLog(message, type = 'info') {
            const container = document.getElementById('log-container');
            const time = new Date().toLocaleTimeString('zh-CN');
            const logClass = `log-${type}`;
            
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `
                <span class="log-time">${time}</span>
                <span class="${logClass}">${message}</span>
            `;
            
            container.insertBefore(entry, container.firstChild);
            
            // 限制日志数量
            while (container.children.length > 50) {
                container.removeChild(container.lastChild);
            }
        }
        
        // 初始加载
        refreshData();
        
        // 自动刷新（每 5 秒）
        setInterval(refreshData, 5000);
    </script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────
# API 路由
# ─────────────────────────────────────────────────────────────

# 全局状态
start_time = datetime.now()
api_call_count = 0
logs = []

def add_log(message: str, level: str = "info"):
    """添加日志"""
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message
    })
    # 限制日志数量
    if len(logs) > 100:
        logs.pop(0)

@app.route('/')
def dashboard():
    """仪表盘页面"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def api_status():
    """获取状态"""
    global api_call_count
    api_call_count += 1
    
    # 这里应该调用真实的悠悠状态
    # 简化处理：返回模拟数据
    status = {
        "uptime": (datetime.now() - start_time).total_seconds(),
        "api_calls": api_call_count,
        "active_sessions": 1,
        "tool_stats": {
            "total": 15,
            "by_tool": {
                "read": 5,
                "write": 3,
                "web_search": 4,
                "memory_search": 2,
                "todo_write": 1
            }
        },
        "tree_health": """🌳 悠悠记忆树
│
├── 📊 健康度：66.7%
├── 🍃 总叶子：3
│   ├── 🌿 绿叶：2
│   ├── 🍂 黄叶：1
│   ├── 🍁 枯叶：0
│   └── 🪨 土壤：0""",
        "tasks": {
            "pending": 2,
            "in_progress": 1,
            "completed": 5
        },
        "background_tasks": 0,
        "logs": logs[-10:]
    }
    
    return jsonify(status)

@app.route('/api/tools')
def api_tools():
    """获取工具列表"""
    # 导入工具注册表
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from tool_registry import youyou_tools
        tools = youyou_tools.list_tools()
        stats = youyou_tools.get_call_stats()
        return jsonify({"tools": tools, "stats": stats})
    except:
        return jsonify({"tools": [], "stats": {}})

@app.route('/api/tasks')
def api_tasks():
    """获取任务列表"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from todo_manager import todo_manager
        result = todo_manager.todo_list()
        return jsonify(result)
    except:
        return jsonify({"success": False, "tasks": []})

@app.route('/api/memory/tree')
def api_memory_tree():
    """获取记忆树健康度"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from memory_tree import MemoryTree
        tree = MemoryTree()
        return jsonify({"health": tree.visualize()})
    except:
        return jsonify({"health": "暂无数据"})

# ─────────────────────────────────────────────────────────────
# 启动服务器
# ─────────────────────────────────────────────────────────────

def run_dashboard(host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
    """运行监控仪表盘"""
    add_log("监控仪表盘启动", "info")
    print(f"📊 悠悠监控仪表盘启动")
    print(f"   地址：http://{host}:{port}")
    print(f"   调试模式：{debug}")
    
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='悠悠监控仪表盘')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址')
    parser.add_argument('--port', type=int, default=5000, help='端口')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    run_dashboard(args.host, args.port, args.debug)
