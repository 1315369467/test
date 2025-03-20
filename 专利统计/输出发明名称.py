import os
import re
import pdfplumber
import csv


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
        match_announcement_number = re.search(r'授 权 公 告 号：[：\s]*(CN[^\n]+)', text_no_spaces)
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


# 将提取的发明名称和公告号输出到CSV文件
def output_patent_info_to_csv(pdf_folder, output_file):
    # 获取文件夹中所有的PDF文件
    pdf_files = get_pdf_files(pdf_folder)

    # 打开CSV文件，准备写入数据
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['发明名称', '公开（公告）号']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入CSV表头
        writer.writeheader()

        # 遍历所有PDF文件并提取信息
        for pdf_file in pdf_files:
            # 提取PDF文件中的发明名称和公告号
            invention_name, announcement_number = extract_patent_info(pdf_file)

            # 将提取的信息写入CSV文件
            writer.writerow({'发明名称': invention_name, '公开（公告）号': announcement_number})

    print(f"提取的发明名称和公告号已成功输出到 {output_file}")


# 输入PDF文件夹路径和输出的CSV文件路径
pdf_folder = '发明专利原件'
output_file = '专利信息输出.csv'

# 调用函数输出结果
output_patent_info_to_csv(pdf_folder, output_file)
