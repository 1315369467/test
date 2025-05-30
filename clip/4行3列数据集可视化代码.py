import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 数据文件路径
file_path = '11数据集average.csv'

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
    if line.split(",")[0] not in ["Tip-Adapter-F", "GraphAdapter", "CaFo", "AMU-Tuning ", "Ours"]:  # 如果是数据集名
        current_dataset = line.split(",")[0]
        datasets[current_dataset] = []
    else:  # 如果是方法及其数据
        datasets[current_dataset].append(line.split(","))

# 删除空数据集（即无方法和数据的情况）
datasets = {key: value for key, value in datasets.items() if len(value) > 0}

# 创建4行3列的子图
fig, axes = plt.subplots(4, 3, figsize=(12, 14))
# fig.suptitle('各数据集在不同训练样本数下的准确率对比', fontsize=16)
x_ticks = [1, 2, 4, 8, 16]  # 横轴为训练样本数
x_labels = ["1-shot", "2-shot", "4-shot", "8-shot", "16-shot"]  # 横轴标签
method_colors = {
    "Tip-Adapter-F": 'blue',
    "GraphAdapter": 'green',
    "CaFo": 'red',
    "AMU-Tuning": 'purple',
    "Ours": 'orange'
}
method_markers = {
    "Tip-Adapter-F": 'o',
    "GraphAdapter": 's',
    "CaFo": '^',
    "AMU-Tuning": 'D',
    "Ours": 'x'
}

# 对数据集进行排序（可以自定义排序规则）
dataset_names = list(datasets.keys())

# 遍历数据集，绘制每个子图
for idx, dataset in enumerate(dataset_names):
    if idx >= 12:  # 如果数据集超过12个，则只显示前12个
        break

    row, col = divmod(idx, 3)
    ax = axes[row, col]

    methods = datasets[dataset]
    for method_data in methods:
        method_name = method_data[0].strip()  # 方法名称

        # 处理可能的数据格式问题
        scores = []
        for score_str in method_data[1:6]:  # 假设只有5个数据点
            try:
                score = float(score_str)
                scores.append(score)
            except (ValueError, IndexError):
                scores.append(np.nan)  # 对于无效数据使用NaN

        # 确保数据点数量正确
        while len(scores) < 5:
            scores.append(np.nan)

        # 过滤掉NaN值
        valid_indices = [i for i, score in enumerate(scores) if not np.isnan(score)]
        valid_x = [x_ticks[i] for i in valid_indices]
        valid_scores = [scores[i] for i in valid_indices]

        if valid_scores:  # 只有当有有效数据时才绘图
            color = method_colors.get(method_name, 'gray')  # 如果方法未定义颜色，则使用灰色
            marker = method_markers.get(method_name, '*')  # 如果方法未定义标记，则使用星号

            ax.plot(
                valid_x,
                valid_scores,
                label=method_name,
                marker=marker,
                # color=color
            )

    # 设置子图标题和坐标轴
    ax.set_title(dataset)
    ax.set_xlabel("Number of training samples per class")
    ax.set_ylabel("Score(%)")
    ax.set_xticks(x_ticks)
    ax.legend(fontsize=6)  # 设置图例字体较小以适应子图
    ax.grid(True)



# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])  # 为标题留出空间
plt.savefig("各数据集对比图.png", dpi=300, bbox_inches="tight")
plt.show()