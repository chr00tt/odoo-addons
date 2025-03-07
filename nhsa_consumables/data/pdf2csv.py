import pdfplumber
import csv
import os
import gc

def dynamic_pdf_to_csv(pdf_path, csv_path, chunk_size=100):
    """通用版PDF分块转换（自动识别总页数）"""
    
    # 第一次预读获取总页数
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
    print(f"检测到PDF总页数: {total_pages}")

    # 初始化CSV文件
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        f.write("")  # 创建空文件

    # 分块处理
    for chunk_start in range(0, total_pages, chunk_size):
        chunk_end = min(chunk_start + chunk_size, total_pages)
        print(f"正在处理 {chunk_start+1}-{chunk_end} 页...")

        # 使用临时文件
        temp_csv = f"temp_{chunk_start}.csv"
        
        # 每次重新打开PDF避免内存累积
        with pdfplumber.open(pdf_path) as pdf, \
             open(temp_csv, 'w', newline='', encoding='utf-8') as tmpfile:
            
            writer = csv.writer(tmpfile)
            for page_num in range(chunk_start, chunk_end):
                try:
                    page = pdf.pages[page_num]
                    
                    # 低内存表格提取设置
                    table_settings = {"snap_tolerance": 8}  # 降低检测精度提升速度
                    tables = page.extract_tables(table_settings)
                    
                    for table in tables:
                        for row in table[1:]:   # 跳过表头
                            cleaned_row = [
                                cell.replace('\n', '').strip() 
                                if cell is not None else ""
                                for cell in row
                            ]
                            writer.writerow(cleaned_row)
                    
                    # 主动释放资源
                    del page
                    if page_num % 10 == 0:
                        gc.collect()
                
                except Exception as e:
                    print(f"第 {page_num+1} 页处理失败: {str(e)}")
                    continue

        # 追加到主文件
        with open(csv_path, 'a', encoding='utf-8') as mainfile:
            with open(temp_csv, 'r', encoding='utf-8') as tmpfile:
                mainfile.write(tmpfile.read())
        os.remove(temp_csv)

# 使用示例
dynamic_pdf_to_csv("医保医用耗材分类与代码_截至2025年1月.pdf", "nhsa.consumables.csv", chunk_size=200)  # 可调节分块大小
