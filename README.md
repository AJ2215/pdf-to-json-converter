# PDF 轉 JSON 轉換器

一個功能強大的 PDF 轉 JSON 工具，支援多種提取方法和 Web 介面。

## 🚀 功能特色

- 📄 **多種 PDF 處理方法**：PyPDF2、PyMuPDF、pdfplumber
- 🌐 **美觀的 Web 介面**：基於 Streamlit 構建
- 📊 **表格提取**：支援從 PDF 中提取表格數據
- 🖼️ **圖片信息**：提取 PDF 中的圖片元數據
- 📋 **詳細輸出**：包含頁面信息、元數據等
- 💾 **多種輸出格式**：美化 JSON 或壓縮格式

## 📦 安裝說明

### 1. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 2. 驗證安裝

```bash
python pdf_to_json.py --help
```

## 🎯 使用方法

### 命令列使用

```bash
# 基本使用
python pdf_to_json.py document.pdf

# 指定輸出文件
python pdf_to_json.py document.pdf -o output.json

# 選擇提取方法
python pdf_to_json.py document.pdf -m pdfplumber

# 顯示詳細信息
python pdf_to_json.py document.pdf -v
```

### Web 介面使用

```bash
# 啟動 Web 介面
streamlit run pdf_ui.py

# 區域網路共享 (其他電腦可訪問)
streamlit run pdf_ui.py --server.address 0.0.0.0 --server.port 8501
```

## 🔧 提取方法說明

| 方法 | 優點 | 適用場景 |
|------|------|----------|
| **auto** | 自動選擇最佳方法 | 推薦使用，適合大多數情況 |
| **pdfplumber** | 最佳表格提取 | 複雜佈局、包含表格的 PDF |
| **pymupdf** | 圖片信息提取 | 需要圖片元數據的場景 |
| **pypdf2** | 基本文字提取 | 簡單 PDF，相容性好 |

## 📋 輸出格式

```json
{
  "conversion_info": {
    "source_file": "document.pdf",
    "source_path": "/path/to/document.pdf",
    "conversion_time": "2024-01-01T12:00:00",
    "file_size": 1024000
  },
  "content": {
    "extraction_method": "pdfplumber",
    "total_pages": 10,
    "metadata": {
      "title": "文件標題",
      "author": "作者"
    },
    "pages": [
      {
        "page_number": 1,
        "text": "頁面文字內容...",
        "char_count": 500,
        "tables": [...],
        "images": [...]
      }
    ]
  }
}
```

## 🌐 Web 介面功能

- 📁 **拖放上傳**：支援拖放 PDF 文件
- ⚙️ **設定選項**：可選擇提取方法和輸出格式
- 📊 **進度顯示**：即時顯示轉換進度
- 📋 **結果預覽**：多種 JSON 顯示模式
- 📥 **一鍵下載**：直接下載轉換結果

## ⚠️ 注意事項

- 支援的文件格式：PDF
- 最大文件大小：200MB（Web 介面預設限制）
- 轉換時間取決於 PDF 文件大小和複雜度
- 某些加密或損壞的 PDF 文件可能無法處理

## 🛠️ 開發說明

### 項目結構

```
├── pdf_to_json.py      # 主轉換程式
├── pdf_ui.py           # Streamlit Web 介面
├── requirements.txt    # 依賴套件清單
└── README.md          # 說明文件
```

### 自訂開發

可以直接導入 `PDFToJSONConverter` 類別在您的項目中使用：

```python
from pdf_to_json import PDFToJSONConverter

converter = PDFToJSONConverter()
result = converter.convert_pdf_to_json('document.pdf', method='auto')
```

## 📄 授權

本項目採用 MIT 授權條款。

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

**PDF to JSON Converter** - 讓 PDF 數據處理更簡單！
