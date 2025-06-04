import os
import re
import pdfplumber
import pandas as pd


def extract_patent_info(pdf_path):
    """提取PDF中的发明名称和授权公告号"""
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        # 提取所有页面的文本内容
        for page in pdf.pages:
            text += page.extract_text()

        # 使用正则表达式提取发明名称和授权公告号
        invention_name = ''
        announcement_number = ''

        # 提取发明名称
        match_invention_name = re.search(r'发 明 名 称：[：\s]*(.*?)(?=\n|专 利 号：)', text)
        if match_invention_name:
            invention_name = match_invention_name.group(1).strip()

        # 提取授权公告号
        text_no_spaces = text.replace(" ", "")
        match_announcement_number = re.search(r'授权公告号：[：\s]*(CN[^\n]+)', text_no_spaces)
        if match_announcement_number:
            announcement_number = match_announcement_number.group(1).strip()

        return invention_name, announcement_number


def get_pdf_files(pdf_folder):
    """获取文件夹中的所有PDF文件"""
    pdf_files = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_files.append(os.path.join(pdf_folder, filename))
    return pdf_files


def sanitize_filename(filename):
    """清理文件名，去除非法字符"""
    # 替换Windows文件名中的非法字符
    illegal_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(illegal_chars, '_', filename)
    # 确保文件名不超过255个字符（Windows限制）
    if len(sanitized) > 250:  # 预留.pdf扩展名的长度
        sanitized = sanitized[:250]
    return sanitized


def process_and_rename_pdfs(excel_path, pdf_folder):
    """处理PDF文件并重命名"""
    # 加载Excel文件
    df = pd.read_excel(excel_path, engine='openpyxl')

    # 获取所有PDF文件
    pdf_files = get_pdf_files(pdf_folder)

    # 统计信息
    empty_invention_count = 0
    renamed_count = 0
    error_count = 0

    # 遍历所有PDF文件
    for pdf_file in pdf_files:
        try:
            # 提取PDF文件中的发明名称和公告号
            invention_name, announcement_number = extract_patent_info(pdf_file)

            if not invention_name:
                empty_invention_count += 1
                continue

            # 构造新文件名
            new_filename = f"{invention_name}-{announcement_number}.pdf"
            new_filename = sanitize_filename(new_filename)
            new_filepath = os.path.join(pdf_folder, new_filename)

            # 重命名文件
            if os.path.exists(new_filepath) and pdf_file != new_filepath:
                base, ext = os.path.splitext(new_filepath)
                counter = 1
                while os.path.exists(new_filepath):
                    new_filepath = f"{base}_{counter}{ext}"
                    counter += 1

            if pdf_file != new_filepath:
                os.rename(pdf_file, new_filepath)
                renamed_count += 1

            # 更新Excel数据
            for idx, row in df.iterrows():
                public_numbers = str(row['公开（公告）号']).split(';')
                if any(announcement_number == number.strip() for number in public_numbers):
                    df.at[idx, '发明名称'] = invention_name

        except Exception as e:
            print(f"处理文件 {pdf_file} 时出错: {str(e)}")
            error_count += 1
            continue

    # 保存更新后的Excel文件
    df.to_excel('更新后的专利信息.xlsx', index=False)

    # 打印统计信息
    print(f"处理完成:")
    print(f"- 成功重命名文件数: {renamed_count}")
    print(f"- 发明名称为空的文件数: {empty_invention_count}")
    print(f"- 处理出错的文件数: {error_count}")


# 输入Excel文件路径和PDF文件夹路径
excel_file = '2024年专利-分学院-计算机.xlsx'
pdf_folder = r'D:\学习\学校文件\劳务工作文件\发明专利原件'

# 执行处理
process_and_rename_pdfs(excel_file, pdf_folder)