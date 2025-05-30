def knapsack(i, cw, items, max_weight, best_weight):
    global bestw
    n = len(items)

    # 如果已遍历完所有物品，或当前总重量已达到最大重量
    if i >= n or cw == max_weight:
        if cw > bestw:
            bestw = cw
            best_weight[:] = current_weight[:]
        return

    # 不装第 i 个物品的情况
    knapsack(i + 1, cw, items, max_weight, best_weight)

    # 装第 i 个物品的情况（前提是加上这个物品不超过最大载重）
    if cw + items[i] <= max_weight:
        current_weight[i] = 1  # 标记这个物品被装载
        knapsack(i + 1, cw + items[i], items, max_weight, best_weight)
        current_weight[i] = 0  # 还原状态，以便回溯


# 测试数据
items = [20, 10, 30, 40]  # 各物品的重量
max_weight = 50  # 最大载重量
bestw = 0  # 找到的最大装载重量
current_weight = [0] * len(items)  # 跟踪哪些物品被选中
best_weight = [0] * len(items)  # 记录最优装载方案

knapsack(0, 0, items, max_weight, best_weight)
print("Maximum weight in the knapsack:", bestw)
print("Items included in the knapsack:", best_weight)
