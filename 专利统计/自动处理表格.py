import os
import re
import pdfplumber
import pandas as pd


# 提取PDF中的发明名称和授权公告号
def extract_patent_info(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        # 提取所有页面的文本内容
        for page in pdf.pages:
            text += page.extract_text()

        # 使用正则表达式提取发明名称和授权公告号
        invention_name = ''
        announcement_number = ''

        # 提取发明名称（假设发明名称格式为“发 明 名 称：<名称>”）
        match_invention_name = re.search(r'发 明 名 称：[：\s]*(.*?)(?=\n|专 利 号：)', text)
        if match_invention_name:
            invention_name = match_invention_name.group(1).strip()

        # 提取授权公告号，去除所有空格和换行符，再匹配公告号
        text_no_spaces = text.replace(" ", "")  # 去除空格
        match_announcement_number = re.search(r'授权公告号：[：\s]*(CN[^\n]+)', text_no_spaces)
        if match_announcement_number:
            announcement_number = match_announcement_number.group(1).strip()

        return invention_name, announcement_number


# 读取文件夹中的所有PDF文件
def get_pdf_files(pdf_folder):
    pdf_files = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_files.append(os.path.join(pdf_folder, filename))
    return pdf_files


# 读取Excel文件并更新发明名称
def update_excel_with_patent_info(excel_path, pdf_folder):
    # 加载Excel文件
    df = pd.read_excel(excel_path, engine='openpyxl')

    # 获取文件夹中所有的PDF文件
    pdf_files = get_pdf_files(pdf_folder)

    # 遍历所有PDF文件并提取信息
    for pdf_file in pdf_files:
        # 提取PDF文件中的发明名称和公告号
        invention_name, announcement_number = extract_patent_info(pdf_file)

        # 初始化空计数器
        empty_invention_count = 0

        # 如果发明名称为空，增加计数器
        if not invention_name:
            empty_invention_count += 1

        # 遍历Excel中的每一行，找到公开（公告）号匹配的行
        for idx, row in df.iterrows():
            # 将公开（公告）号列的多个公告号拆分成一个列表
            public_numbers = str(row['公开（公告）号']).split(';')

            # 检查是否有公告号与announcement_number完全匹配
            if any(announcement_number == number.strip() for number in public_numbers):
                # 更新发明名称
                df.at[idx, '发明名称'] = invention_name

    # 保存更新后的Excel文件
    df.to_excel('更新后的专利信息.xlsx', index=False)

    # 打印空的发明名称的统计信息
    print(f"共有 {empty_invention_count} 个PDF文件的发明名称为空。")


# 输入Excel文件路径和PDF文件夹路径
excel_file = '2024年专利-分学院-计算机.xlsx'
pdf_folder = r'D:\学习\学校文件\劳务工作文件\发明专利原件'

# 调用函数更新表格
update_excel_with_patent_info(excel_file, pdf_folder)

print("表格更新完成，保存为 '更新后的专利信息.xlsx'")
