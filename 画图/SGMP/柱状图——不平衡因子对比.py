import matplotlib.pyplot as plt
import numpy as np

# 数据
imbalance_coefficients = [1, 2, 3, 4]
protoPL = [68.7, 73.6, 76.0, 77.6]
PUTM = [70.1, 73.2, 74.4, 75.1]
our = [72.2, 76.4, 77.8, 78.8]

# 设置柱状图的位置
bar_width = 0.2
index = np.arange(len(imbalance_coefficients))

# 创建柱状图
fig, ax = plt.subplots(figsize=(6, 4))

bar1 = ax.bar(index - bar_width, protoPL, bar_width, label='ProtoPL')
bar2 = ax.bar(index, PUTM, bar_width, label='PUTM')
bar3 = ax.bar(index + bar_width, our, bar_width, label='ours')

# 添加标签和标题
plt.xlabel('Imbalanced Coefficient ')
plt.ylabel('Mean Accuracy (%)')
plt.title('mini-ImageNet 5-way 1-shot')
ax.set_xticks(index)
ax.set_xticklabels(imbalance_coefficients)
ax.set_ylim([66, 80])
ax.legend()

# 显示图表
plt.show()
