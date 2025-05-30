import pandas as pd
import matplotlib.pyplot as plt

# 数据文件路径
file_path = 'master.csv'

# 读取CSV数据
with open(file_path, 'r') as file:
    lines = file.readlines()

# 解析数据，提取各数据集
datasets = {}
current_dataset = None
for line in lines:
    line = line.strip()
    if line == "":  # 跳过空行
        continue
    if line.split(",")[0] not in ["Tip-Adapter-F","GraphAdapter", "CaFo", "AMU-Tuning ", "Ours"]:  # 如果是数据集名
        current_dataset = line.split(",")[0]
        datasets[current_dataset] = []
    else:  # 如果是方法及其数据
        datasets[current_dataset].append(line.split(","))

# 删除空数据集（即无方法和数据的情况）
datasets = {key: value for key, value in datasets.items() if len(value) > 0}

# 创建2行5列的子图
fig, axes = plt.subplots(2, 5, figsize=(16, 6.5))
x_ticks = [1, 2, 4, 8, 16]  # 横轴为训练样本数
x_labels = ["1-shot", "2-shot", "4-shot", "8-shot", "16-shot"]  # 横轴标签

# 遍历数据集，绘制每个子图
for idx, (dataset, methods) in enumerate(datasets.items()):
    row, col = divmod(idx, 5)
    ax = axes[row, col]
    ax.set_title(dataset)
    for method_data in methods:
        method_name = method_data[0].strip()  # 方法名称
        scores = list(map(float, method_data[1:]))  # 方法对应的分数
        ax.plot(
            x_ticks,  # 横轴
            scores,  # y轴
            label=method_name,
            marker="o"
        )
    ax.set_xlabel("Number of training samples per class")
    ax.set_ylabel("Score(%)")
    ax.set_xticks(x_ticks)
    ax.legend(fontsize=8)  # 设置图例字体较小以适应子图
    ax.grid(True)

# 隐藏多余的子图（如果数据集不足10个）
for idx in range(len(datasets), 10):
    row, col = divmod(idx, 5)
    axes[row, col].axis("off")

# 调整布局
plt.tight_layout()
plt.show()
