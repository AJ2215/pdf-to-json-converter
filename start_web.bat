@echo off
echo ================================
echo    PDF 轉 JSON 轉換器 Web 介面
echo ================================
echo.
echo 正在啟動 Streamlit 服務...
echo 請稍候，瀏覽器會自動開啟
echo.
echo 如需讓其他電腦訪問，請使用：
echo streamlit run pdf_ui.py --server.address 0.0.0.0 --server.port 8501
echo.

cd /d "%~dp0"
streamlit run pdf_ui.py

pause
