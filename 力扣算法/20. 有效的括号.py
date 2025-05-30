def isValid(s: str) -> bool:
    """
    判断字符串中的括号是否有效

    参数:
    s (str): 只包含括号的字符串 '(', ')', '{', '}', '[', ']'

    返回:
    bool: 如果括号有效返回True，否则返回False
    """
    # 如果字符串长度为奇数，肯定不是有效的括号序列
    if len(s) % 2 != 0:
        return False

    # 定义括号对应关系的字典（右括号:左括号）
    dic = {')': '(', '}': '{', ']': '['}

    # 创建一个栈
    stack = []

    # 遍历字符串中的每个字符
    for char in s:
        # 如果是左括号，入栈
        if char not in dic:
            stack.append(char)
        # 如果是右括号，检查栈是否为空或栈顶元素是否匹配
        elif not stack or stack.pop() != dic[char]:
            return False

    # 最后检查栈是否为空
    return len(stack) == 0


# 测试示例
print(isValid("()"))  # 应输出: True
print(isValid("()[]{}"))  # 应输出: True
print(isValid("(]"))  # 应输出: False
print(isValid("([)]"))  # 应输出: False
print(isValid("{[]}"))  # 应输出: True