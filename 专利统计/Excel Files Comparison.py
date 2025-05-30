import pandas as pd


def compare_invention_names(file1_path, file2_path):
    """
    比较两个Excel文件中发明名称列只出现一次的数据
    """
    # 读取两个Excel文件
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)

    # 合并两个文件的发明名称列
    all_names = pd.concat([df1['发明名称'], df2['发明名称']])

    # 计算每个发明名称出现的次数
    name_counts = all_names.value_counts()

    # 找出只出现一次的发明名称
    unique_names = name_counts[name_counts == 1]

    # 分别找出在每个文件中只出现一次的发明名称
    file1_unique = []
    file2_unique = []

    for name in unique_names.index:
        if name in df1['发明名称'].values:
            file1_unique.append(name)
        if name in df2['发明名称'].values:
            file2_unique.append(name)

    # 创建结果DataFrame
    results = pd.DataFrame({
        '文件1独有的发明名称': pd.Series(file1_unique),
        '文件2独有的发明名称': pd.Series(file2_unique)
    })

    # 保存结果到Excel文件
    results.to_excel('独有发明名称比较结果.xlsx', index=False)

    # 打印统计信息
    print(f"文件1独有的发明名称数量: {len(file1_unique)}")
    print(f"文件2独有的发明名称数量: {len(file2_unique)}")
    print("\n前5个独有发明名称示例:")
    print("\n文件1独有:")
    for name in file1_unique[:5]:
        print(f"- {name}")
    print("\n文件2独有:")
    for name in file2_unique[:5]:
        print(f"- {name}")

    return results


# 使用示例
file1_path = r"C:\Users\wang\Desktop\专利信息输出.xlsx"  # 替换为你的第一个文件路径
file2_path = r"C:\Users\wang\Desktop\2024年专利-分学院-计算机.xlsx"  # 替换为你的第二个文件路径

# 运行比较
results = compare_invention_names(file1_path, file2_path)