"""
==========
plot(x, y)
==========

See `~matplotlib.axes.Axes.plot`.
"""

import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
import numpy as np

# plt.style.use('_mpl-gallery')

# 生成数据
x = [1, 2, 3]
y = np.array([[1, 2], [3, 4], [5, 6]])
# plt.plot(x, y)

plot([1, 2, 3], [1, 2, 3], 'go:', label='line 1', linewidth=2)
plot([1, 2, 3], [1, 4, 9], 'rs-', label='line 2')


# # 创建画布和子图
# fig, ax = plt.subplots()
# # 绘制曲线
# ax.plot(x, y, linewidth=2.0)
# # 设置横轴和纵轴的范围和刻度
# ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))
# # 显示图形
plt.show()

