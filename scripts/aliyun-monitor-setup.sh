#!/bin/bash
# aliyun-monitor-setup.sh - 阿里云监控配置脚本
# 用法：./aliyun-monitor-setup.sh

set -euo pipefail

echo "🔧 配置阿里云监控..."

# 获取当前 ECS 实例 ID
INSTANCE_ID=$(curl -s http://100.100.100.200/latest/meta-data/instance-id 2>/dev/null || echo "unknown")

echo "📊 实例 ID: $INSTANCE_ID"

# 创建云监控告警模板
cat > /tmp/cms-alert-template.json << EOF
{
  "Namespace": "acs_ecs_dashboard",
  "MetricName": "CPUUtilization",
  "Dimensions": {
    "instanceId": "$INSTANCE_ID"
  },
  "Period": 300,
  "Type": "greater_than_threshold",
  "Threshold": 80,
  "ComparisonOperator": "GreaterThanOrEqualToThreshold",
  "EvaluationCount": 3,
  "ContactGroups": "$(whoami)-alert-group",
  "Webhook": ""
}
EOF

echo "📋 告警规则模板已创建"

# 提示用户配置
cat << 'EOF'

=====================================
阿里云监控配置指南
=====================================

## 方案 1: 使用云监控控制台（推荐）

1. 访问阿里云控制台
   https://ecs.console.aliyun.com/

2. 进入 监控与运维 → 云监控

3. 创建告警规则：
   - CPU 使用率 > 80% (持续 3 个周期)
   - 内存使用率 > 85%
   - 磁盘使用率 > 90%
   - 网络流量异常

4. 设置通知方式：
   - 短信
   - 邮件
   - 钉钉机器人
   - Webhook

## 方案 2: 使用 CLI 配置

# 创建告警联系人组
aliyun cms PutContactGroup \
  --ContactGroupName "$(whoami)-alert-group" \
  --Contacts "[{\"Name\":\"$(whoami)\",\"Email\":\"your@email.com\"}]"

# 创建 CPU 告警
aliyun cms PutResourceMetricRule \
  --MetricRuleName "ECS-CPU-Alert" \
  --Namespace "acs_ecs_dashboard" \
  --MetricName "CPUUtilization" \
  --Threshold 80

# 创建内存告警
aliyun cms PutResourceMetricRule \
  --MetricRuleName "ECS-Memory-Alert" \
  --Namespace "acs_ecs_dashboard" \
  --MetricName "MemoryUtilization" \
  --Threshold 85

## 方案 3: 使用云助手（最简单）

在阿里云控制台：
1. 运维与监控 → 云助手
2. 创建定时任务
3. 执行健康检查脚本
4. 设置告警通知

=====================================
EOF

echo ""
echo "✅ 配置模板已准备就绪"
echo "📖 详细配置请查看：/home/admin/.openclaw/workspace/logs/aliyun-monitor-guide.md"
