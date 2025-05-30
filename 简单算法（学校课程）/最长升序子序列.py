def lengthOfLIS_verbose(nums):
    if not nums:
        return 0

    dp = [1] * len(nums)  # 初始化dp数组
    print("Initial dp:", dp)  # 打印初始化的dp数组
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
        print(f"dp after processing element {nums[i]} (index {i}):", dp)  # 打印每一步的dp数组

    return max(dp)


# 示例数组
nums = [10, 9, 2, 5, 3, 7, 4, 5]
lengthOfLIS_verbose(nums)
