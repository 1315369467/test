from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

# root =[1,2,3,4,5,null,8,null,null,6,7,9]
# 预期结果 [4,2,6,5,7,1,3,9,8]

class Solution:
	def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
		if root is None:
			return []
		return self.inorderTraversal(root.left) + self.inorderTraversal(root.right)+ [root.val]

# Helper function to build a tree from a list
def buildTree(arr):
	if not arr:
		return None
	root = TreeNode(arr[0])
	queue = [root]
	i = 1
	while queue and i < len(arr):
		node = queue.pop(0)
		if arr[i] is not None:
			node.left = TreeNode(arr[i])
			queue.append(node.left)
		i += 1
		if i < len(arr) and arr[i] is not None:
			node.right = TreeNode(arr[i])
			queue.append(node.right)
		i += 1
	return root

# 测试代码
if __name__ == '__main__':
	# Test case 1: Full binary tree
	root = buildTree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
	sol = Solution()
	print(sol.inorderTraversal(root))  # Expected output: [4, 2, 6, 5, 7, 1, 3, 9, 8]

	# Test case 2: Tree with only right children
	root = buildTree([1, None, 2, None, 3])
	print(sol.inorderTraversal(root))  # Expected output: [1, 3, 2]

	# Test case 3: Empty tree
	root = buildTree([])
	print(sol.inorderTraversal(root))  # Expected output: []

	# Test case 4: Single node tree
	root = buildTree([1])
	print(sol.inorderTraversal(root))  # Expected output: [1]



