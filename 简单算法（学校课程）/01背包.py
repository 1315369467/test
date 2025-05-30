import numpy as np


def knapsack_01_numpy(n, c, w, v):
    dp = np.zeros((n + 1, c + 1), dtype=int) # 使用numpy数组初始化动态规划表格

    # 填充动态规划表格
    for i in range(1, n + 1): # 遍历物品
        for j in range(1, c + 1): # 遍历背包容量
            if j >= w[i - 1]:  # 如果当前背包容量可以放下当前物品
                dp[i, j] = max(dp[i - 1, j], dp[i - 1, j - w[i - 1]] + v[i - 1]) # 选择当前物品或者不选择当前物品
            else:
                dp[i, j] = dp[i - 1, j] # 否选择当前物品

    # 从动态规划表格中找出最大价值及其对应的物品
    max_value = dp[n, c]
    print(dp)
    items_chosen = []
    capacity = c
    for i in range(n, 0, -1):
        a,b=dp[i, capacity],dp[i-1,capacity] #
        if a != b:
            items_chosen.append(i) # 将物品添加到已选择的物品列表中
            capacity -= w[i - 1] # 背包容量减去当前物品的重量

    # 反转使得物品的顺序是从1到n
    items_chosen.reverse()
    print("最大价值：", max_value)
    print("已选择的物品：", items_chosen)
    return max_value, items_chosen

# 给定参数
n = 5 #·物品数量
c = 10 # 背包容量
w = [2,2,6,5,4] # 物品重量
v = [6,3,5,4,6] # 物品价值
# 调用01背包问题解决函数（使用numpy）
knapsack_01_numpy(n, c, w, v) # 输出结果
