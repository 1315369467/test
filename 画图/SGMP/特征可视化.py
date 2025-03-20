import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# 生成示例数据
np.random.seed(0)
X = np.random.rand(80, 5)  # 特征矩阵
Y = np.random.randint(0, 2, 80)  # 预测标签

# 执行t-SNE
tsne = TSNE(n_components=2, random_state=1)
X_tsne = tsne.fit_transform(X)

# 绘制t-SNE结果
plt.figure(figsize=(6, 4))
scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=Y, cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label='Label')
plt.title('t-SNE Visualization of X with Labels')
plt.xlabel('t-SNE feature 1')
plt.ylabel('t-SNE feature 2')
plt.show()
