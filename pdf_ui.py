#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF to JSON Converter - Streamlit Web Interface
PDF 轉 JSON 轉換器 - Streamlit 網頁介面
"""

import streamlit as st
import json
import os
import tempfile
from datetime import datetime
from pdf_to_json import PDFToJSONConverter

# 設定頁面配置
st.set_page_config(
    page_title="PDF 轉 JSON 轉換器",
    page_icon="📄",
    layout="wide"
)

# 主標題
st.title("📄 PDF 轉 JSON 轉換器")
st.markdown("---")

# 側邊欄設定
st.sidebar.header("⚙️ 轉換設定")

# 選擇提取方法
method = st.sidebar.selectbox(
    "選擇提取方法：",
    ["auto", "pdfplumber", "pymupdf", "pypdf2"],
    index=0,
    help="auto 會自動選擇最佳方法"
)

# 輸出格式選項
pretty_json = st.sidebar.checkbox("美化 JSON 輸出", value=True)
download_json = st.sidebar.checkbox("下載 JSON 文件", value=True)

# 主要內容區域
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 上傳 PDF 文件")
    
    # 文件上傳器
    uploaded_file = st.file_uploader(
        "選擇 PDF 文件",
        type=['pdf'],
        help="支援的格式：PDF"
    )
    
    if uploaded_file is not None:
        # 顯示文件信息
        st.success("✅ 文件上傳成功！")
        st.info(f"📝 文件名：{uploaded_file.name}")
        st.info(f"📊 文件大小：{uploaded_file.size:,} bytes")

with col2:
    st.header("🔄 轉換結果")
    
    if uploaded_file is not None:
        # 轉換按鈕
        if st.button("🚀 開始轉換", type="primary"):
            try:
                # 顯示進度條
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("正在處理 PDF 文件...")
                progress_bar.progress(25)
                
                # 創建臨時文件
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                
                status_text.text("正在提取 PDF 內容...")
                progress_bar.progress(50)
                
                # 初始化轉換器
                converter = PDFToJSONConverter()
                
                status_text.text("正在轉換為 JSON...")
                progress_bar.progress(75)
                
                # 執行轉換
                result = converter.convert_pdf_to_json(
                    pdf_path=tmp_file_path,
                    method=method,
                    output_path=None,
                    pretty=pretty_json
                )
                
                progress_bar.progress(100)
                status_text.text("✅ 轉換完成！")
                
                # 清理臨時文件
                os.unlink(tmp_file_path)
                
                # 顯示轉換結果統計
                st.success("🎉 PDF 轉換成功！")
                
                # 顯示統計信息
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric("📄 總頁數", result['content']['total_pages'])
                
                with col_stat2:
                    st.metric("🔧 提取方法", result['content']['extraction_method'])
                
                with col_stat3:
                    conversion_time = datetime.fromisoformat(result['conversion_info']['conversion_time'])
                    st.metric("⏰ 轉換時間", conversion_time.strftime("%H:%M:%S"))
                
                # 顯示 JSON 結果
                st.markdown("---")
                st.header("📋 JSON 結果")
                
                # JSON 顯示選項
                display_option = st.radio(
                    "選擇顯示方式：",
                    ["預覽前 1000 字符", "顯示完整 JSON", "僅顯示結構"],
                    horizontal=True
                )
                
                json_str = json.dumps(result, ensure_ascii=False, indent=2 if pretty_json else None)
                
                if display_option == "預覽前 1000 字符":
                    preview = json_str[:1000] + "..." if len(json_str) > 1000 else json_str
                    st.code(preview, language='json')
                    if len(json_str) > 1000:
                        st.info(f"顯示前 1000 字符，完整 JSON 共 {len(json_str):,} 字符")
                
                elif display_option == "顯示完整 JSON":
                    st.code(json_str, language='json')
                
                elif display_option == "僅顯示結構":
                    structure = {
                        "conversion_info": {
                            "source_file": result['conversion_info']['source_file'],
                            "conversion_time": result['conversion_info']['conversion_time'],
                            "file_size": result['conversion_info']['file_size']
                        },
                        "content": {
                            "extraction_method": result['content']['extraction_method'],
                            "total_pages": result['content']['total_pages'],
                            "metadata": "..." if result['content']['metadata'] else None,
                            "pages": f"{len(result['content']['pages'])} pages with text and data"
                        }
                    }
                    st.json(structure)
                
                # 下載按鈕
                if download_json:
                    st.markdown("---")
                    output_filename = f"{os.path.splitext(uploaded_file.name)[0]}.json"
                    
                    st.download_button(
                        label="📥 下載 JSON 文件",
                        data=json_str,
                        file_name=output_filename,
                        mime="application/json",
                        type="secondary"
                    )
                
            except Exception as e:
                st.error(f"❌ 轉換失敗：{str(e)}")
                st.error("請檢查 PDF 文件是否損壞或嘗試其他提取方法")
                
                # 顯示詳細錯誤信息（可選）
                with st.expander("查看詳細錯誤信息"):
                    import traceback
                    st.code(traceback.format_exc())

# 底部信息
st.markdown("---")
st.markdown(
    """
    ### 📖 使用說明
    1. **上傳 PDF 文件**：點擊上方的文件上傳區域選擇 PDF 文件
    2. **選擇設定**：在左側設定轉換參數
    3. **開始轉換**：點擊「開始轉換」按鈕
    4. **查看結果**：在右側查看轉換結果和下載 JSON 文件
    
    ### 🔧 提取方法說明
    - **auto**：自動選擇最佳方法（推薦）
    - **pdfplumber**：最佳的表格提取，適合複雜佈局
    - **pymupdf**：支援圖片信息提取
    - **pypdf2**：基本文字提取，相容性好
    
    ### ⚠️ 注意事項
    - 支援的文件格式：PDF
    - 最大文件大小限制：200MB（Streamlit 預設）
    - 轉換時間取決於 PDF 文件大小和複雜度
    """
)

# 頁腳
st.markdown(
    """
    <div style="text-align: center; padding: 20px; color: #888;">
        <hr>
        <p>PDF to JSON Converter | 基於 Streamlit 構建</p>
    </div>
    """,
    unsafe_allow_html=True
)
