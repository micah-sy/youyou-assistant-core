# GitHub 远程仓库配置指南 🚀

## 第一步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`youyou-workspace`（或你喜欢的名字）
3. 可见性：**Private**（私有）
4. **不要**勾选 "Add a README file"
5. **不要**勾选 "Add .gitignore"
6. 点击 "Create repository"

---

## 第二步：添加 SSH Key 到 GitHub

1. 复制下面的公钥（已生成）：
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKL9uSD6NuhbAO5idlD1K71+jzNvbFzPnglM5F/MfC0h youyou@openclaw.local
```

2. 访问 https://github.com/settings/keys
3. 点击 "New SSH key"
4. Title: `youyou@openclaw`
5. Key type: **Authentication Key**
6. 粘贴上面的公钥
7. 点击 "Add SSH key"

---

## 第三步：配置远程仓库

在创建 GitHub 仓库后，执行以下命令：

```bash
cd /home/admin/.openclaw/workspace

# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin git@github.com:YOUR_USERNAME/youyou-workspace.git

# 验证远程仓库
git remote -v

# 首次推送
git push -u origin main
```

---

## 第四步：更新备份脚本

```bash
# 编辑 scripts/backup.sh，在末尾添加远程推送
cat >> scripts/backup.sh << 'EOF'

# 推送到远程仓库
git push origin main 2>&1 | tee -a "$LOG_FILE"
EOF
```

---

## 第五步：测试连接

```bash
# 测试 SSH 连接
ssh -T git@github.com

# 应该看到：
# Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## 第六步：更新 Crontab（可选）

如果需要推送到 GitHub，更新 crontab：

```bash
crontab -e

# 修改为：
0 5 * * * /home/admin/.openclaw/workspace/scripts/backup.sh "Daily backup" >> /home/admin/.openclaw/workspace/logs/backup.log 2>&1
```

---

## 常见问题

### Q1: 推送失败，提示权限问题？
```bash
# 确保 SSH key 已添加到 GitHub
# 测试连接：
ssh -T git@github.com
```

### Q2: 想要切换远程仓库？
```bash
# 移除旧远程
git remote remove origin

# 添加新远程
git remote add origin git@github.com:NEW_USERNAME/new-repo.git
```

### Q3: 查看远程仓库状态？
```bash
git remote -v
git status
```

### Q4: 拉取远程更改？
```bash
git pull origin main
```

---

## 安全提示

1. **私有仓库** - 确保仓库是 Private，不要公开你的工作区
2. **不要提交敏感信息** - `.gitignore` 已配置，排除 auth-profiles.json 等
3. **定期检查** - 使用 `git log` 查看提交历史
4. **双因素认证** - 建议开启 GitHub 2FA

---

## 当前状态 ✅ 全部完成！

- ✅ SSH Key 已生成
- ✅ SSH Config 已配置
- ✅ .gitignore 已创建
- ✅ Git 全局配置已设置
- ✅ GitHub 仓库已创建：https://github.com/micah-sy/youyou-workspace
- ✅ SSH Key 已添加到 GitHub
- ✅ 远程仓库已配置：origin@github.com:micah-sy/youyou-workspace
- ✅ 首次推送成功：8799ea0
- ✅ 自动备份脚本已更新（包含推送）

---

## 🎉 配置完成！

远程仓库地址：https://github.com/micah-sy/youyou-workspace

**自动化备份：**
- 每天凌晨 5 点自动备份并推送到 GitHub
- 每次更改都会提交到本地 git
- 敏感文件已排除（auth-profiles.json, credentials/等）

**查看提交历史：**
```bash
git log --oneline
```

**手动触发备份：**
```bash
cd /home/admin/.openclaw/workspace
./scripts/backup.sh "手动备份"
```

---

_悠悠的工作区现在安全啦～有本地 git + 远程 GitHub 双重备份！_ 🐣🛡️
