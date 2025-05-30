class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        leftlist=[]
        rightlist=[]
        lmax=height[0]
        rmax=height[-1]
        for i in height:
            lmax = max(i,lmax)
            leftlist.append(lmax)
        for i in height[::-1]:
            rmax = max(i,rmax)
            rightlist.append(rmax)
        rightlist.reverse()
        ans=0
        for i in range(len(height)):
            ans += min(leftlist[i],rightlist[i])-height[i]
        return ans







Solution().trap([0,1,0,2,1,0,1,3,2,1,2,1])
