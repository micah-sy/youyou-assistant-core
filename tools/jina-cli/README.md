# jina-cli - 网页读取工具 🌿

> 轻量级 CLI 工具，封装 Jina AI Reader API，将任意网页转换为 LLM 友好的 Markdown 格式

---

## 🎯 用途

- ✅ 读取 X (Twitter) 帖子（绕过登录墙）
- ✅ 抓取博客、新闻网站
- ✅ 给 AI 提供干净的网页内容
- ✅ 网络搜索 + 自动内容提取

---

## 📦 安装

### 方式一：CLI 二进制（推荐）

```bash
wget -qO- https://raw.githubusercontent.com/geekjourneyx/jina-cli/main/scripts/install.sh | bash
```

验证安装：
```bash
jina --version
```

### 方式二：OpenClaw Skill

Skill 已位于：`~/.openclaw/workspace/skills/jina-cli/SKILL.md`

重启 OpenClaw 后，可以直接在对话中使用 `jina read` 和 `jina search` 命令。

---

## 💡 常用命令

### 读取网页

```bash
# 基本读取
jina read -u "https://example.com"

# 输出 Markdown 格式
jina read -u "https://example.com" --output markdown

# 保存到文件
jina read -u "https://example.com" --output-file result.md

# 读取 X (Twitter) 帖子
jina read -u "https://x.com/user/status/123456" --with-alt

# 使用 Nitter 读取 X（不需要登录）
jina read -u "https://nitter.net/user/status/123456"
```

### 网络搜索

```bash
# 基本搜索
jina search -q "golang latest news"

# 限定站点
jina search -q "AI developments" --site techcrunch.com --site theverge.com

# 限制结果数量
jina search -q "climate change" --limit 10
```

### 配置

```bash
# 查看所有配置
jina config list

# 设置超时
jina config set timeout 60

# 设置 API Key（获取更高速率限制）
jina config set api_key jina_xxxxxxxxxxxxx
```

---

## 🔗 相关链接

- **项目主页**: https://github.com/geekjourneyx/jina-cli
- **Jina AI Reader**: https://jina.ai/reader
- **Nitter (X 前端)**: https://nitter.net

---

## 📝 示例

### 读取新闻文章

```bash
jina read -u "https://techcrunch.com/2024/01/01/ai-news" --output markdown
```

### 批量读取 URL

```bash
# 创建 URL 列表
cat > urls.txt << EOF
https://example.com/page1
https://example.com/page2
https://nitter.net/user/status/123
EOF

# 批量读取
jina read --file urls.txt --output markdown
```

### 研究工作流

```bash
# 1. 搜索主题
jina search -q "quantum computing 2025" --limit 10

# 2. 读取具体结果
jina read --file search_results.txt
```

---

## ⚠️ 注意事项

- **X (Twitter)** 需要登录才能直接访问，建议使用 Nitter 前端
- **GitHub** 部分页面需要登录
- 默认使用缓存，需要最新内容可加 `--no-cache`

---

_安装日期：2026-03-03_
