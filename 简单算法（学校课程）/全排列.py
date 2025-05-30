def permute(nums, depth=0):
    """生成列表的所有排列，添加调试信息显示递归深度和过程"""
    # 显示当前递归深度和处理的子列表
    print(f"{'  ' * depth}permute({nums}), depth={depth}")
    if len(nums) == 0:
        return [[]]
    result = []
    for i in range(len(nums)):
        rest = nums[:i] + nums[i + 1:]
        # 递归调用前打印信息
        print(f"{'  ' * depth}Choosing element {nums[i]} at depth {depth}")
        for p in permute(rest, depth + 1):
            # 将当前元素添加到剩余元素的排列前面，形成新的排列
            result.append([nums[i]] + p)
            # 显示生成的排列
            print(f"{'  ' * (depth + 1)}Formed permutation: {[nums[i]] + p}")
    return result


# 示例
nums = [1, 2, 3, 4, 5]
perms = permute(nums)
# 由于输出可能会很长，这里不直接运行代码。你可以在本地环境中运行以查看详细的调试输出。
