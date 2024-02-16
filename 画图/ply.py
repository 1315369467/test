import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# epoch,acc,loss,val_acc,val_loss
x_axis_data = [1, 5, 10, 20, 30]
y_axis_data1 = [82.8, 94.8, 96.9, 98.4, 99.0]
y_axis_data2 = [84.3, 95.6,097.4, 98.7, 99.1]

# 画图
plt.plot(x_axis_data, y_axis_data2, 'rs-', alpha=0.5,label='改进方法')
plt.plot(x_axis_data, y_axis_data1, 'bo:', alpha=0.5,label='baseline')


## 设置数据标签位置及大小
for a, b in zip(x_axis_data, y_axis_data1):
    plt.text(a, b, str(b), ha='center', va='top', fontsize=13)  # ha='center', va='top'
for a, b1 in zip(x_axis_data, y_axis_data2):
    plt.text(a, b1, str(b1), ha='center', va='bottom', fontsize=13)
plt.legend()  # 显示上面的label

plt.xlabel('rank')
plt.ylabel('匹配率/%')  # accuracy

plt.ylim(80,100)#仅设置y轴坐标范围
plt.show()