import numpy as np

import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
# 创建一个示例的 100x100 的张量
A = np.arange(0, 100).reshape(10, 10)**2  # 生成随机数据，你可以替换成你的张量数据
A=(A.mean()-A)
# 绘制热力图
plt.figure(figsize=(8, 6))
plt.imshow(A, cmap='coolwarm')  # cmap可以根据你的需求选择不同的颜色映射
plt.colorbar()  # 添加颜色条，用于标识值和颜色的对应关系
plt.title('Heatmap of Tensor A')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
