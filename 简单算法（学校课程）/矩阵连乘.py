import numpy as np

# 矩阵的维度 (p[i-1] x p[i])
p = [30, 40, 15, 5, 20, 10, 25]

# 矩阵数量
n = len(p) - 1

# 初始化 m 和 s
m = np.zeros((n+1, n+1), dtype=int)
s = np.zeros((n+1, n+1), dtype=int)

# 动态规划填表
for l in range(2, n+1):  # l是链的长度
    for i in range(1, n-l+2):  # i是计算的起点
        j = i + l - 1  # j是计算的终点
        m[i][j] = 1e9  # 初始化为无穷大
        for k in range(i, j):
            # 计算分割点
            q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]
            if q < m[i][j]:  # 更新最小值
                m[i][j] = q
                s[i][j] = k  # 记录分割点

# m = m[1:,1:]  # 调整矩阵，以便输出从1开始计数
# s = s[1:,1:]
print(m)
print(s)
def print_optimal_parens(s, i, j):
    """递归打印最优的矩阵链乘法括号位置"""
    if i == j:
        print(f"A{i}", end="")
    else:
        print("(", end="")
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(")", end="")

# 调用函数打印 A1 到 A6 的最优乘法顺序
print_optimal_parens(s, 1, 6)
