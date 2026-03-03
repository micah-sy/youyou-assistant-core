# 📝 WPS 接入方案

**日期：** 2026-03-02  
**状态：** 📋 方案规划中

---

## 🎯 WPS 接入方式

### 方案 1：WPS 开放平台 API（推荐）

**官方 API：** https://open.wps.cn/

**功能：**
- 📄 文档创建/编辑/保存
- 📊 表格数据处理
- 📑 演示文稿生成
- ☁️ 云存储同步

**接入步骤：**
1. 注册 WPS 开放平台账号
2. 创建应用获取 AppKey/AppSecret
3. 配置 OAuth 2.0 授权
4. 调用 REST API

**优点：**
- ✅ 官方支持，稳定可靠
- ✅ 功能完整
- ✅ 文档齐全

**缺点：**
- ⚠️ 需要企业账号（部分功能）
- ⚠️ 有调用限制

---

### 方案 2：本地 WPS 自动化（Linux）

**工具：** `wps` 命令行 + Python 脚本

**依赖：**
```bash
# 安装 WPS Office
sudo apt install wps-office

# Python 库
pip install python-docx openpyxl
```

**功能：**
- 📄 本地文档操作
- 📊 表格生成
- 🔄 格式转换（docx ↔ pdf）

**优点：**
- ✅ 无需 API key
- ✅ 完全本地，隐私好
- ✅ 无调用限制

**缺点：**
- ⚠️ 需要安装 WPS
- ⚠️ 仅限本地文件

---

### 方案 3：WPS Webhook + 云文档

**原理：** WPS 云文档 + Webhook 触发

**流程：**
```
悠悠 → 创建文档 → WPS 云存储 → 分享链接 → 用户
```

**优点：**
- ✅ 云端协作
- ✅ 实时同步
- ✅ 分享方便

**缺点：**
- ⚠️ 需要配置 Webhook
- ⚠️ 依赖网络

---

## 🔧 推荐实现（方案 2：本地自动化）

### 1. 安装依赖

```bash
# WPS Office
sudo apt install wps-office

# Python 库
cd ~/.openclaw/workspace
source .venv/bin/activate
uv pip install python-docx openpyxl reportlab
```

### 2. 创建 WPS 工具脚本

```python
#!/usr/bin/env python3
# scripts/wps-tools.py

from docx import Document
from openpyxl import Workbook
import os

class WPSAutomation:
    def __init__(self, output_dir="~/Documents/wps-output"):
        self.output_dir = os.path.expanduser(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_doc(self, filename, content):
        """创建 Word 文档"""
        doc = Document()
        for para in content:
            doc.add_paragraph(para)
        path = os.path.join(self.output_dir, filename)
        doc.save(path)
        return path
    
    def create_excel(self, filename, data):
        """创建 Excel 表格"""
        wb = Workbook()
        ws = wb.active
        for row in data:
            ws.append(row)
        path = os.path.join(self.output_dir, filename)
        wb.save(path)
        return path
    
    def doc_to_pdf(self, doc_path):
        """Word 转 PDF（需要 WPS 命令行）"""
        pdf_path = doc_path.replace('.docx', '.pdf')
        os.system(f'wps --headless --convert-to pdf {doc_path} -o {self.output_dir}')
        return pdf_path

# 测试
if __name__ == "__main__":
    wps = WPSAutomation()
    
    # 创建文档
    doc_path = wps.create_doc("test.docx", ["Hello WPS!", "这是悠悠创建的文档"])
    print(f"文档已创建：{doc_path}")
    
    # 创建表格
    excel_path = wps.create_excel("test.xlsx", [
        ["姓名", "年龄", "城市"],
        ["悠悠", "1", "云端"],
        ["用户", "20", "地球"]
    ])
    print(f"表格已创建：{excel_path}")
```

### 3. 添加到悠悠工具集

在 `scripts/production-tools.py` 中添加：

```python
@register_tool
def wps_create_doc(title, content):
    """创建 WPS 文档"""
    wps = WPSAutomation()
    filename = f"{title}.docx"
    path = wps.create_doc(filename, content)
    return f"✅ 文档已创建：{path}"

@register_tool
def wps_create_excel(title, data):
    """创建 WPS 表格"""
    wps = WPSAutomation()
    filename = f"{title}.xlsx"
    path = wps.create_excel(filename, data)
    return f"✅ 表格已创建：{path}"
```

---

## 📋 实施计划

### 阶段 1：本地文档生成（1 天）

- [ ] 安装 WPS Office
- [ ] 安装 Python 库
- [ ] 创建 `wps-tools.py`
- [ ] 测试文档创建
- [ ] 测试表格创建

### 阶段 2：格式转换（1 天）

- [ ] 实现 docx → pdf
- [ ] 实现 xlsx → csv
- [ ] 批量转换支持

### 阶段 3：云文档集成（可选）

- [ ] 申请 WPS 开放平台 API
- [ ] 实现 OAuth 授权
- [ ] 云文档上传/下载
- [ ] 分享链接生成

---

## 🎯 使用示例

### 悠悠，帮我创建一个文档

```
用户：悠悠，帮我写一份跨境电商调研报告
悠悠：好的！正在创建文档...
     ✅ 文档已创建：~/Documents/wps-output/跨境电商调研报告.docx
     内容包括：
     1. 市场概况
     2. 主要平台对比
     3. 运营策略
     4. 风险提示
```

### 悠悠，帮我做个表格

```
用户：悠悠，帮我做个产品对比表
悠悠：好的！正在创建表格...
     ✅ 表格已创建：~/Documents/wps-output/产品对比表.xlsx
     包含：Amazon、eBay、独立站 的对比数据
```

---

## 💡 建议

**对于你的业务（反光马甲跨境电商）：**

1. **产品文档** - 自动生成产品描述、规格书
2. **报价单** - 根据客户询价自动生成 Excel 报价
3. **合同模板** - 标准合同快速生成
4. **周报/月报** - 定期生成业务报告
5. **产品目录** - 批量生成产品 catalog

---

## 🚀 下一步

**要开始实施吗？我可以：**

1. ✅ 立即安装 WPS 和依赖
2. ✅ 创建 `wps-tools.py` 脚本
3. ✅ 测试文档/表格生成功能
4. ✅ 集成到悠悠工具集

**或者你想先用 WPS 开放平台 API？** 需要：
- 企业账号
- 应用审核（1-3 天）
- API 配额申请

---

_让悠悠帮你自动化文档工作！_ 📝✨
