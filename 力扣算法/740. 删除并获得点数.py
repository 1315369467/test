# https://leetcode.cn/problems/delete-and-earn/description/?envType=study-plan-v2&envId=dynamic-programming
def deleteAndEarn(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    # 统计每个数字出现的次数
    count = {}
    for num in nums:
        count[num] = count.get(num, 0) + 1

    # 找出最大的数字，用于确定数组大小
    max_num = max(nums)

    # 创建一个数组，索引为数字，值为选择该数字可获得的点数
    points = [0] * (max_num + 1)
    for num in count:
        points[num] = num * count[num]

    # 动态规划
    dp = [0] * (max_num + 1)
    dp[1] = points[1]  # 基础情况

    # 对于每个数字，我们有两种选择：选择它（并跳过前一个数字）或不选择它
    for i in range(2, max_num + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + points[i])

    return dp[max_num]
#测试代码
nums = [3,4,2,3,4,3,4]
print(deleteAndEarn(nums))