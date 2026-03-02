# 悠悠的远程备份配置指南

## 当前状态

- ✅ Git 本地仓库已初始化
- ✅ 首次提交完成：`6ced26b Initial commit`
- ✅ 自动备份脚本已配置
- ✅ Crontab 定时任务已设置
- ⚠️ 远程仓库：未配置

---

## 方案 1: GitHub 私有仓库（推荐）

### 步骤 1: 创建 GitHub 仓库

```bash
# 在 GitHub 上创建私有仓库，例如：youyou-workspace
# 不要初始化 README/.gitignore，使用现有仓库
```

### 步骤 2: 配置远程仓库

```bash
cd /home/admin/.openclaw/workspace

# 添加远程仓库（替换为你的仓库地址）
git remote add origin git@github.com:YOUR_USERNAME/youyou-workspace.git

# 或者使用 HTTPS（需要 token）
git remote add origin https://github.com/YOUR_USERNAME/youyou-workspace.git
```

### 步骤 3: 配置 SSH Key（如果用 SSH）

```bash
# 生成 SSH key
ssh-keygen -t ed25519 -C "youyou@openclaw.local" -f /home/admin/.ssh/id_ed25519_youyou

# 查看公钥
cat /home/admin/.ssh/id_ed25519_youyou.pub

# 将公钥添加到 GitHub: Settings → SSH and GPG keys → New SSH key
```

### 步骤 4: 首次推送

```bash
cd /home/admin/.openclaw/workspace
git branch -M main
git push -u origin main
```

### 步骤 5: 更新备份脚本

```bash
# 编辑 scripts/backup.sh，在末尾添加：
git push origin main 2>/dev/null || echo "推送失败（可能无网络）" >> "$LOG_FILE"
```

---

## 方案 2: 阿里云 OSS 备份

### 步骤 1: 安装 ossutil

```bash
wget https://gosspublic.alicdn.com/ossutil/1.7.19/ossutil64
chmod 755 ossutil64
./ossutil64 config
```

### 步骤 2: 配置备份

```bash
# 创建备份脚本 scripts/oss-backup.sh
#!/bin/bash
WORKSPACE="/home/admin/.openclaw/workspace"
OSS_BUCKET="oss://your-backup-bucket/workspace-backup"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

cd "$WORKSPACE"
tar -czf "/tmp/workspace-$TIMESTAMP.tar.gz" \
    --exclude='.git' \
    --exclude='logs' \
    .

./ossutil64 cp "/tmp/workspace-$TIMESTAMP.tar.gz" "$OSS_BUCKET/"
rm "/tmp/workspace-$TIMESTAMP.tar.gz"
```

---

## 方案 3: 本地快照（最简单）

### 使用阿里云 ECS 快照

```bash
# 在阿里云控制台配置自动快照策略
# 1. 进入 ECS 控制台
# 2. 磁盘和快照 → 自动快照策略
# 3. 创建策略：每天凌晨 6 点
# 4. 应用到工作区所在磁盘
```

**优点：**
- 无需配置
- 完整系统备份
- 可回滚到任意时间点

**缺点：**
- 占用磁盘空间
- 不能细粒度恢复

---

## 推荐配置

对于个人使用，推荐：

1. **GitHub 私有仓库** — 代码和配置版本控制
2. **阿里云快照** — 完整系统备份（每周）

这样既有细粒度的 git 历史，又有完整的系统快照。

---

## 敏感信息保护

在推送远程仓库前，确保以下文件**不要提交**：

```bash
# 创建 .gitignore
cat > /home/admin/.openclaw/workspace/.gitignore << 'EOF'
# 敏感信息
*.key
*.pem
*.secret
auth-profiles.json
credentials/

# 日志文件（可选）
logs/*.log

# 临时文件
*.tmp
*.swp
*~

# 系统文件
.DS_Store
Thumbs.db
EOF
```

---

_需要我帮你配置哪个方案？告诉我即可～_ 🐣
