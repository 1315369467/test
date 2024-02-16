import torch
import numpy as np
from sklearn.decomposition import FastICA
import matplotlib.pyplot as plt

# 生成混合信号
np.random.seed(42)
t = np.linspace(0, 5, 1000)
s1 = np.sin(2 * np.pi * t)  # 原始信号1
s2 = np.random.random(t.shape[0])  # 原始信号2
S = np.c_[s1, s2]  # 原始信号矩阵

# 混合信号
A = np.array([[1, 1], [0.5, 2]])  # 混合矩阵
X = S.dot(A.T)  # 混合后的信号矩阵

# 使用FastICA进行独立成分分析
ica = FastICA(n_components=2)
S_ = ica.fit_transform(X)  # 估计的独立成分

# 绘制结果
plt.figure(figsize=(8, 6))

plt.subplot(3, 1, 1)
plt.title('Original Signals')
plt.plot(S)

plt.subplot(3, 1, 2)
plt.title('Mixed Signals')
plt.plot(X)

plt.subplot(3, 1, 3)
plt.title('ICA Recovered Signals')
plt.plot(S_)

plt.tight_layout()
plt.show()
