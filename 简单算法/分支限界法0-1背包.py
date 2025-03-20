class Node:
    def __init__(self, lev, cv, cw):
        self.lev = lev  # 当前节点在搜索树中的层次
        self.cv = cv  # 当前节点的总价值
        self.cw = cw  # 当前节点的总重量

def bound(node, n, W, w, v):
    if node.cw >= W:
        return 0  # 超过容量返回0
    cv_bound = node.cv  # 初始化为当前节点的总价值
    j = node.lev + 1  # 从下一个层次开始
    total_w = node.cw  # 初始化为当前节点的总重量
    # 尽可能多地装入物品
    while j < n and total_w + w[j] <= W:
        total_w += w[j]
        cv_bound += v[j]
        j += 1
    # 如果还有剩余容量，可以装入部分物品
    if j < n:
        cv_bound += (W - total_w) * v[j] / w[j]  # 剩余容量乘以价值密度
    return cv_bound  # 返回计算出的上界

def knapsack_bb(n, W, w, v):
    # 按照价值密度排序
    items = sorted(range(n), key=lambda i: v[i] / w[i], reverse=True)
    max_v = 0  # 初始化最大价值
    queue = [Node(-1, 0, 0)]  # 初始化队列，包含根节点
    while queue:
        node = queue.pop(0)  # 取出队列中的第一个节点
        # 如果已经处理完所有层次，跳过
        if node.lev == n - 1:
            continue
        lev = node.lev + 1  # 下一个层次

        # 选择下一个物品（包含当前物品）
        with_item = Node(lev, node.cv + v[items[lev]], node.cw + w[items[lev]])
        if with_item.cw <= W and with_item.cv > max_v:
            max_v = with_item.cv  # 更新最大价值
        if bound(with_item, n, W, w, v) > max_v:
            queue.append(with_item)  # 将节点添加到队列

        # 不选择下一个物品（不包含当前物品）
        without_item = Node(lev, node.cv, node.cw)
        if bound(without_item, n, W, w, v) > max_v:
            queue.append(without_item)  # 将节点添加到队列
    return max_v  # 返回最大价值

# 测试用例
n = 4  # 物品总数
W = 10  # 背包的容量
w = [2, 3, 4, 5]  # 物品的重量
v = [3, 4, 5, 6]  # 物品的价值

print("最大价值为:", knapsack_bb(n, W, w, v))
