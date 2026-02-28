# 悠悠的工作区权限配置

## 当前权限状态

```bash
# 工作区目录
drwxrwxr-x  admin:admin  /home/admin/.openclaw/workspace/

# 脚本目录（可执行）
drwxrwxr-x  admin:admin  /home/admin/.openclaw/workspace/scripts/
-rwxr-xr-x  backup.sh    # 备份脚本（可执行）

# 日志目录（只读写入）
drwxrwxr-x  admin:admin  /home/admin/.openclaw/workspace/logs/

# 记忆系统目录
drwxr-xr-x  admin:admin  /home/admin/.openclaw/workspace/memory/
```

## 权限策略

### 悠悠的权限边界

| 目录 | 权限 | 说明 |
|------|------|------|
| `workspace/` | 读写 | 主要工作区，可自由编辑 |
| `scripts/` | 读写 + 执行 | 脚本可执行 |
| `logs/` | 追加写入 | 日志只追加，不覆盖 |
| `memory/` | 读写 | 记忆系统，自动维护 |
| `avatars/` | 只读 | 头像等静态资源 |
| `.git/` | 只读 | git 仓库，通过 git 命令修改 |

### 禁止操作（除非用户明确要求）

- ❌ 删除 `/etc/` 下任何文件
- ❌ 修改系统服务配置
- ❌ 安装未经验证的软件
- ❌ 访问用户家目录以外的敏感文件
- ❌ 修改网络配置

### 安全操作

- ✅ 使用 `trash` 代替 `rm`
- ✅ 所有操作记录到 `logs/command-audit.md`
- ✅ 每天自动备份到 git
- ✅ 系统级操作前先询问

---

_最后更新：2026-02-28_
