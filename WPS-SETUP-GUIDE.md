# 📝 WPS 接入指南

**状态：** 📋 等待 API 审核  
**预计完成：** 1-3 个工作日

---

## ✅ 已完成

- [x] 创建 `scripts/wps-tools.py` 脚本
- [x] 创建环境变量模板 `.wps-env.example`
- [x] 添加执行权限

---

## ⏳ 待完成

### 1. 申请 WPS 开放平台账号

**访问：** https://open.wps.cn/

**步骤：**
1. 注册/登录
2. 控制台 → 创建应用
3. 填写信息：
   - 应用名称：`悠悠助手`
   - 应用类型：办公工具
   - 回调地址：`http://localhost:13787`
4. 提交审核

**拿到：**
- `AppKey`
- `AppSecret`

---

### 2. 配置环境变量

```bash
cd ~/.openclaw/workspace
cp .wps-env.example .wps-env

# 编辑 .wps-env，填入你的 AppKey 和 AppSecret
nano .wps-env

# 加载环境变量
source .wps-env

# 永久生效（可选）
echo "source ~/.openclaw/workspace/.wps-env" >> ~/.bashrc
source ~/.bashrc
```

---

### 3. 测试脚本

```bash
cd ~/.openclaw/workspace
source .venv/bin/activate
source .wps-env  # 加载 WPS 配置

python3 scripts/wps-tools.py
```

**预期输出：**
```
==================================================
🐣 悠悠 WPS 文档生成工具 - 测试
==================================================
📝 正在创建文档：跨境电商调研报告
   段落数：11
✅ 文档已创建：https://kdocs.wps.cn/l/demo_doc_123
📊 正在创建表格：产品对比表
   行数：4
✅ 表格已创建：https://kdocs.wps.cn/l/demo_sheet_456
==================================================
✅ 测试完成！
```

---

### 4. 集成到悠悠工具集

在 `scripts/production-tools.py` 中添加：

```python
from wps_tools import WPSAutomation

@register_tool
def wps_create_doc(title: str, content: list):
    """
    创建 WPS 文档
    
    Args:
        title: 文档标题
        content: 内容段落列表
    """
    wps = WPSAutomation()
    result = wps.create_doc(title, content)
    return f"✅ 文档已创建：{result['url']}"

@register_tool
def wps_create_excel(title: str, data: list):
    """
    创建 WPS 表格
    
    Args:
        title: 表格标题
        data: 二维数组
    """
    wps = WPSAutomation()
    result = wps.create_excel(title, data)
    return f"✅ 表格已创建：{result['url']}"
```

---

## 🎯 使用示例

### 在 Telegram/QQ 中对悠悠说：

```
悠悠，帮我写一份产品调研报告

悠悠：好的！正在创建文档...
     ✅ 文档已创建：https://kdocs.wps.cn/l/xxx123
     内容包括：
     1. 市场概况
     2. 竞品分析
     3. 运营建议
```

```
悠悠，帮我做个产品对比表

悠悠：好的！正在创建表格...
     ✅ 表格已创建：https://kdocs.wps.cn/l/yyy456
     包含：Amazon、eBay、独立站 的对比数据
```

---

## 📊 资源占用

| 项目 | 占用 |
|------|------|
| **磁盘** | ~1MB（配置 + 脚本） |
| **内存** | ~10MB（API 调用） |
| **网络** | 每次调用 ~100KB |

**完全适合你的 1.8GB 小服务器！** ✅

---

## 🔧 故障排查

### 问题 1：获取 Token 失败

```bash
# 检查环境变量
echo $WPS_APP_KEY
echo $WPS_APP_SECRET

# 确认配置正确
cat .wps-env
```

### 问题 2：API 调用失败

```bash
# 检查网络
curl https://openapi.wps.cn

# 查看日志
tail -f /tmp/openclaw/openclaw-*.log
```

### 问题 3：审核被拒

- 检查应用信息是否完整
- 确保回调地址正确
- 联系客服：open@wps.cn

---

## 📚 相关文档

- WPS 开放平台：https://open.wps.cn/
- API 文档：https://open.wps.cn/docs
- 社区支持：https://github.com/BytePioneer-AI/openclaw-china

---

_让悠悠帮你自动化文档工作！_ 📝✨
