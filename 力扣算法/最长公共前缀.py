# https://leetcode.cn/problems/longest-common-prefix/solutions/288575/zui-chang-gong-gong-qian-zhui-by-leetcode-solution/
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""

        length, count = len(strs[0]), len(strs)  # 获取第一个字符串的长度和字符串列表的长度
        for i in range(length):                   # 遍历第一个字符串的每个字符                   # 获取当前字符
            for j in range(1, count):             # 从第二个字符串开始比较
                if i == len(strs[j]) or strs[j][i] != strs[0][i]:  # 如果当前索引超出某个字符串的长度，或者字符不匹配
                    return strs[0][:i]            # 返回当前找到的最长公共前缀

        return strs[0]

#测试代码
if __name__ == '__main__':
    solution = Solution()

    # 测试用例1
    strs1 = ["flower", "flow", "flight"]
    expected1 = "fl"
    result1 = solution.longestCommonPrefix(strs1)
    assert result1 == expected1

    # 测试用例2
    strs2 = ["dog", "racecar", "car"]
    expected2 = ""
    result2 = solution.longestCommonPrefix(strs2)
    assert result2 == expected2
