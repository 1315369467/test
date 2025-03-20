import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.gridspec import GridSpec

# 示例预测标签和真实标签
y_true = [0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]
ours = [0,3,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,4,4,0,1,2,3,4,2,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,1,4,0,1,2,3,4,3,1,2,1,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]
protoPL = [2,3,2,3,4,0,1,2,3,4,0,3,2,3,4,0,1,2,4,4,0,1,2,3,4,2,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,1,4,2,1,2,3,4,3,1,2,1,4,0,1,2,3,4,0,3,2,3,4,0,1,2,1,4,0,1,2,3,4]
PUTM = [2,3,2,3,4,0,1,2,3,4,0,3,2,3,4,0,1,2,4,4,0,1,2,3,4,2,1,0,3,4,0,1,0,3,4,0,1,2,3,4,0,1,2,1,4,2,1,0,0,4,3,1,2,1,4,0,1,2,3,4,0,1,2,3,4,0,1,0,1,4,0,1,2,3,4]

# 计算混淆矩阵
cm_ours = confusion_matrix(y_true, ours)
cm_protoPL = confusion_matrix(y_true, protoPL)
cm_PUTM = confusion_matrix(y_true, PUTM)
cm_gt = confusion_matrix(y_true, y_true)  # Ground Truth 对角线全是正确的

# 创建图表
fig = plt.figure(figsize=(10, 4))
gs = GridSpec(1, 5, width_ratios=[1, 1, 1, 1, 0.05])

# 定义颜色标尺的最大值和最小值以保持一致性
vmin = min(cm_ours.min(), cm_protoPL.min(), cm_PUTM.min(), cm_gt.min())
vmax = max(cm_ours.max(), cm_protoPL.max(), cm_PUTM.max(), cm_gt.max())

# 绘制混淆矩阵
ax0 = plt.subplot(gs[0, 2])
sns.heatmap(cm_ours, fmt='d', cmap='plasma', ax=ax0, cbar=False, vmin=vmin, vmax=vmax, square=True)
ax0.set_title('Ours')
ax0.set_xticks([])
ax0.set_yticks([])


ax1 = plt.subplot(gs[0, 1])
sns.heatmap(cm_protoPL, fmt='d', cmap='plasma', ax=ax1, cbar=False, vmin=vmin, vmax=vmax, square=True)
ax1.set_title('ProtoPL')
ax1.set_xticks([])
ax1.set_yticks([])

ax2 = plt.subplot(gs[0, 0])
sns.heatmap(cm_PUTM, fmt='d', cmap='plasma', ax=ax2, cbar=False, vmin=vmin, vmax=vmax, square=True)
ax2.set_title('PUTM')
ax2.set_xticks([])
ax2.set_yticks([])

ax3 = plt.subplot(gs[0, 3])
sns.heatmap(cm_gt, fmt='d', cmap='plasma', ax=ax3, cbar=False, vmin=vmin, vmax=vmax, square=True)
ax3.set_title('Ground Truth')
ax3.set_xticks([])
ax3.set_yticks([])

# 添加共享colorbar
cax = plt.subplot(gs[0, 4])
plt.colorbar(ax3.collections[0], cax=cax)

# plt.suptitle('Confusion Matrix on the Balanced Setting')
plt.tight_layout(rect=[0, 0, 0.95, 1])  # 调整图像范围以适应标题
plt.show()
