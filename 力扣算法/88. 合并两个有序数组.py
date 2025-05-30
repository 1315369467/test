class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        list=[]
        i=0
        j=0
        while i<m and j<n:
            if nums1[i]<=nums2[j]:
                list.append(nums1[i])
                i+=1
            else:
                list.append(nums2[j])
                j+=1
        if i==m:
            while j!=n:
                list.append(nums2[j])
                j+=1
        else:
            while i!=m:
                list.append(nums1[i])
                i+=1
        # 将合并后的数组赋值给nums1
        nums1[:]=list
        return nums1

#测试代码
if __name__ == '__main__':
    solution = Solution()

    # 测试用例1
    nums1 = [1, 2, 3, 0, 0, 0]
    m = 3
    nums2 = [2, 5, 6]
    n = 3
    solution.merge(nums1, m, nums2, n)
    print(nums1)  # 输出：[1, 2, 2, 3, 5, 6]