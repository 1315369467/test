import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# 设置参数
num_classes = 5
samples_per_class = 15
num_features = 10

# 生成数据
data = []
labels = []
for i in range(num_classes):
    mean = np.random.rand(num_features) * 10  # 随机生成均值
    cov = np.random.rand(num_features, num_features)
    cov = np.dot(cov, cov.transpose())  # 生成协方差矩阵

    class_data = np.random.multivariate_normal(mean, cov, samples_per_class)
    class_labels = np.full(samples_per_class, i)

    data.append(class_data)
    labels.append(class_labels)

# 将数据和标签转换成NumPy数组
data_np = np.vstack(data)
labels_np = np.concatenate(labels)

# 使用t-SNE进行降维
tsne = TSNE(n_components=2, random_state=0)
data_2d = tsne.fit_transform(data_np)

# 绘制t-SNE散点图
plt.figure(figsize=(10, 6))

for i in range(num_classes):
    idxs = labels_np == i
    plt.scatter(data_2d[idxs, 0], data_2d[idxs, 1], label=f"Class {i}")
plt.title("t-SNE Visualization of Gaussian Distributed Features")
plt.xlabel("t-SNE Feature 1")
plt.ylabel("t-SNE Feature 2")
plt.legend()
plt.show()
