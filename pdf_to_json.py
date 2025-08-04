#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF to JSON Converter Tool
將 PDF 文件轉換為 JSON 格式的工具
"""

import json
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Any
import logging

try:
    import PyPDF2
    import fitz  # PyMuPDF
    from pdfplumber import PDF
except ImportError as e:
    print(f"缺少必要的套件: {e}")
    print("請執行: pip install PyPDF2 PyMuPDF pdfplumber")
    sys.exit(1)


class PDFToJSONConverter:
    """PDF 轉 JSON 轉換器"""
    
    def __init__(self):
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌記錄器"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def extract_with_pypdf2(self, pdf_path: str) -> Dict[str, Any]:
        """使用 PyPDF2 提取 PDF 內容"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                metadata = {
                    'title': pdf_reader.metadata.get('/Title', '') if pdf_reader.metadata else '',
                    'author': pdf_reader.metadata.get('/Author', '') if pdf_reader.metadata else '',
                    'subject': pdf_reader.metadata.get('/Subject', '') if pdf_reader.metadata else '',
                    'creator': pdf_reader.metadata.get('/Creator', '') if pdf_reader.metadata else '',
                    'producer': pdf_reader.metadata.get('/Producer', '') if pdf_reader.metadata else '',
                }
                
                pages = []
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    pages.append({
                        'page_number': page_num,
                        'text': text.strip(),
                        'char_count': len(text)
                    })
                
                return {
                    'extraction_method': 'PyPDF2',
                    'total_pages': len(pdf_reader.pages),
                    'metadata': metadata,
                    'pages': pages
                }
        except Exception as e:
            self.logger.error(f"PyPDF2 提取失敗: {e}")
            return None
    
    def extract_with_pymupdf(self, pdf_path: str) -> Dict[str, Any]:
        """使用 PyMuPDF 提取 PDF 內容"""
        try:
            doc = fitz.open(pdf_path)
            
            metadata = doc.metadata
            
            pages = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                # 提取圖片信息
                images = []
                image_list = page.get_images()
                for img_index, img in enumerate(image_list):
                    images.append({
                        'image_index': img_index,
                        'xref': img[0],
                        'width': img[2],
                        'height': img[3]
                    })
                
                pages.append({
                    'page_number': page_num + 1,
                    'text': text.strip(),
                    'char_count': len(text),
                    'images': images,
                    'rect': {
                        'width': page.rect.width,
                        'height': page.rect.height
                    }
                })
            
            doc.close()
            
            return {
                'extraction_method': 'PyMuPDF',
                'total_pages': len(pages),
                'metadata': metadata,
                'pages': pages
            }
        except Exception as e:
            self.logger.error(f"PyMuPDF 提取失敗: {e}")
            return None
    
    def extract_with_pdfplumber(self, pdf_path: str) -> Dict[str, Any]:
        """使用 pdfplumber 提取 PDF 內容 (包含表格)"""
        try:
            with PDF.open(pdf_path) as pdf:
                metadata = pdf.metadata
                
                pages = []
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""
                    
                    # 提取表格
                    tables = []
                    page_tables = page.extract_tables()
                    for table_index, table in enumerate(page_tables):
                        if table:
                            tables.append({
                                'table_index': table_index,
                                'rows': len(table),
                                'columns': len(table[0]) if table else 0,
                                'data': table
                            })
                    
                    pages.append({
                        'page_number': page_num,
                        'text': text.strip(),
                        'char_count': len(text),
                        'tables': tables,
                        'page_size': {
                            'width': page.width,
                            'height': page.height
                        }
                    })
                
                return {
                    'extraction_method': 'pdfplumber',
                    'total_pages': len(pages),
                    'metadata': metadata,
                    'pages': pages
                }
        except Exception as e:
            self.logger.error(f"pdfplumber 提取失敗: {e}")
            return None
    
    def convert_pdf_to_json(self, pdf_path: str, method: str = 'auto', 
                           output_path: str = None, pretty: bool = True) -> Dict[str, Any]:
        """
        將 PDF 轉換為 JSON
        
        Args:
            pdf_path: PDF 文件路徑
            method: 提取方法 ('pypdf2', 'pymupdf', 'pdfplumber', 'auto')
            output_path: 輸出 JSON 文件路徑
            pretty: 是否美化 JSON 輸出
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"找不到 PDF 文件: {pdf_path}")
        
        self.logger.info(f"開始處理 PDF: {pdf_path}")
        
        # 選擇提取方法
        if method == 'auto':
            # 自動選擇最佳方法，優先使用 pdfplumber
            result = self.extract_with_pdfplumber(pdf_path)
            if not result:
                result = self.extract_with_pymupdf(pdf_path)
            if not result:
                result = self.extract_with_pypdf2(pdf_path)
        elif method == 'pypdf2':
            result = self.extract_with_pypdf2(pdf_path)
        elif method == 'pymupdf':
            result = self.extract_with_pymupdf(pdf_path)
        elif method == 'pdfplumber':
            result = self.extract_with_pdfplumber(pdf_path)
        else:
            raise ValueError(f"不支援的提取方法: {method}")
        
        if not result:
            raise Exception("所有提取方法都失敗了")
        
        # 添加轉換信息
        conversion_info = {
            'source_file': os.path.basename(pdf_path),
            'source_path': pdf_path,
            'conversion_time': datetime.now().isoformat(),
            'file_size': os.path.getsize(pdf_path)
        }
        
        final_result = {
            'conversion_info': conversion_info,
            'content': result
        }
        
        # 保存到文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(final_result, f, ensure_ascii=False, indent=2)
                else:
                    json.dump(final_result, f, ensure_ascii=False)
            
            self.logger.info(f"JSON 文件已保存到: {output_path}")
        
        return final_result


def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='PDF 轉 JSON 轉換工具')
    parser.add_argument('pdf_path', help='PDF 文件路徑')
    parser.add_argument('-o', '--output', help='輸出 JSON 文件路徑')
    parser.add_argument('-m', '--method', 
                       choices=['pypdf2', 'pymupdf', 'pdfplumber', 'auto'],
                       default='auto',
                       help='提取方法 (預設: auto)')
    parser.add_argument('--no-pretty', action='store_true',
                       help='不美化 JSON 輸出')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='顯示詳細信息')
    
    args = parser.parse_args()
    
    # 設置日誌級別
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 設置輸出路徑
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.pdf_path))[0]
        args.output = f"{base_name}.json"
    
    try:
        converter = PDFToJSONConverter()
        result = converter.convert_pdf_to_json(
            pdf_path=args.pdf_path,
            method=args.method,
            output_path=args.output,
            pretty=not args.no_pretty
        )
        
        print(f"✅ 轉換完成!")
        print(f"📄 來源文件: {args.pdf_path}")
        print(f"📋 輸出文件: {args.output}")
        print(f"📊 總頁數: {result['content']['total_pages']}")
        print(f"🔧 提取方法: {result['content']['extraction_method']}")
        
    except Exception as e:
        print(f"❌ 轉換失敗: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
