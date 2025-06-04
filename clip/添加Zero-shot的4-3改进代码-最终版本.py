import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 数据文件路径
# file_path = '主_11数据集average.csv'
# file_path = '主_11数据集average - 副本.csv'
file_path = '主_11数据集average - new.csv'

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

# 添加Zero-shot CLIP数据
zero_shot_data = {
    "FGVCAircraft": 17.28,
    "Caltech101": 86.29,
    "StandfordCars": 55.61,
    "DTD": 42.32 ,
    "EuroSAT": 37.56,
    "Flowers102": 66.14,
    "Food101": 77.20,
    "ImageNet-1K": 60.33,
    "OxfordPets": 85.77,
    "SUN397": 58.52,
    "UCF101": 61.46,
    "Average over 11 datasets": 58.95
}

# 创建4行3列的子图
fig, axes = plt.subplots(4, 3, figsize=(15, 16))
# 修改x轴刻度，添加0-shot
x_ticks = [0, 1, 2, 4, 8, 16]  # 添加了0用于zero-shot
x_labels = ["0-shot", "1-shot", "2-shot", "4-shot", "8-shot", "16-shot"]  # 添加了0-shot标签

# method_colors = {
#     "Tip-Adapter-F": 'purple',  # 修改为图中的颜色
#     "GraphAdapter": 'green',
#     "CaFo": 'orange',
#     "AMU-Tuning": 'blue',  # CoOp在图中是蓝色
#     "Ours": 'red',
#     "Zero-shot CLIP": 'purple'  # Zero-shot为紫色
# }
method_markers = {
    "Tip-Adapter-F": '*',  # 星形标记
    "GraphAdapter": 'o',  # CLIP-Adapter用圆形
    "CaFo": 's',
    "AMU-Tuning": 'o',  # CoOp用圆形
    "Ours": 'D',
    "Zero-shot CLIP": 'D'  # Zero-shot用菱形
}

# 对数据集进行排序（可以自定义排序规则）
dataset_names = list(datasets.keys())

# 遍历数据集，绘制每个子图
for idx, dataset in enumerate(dataset_names):
    if idx >= 12:  # 如果数据集超过12个，则只显示前12个
        break

    row, col = divmod(idx, 3)
    ax = axes[row, col]

    # 先添加Zero-shot数据点
    if dataset in zero_shot_data:
        ax.scatter(0, zero_shot_data[dataset],
                   color="brown",
                   marker=method_markers["Zero-shot CLIP"],
                   s=50,
                   label="Zero-shot CLIP")


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

        # 过滤掉NaN值，但保留索引位置（从1开始，因为0位置是zero-shot）
        valid_indices = [i for i, score in enumerate(scores) if not np.isnan(score)]
        valid_x = [x_ticks[i + 1] for i in valid_indices]  # +1因为x_ticks现在从0开始
        valid_scores = [scores[i] for i in valid_indices]

        if valid_scores:  # 只有当有有效数据时才绘图
            # color = method_colors.get(method_name, 'gray')  # 如果方法未定义颜色，则使用灰色
            marker = method_markers.get(method_name, '*')  # 如果方法未定义标记，则使用星号

            ax.plot(
                valid_x,
                valid_scores,
                label=method_name,
                marker=marker,
                # color=color,
                linewidth=2
            )
            from matplotlib.ticker import MaxNLocator

            # 假设你已经有一个图表对象 ax
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))


    # 设置子图标题和坐标轴
    ax.set_title(dataset, fontsize=14)
    ax.set_xlabel("Number of labeled training examples per class", fontsize=12)
    ax.set_ylabel("Score(%)", fontsize=12)
    ax.set_xticks(x_ticks)
    ax.legend(loc='lower right', fontsize=10)  # 调整图例位置和大小
    ax.grid(True, linestyle='--', alpha=0.7)


# 调整布局并保存图片
plt.tight_layout(rect=[0, 0, 1, 0.96])  # 为标题留出空间
plt.savefig("各数据集对比图_含zero_shot.png", dpi=300, bbox_inches="tight")
plt.show()