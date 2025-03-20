import matplotlib.pyplot as plt

# 估计的数据
alpha_dir = [1, 2, 3, 4, 5, 6]
# ours = [87.5, 88.0, 88.5, 89.0, 89.3, 89.5]
# protolp = [80.0, 85.5, 87.0, 87.6, 88.0, 88.3]
# putm = [85.5, 85.8, 86.0, 86.1, 86.2, 86.2]
# alpha_tim = [82.0, 82.5, 83.0, 83.5, 83.5, 84.0]
# tim = [81.0, 82.0, 83.0, 83.5, 83.5, 83.5]
# pt_map = [72.0, 73.5, 75.0, 76.5, 78.0, 79.5]



ours = [87.5, 88.0, 88.5, 89.0, 89.3, 89.5]
protolp = [80.0, 85.5, 87.0, 87.6, 88.0, 88.3]
putm = [85.5, 85.8, 86.0, 86.1, 86.2, 86.2]
# 创建图表
plt.figure(figsize=(6, 5))
plt.plot(alpha_dir, ours, 's-', label='Ours', color='red')
plt.plot(alpha_dir, protolp, '^-', label='ProtoLP', color='blue')
plt.plot(alpha_dir, putm, 'o-', label='PUTM', color='green')
# plt.plot(alpha_dir, alpha_tim, 'd-', label='α-TIM', color='orange')
# plt.plot(alpha_dir, tim, 'p-', label='TIM', color='brown')
# plt.plot(alpha_dir, pt_map, 'h-', label='PT-MAP', color='gray')

# 添加标签和标题
plt.xlabel('Imbalanced Coefficient $\\alpha_{dir}$')
plt.ylabel('Mean Accuracy (%)')
plt.title('mini-ImageNet 5-way 5-shot')
plt.legend()
plt.grid(True)

# 显示图表
plt.show()
