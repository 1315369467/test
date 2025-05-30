class Solution:
    def isPalindrome(self, x: int) -> bool:
        x = str(x)
        n = len(x)
        if n==1:
            return True
        for i in range(0, n // 2):
            if x[i] != x[n - i - 1]:
                return False
        return True


print(Solution.isPalindrome(1, 1000021))
