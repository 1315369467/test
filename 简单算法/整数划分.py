def print_integer_partitions_desc(n, max_val=None, partition=[]):
    """
    输出整数n的所有划分，其中划分中的数首先输出最大的数且递减。

    参数:
    - n: 需要划分的整数。
    - max_val: 可以加入划分的最大值，初始时未指定。
    - partition: 当前划分的部分，初始为空列表。
    """
    # 如果n为0，说明已经找到了一个完整的划分
    if n == 0:
        # 将当前划分中的数字转换为字符串，然后用' + '连接，最后打印
        print(' + '.join(map(str, partition)))
        return

    # 如果max_val未指定，设置为n，表示划分中可以包含n本身
    if max_val is None:
        max_val = n

    # 从max_val开始向下遍历，直到1
    for i in range(max_val, 0, -1):
        # 只有当当前数字i不大于n时，才考虑将其加入到划分中
        if i <= n:
            # 将i加入到当前划分的副本中，递归调用函数处理剩余的部分(n-i)
            # 同时，将i作为下一步的max_val，确保划分中的数递减
            print_integer_partitions_desc(n - i, i, partition + [i])


# 示例：输出整数4的所有划分，先输出最大的数，且输出的数递减
print_integer_partitions_desc(20)
