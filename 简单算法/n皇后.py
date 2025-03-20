def solve_n_queens(n):
    results = []  # 初始化结果列表，用于存储所有可能的N皇后布局

    # 检查当前放置的皇后是否安全的辅助函数
    def is_safe(queens, row, col):
        # 遍历已经放置的皇后，检查是否在同一列或同一对角线上
        for r in range(row):
            c = queens[r]  # 获取当前行的皇后列
            if c == col or abs(c - col) == abs(r - row):  # 同一列或同一对角线上
                return False
        return True

    # 回溯法递归放置皇后的函数
    def place_queens(queens, row):
        if row == n:  # 如果所有行都放置了皇后，保存当前布局
            results.append(queens[:])
            return
        # 尝试在当前行的每一列放置皇后
        for col in range(n): # 遍历每一列
            if is_safe(queens, row, col):  # 如果安全，则放置皇后
                queens[row] = col
                place_queens(queens, row + 1)  # 递归尝试下一行
                queens[row] = -1  # 回溯：移除当前行的皇后

    queens = [-1] * n  # 初始化皇后位置数组，-1表示尚未放置皇后
    place_queens(queens, 0)  # 开始递归放置皇后，从第0行开始
    return results


def generate_and_print_solutions(solutions, n):  # 打印所有解决方案
    # 遍历所有解决方案
    for queens in solutions:
        for r in queens:
            row = ['.'] * n
            row[r] = 'Q'  # 在对应位置放置皇后
            print(''.join(row))
        print()
    print(solutions)
    print("Found", len(solutions), "solutions:")


# 测试函数
n = 4
solutions = solve_n_queens(n)  # 获取所有解决方案
generate_and_print_solutions(solutions, n)  # 打印所有解决方案
