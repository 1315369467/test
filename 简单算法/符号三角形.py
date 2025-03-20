import numpy as np


def compute(n):
    """
    计算符号三角形的数量，判断符号总个数是否为偶数并调整 half 为单个符号的个数。
    """
    half = n * (n + 1) // 2
    if half % 2 == 1:  # 符号总个数为奇数，不可能出现 "+"、"-" 个数相等的情况
        return 0
    half //= 2  # 符号总个数为偶数，将 half 设置为 "+" 或 "-" 的个数
    count = 0  # "+" 符号的个数
    sum = 0  # 符号三角形的数量
    p = np.zeros((n + 1, n + 1), dtype=int)
    sum = backtrack(n, 1, half, count, sum, p)
    return sum


def backtrack(n, t, half, count, sum, p):  # t 表示当前行，count 表示当前行 "+" 符号的个数
    # 当前 "+" 符号个数或 "-" 符号个数已超过 half
    if count > half or (t * (t - 1) // 2 - count > half):
        return sum

    if t > n:  # 已构造出一个符合要求的符号三角形
        sum += 1  # 符号三角形数量加 1
        print_triangle(p, n)
        return sum
    else:
        for i in range(2):
            p[1][t] = i  # 设置第 t 个符号
            count += i  # 更新 "+" 符号的计数
            # 根据当前行和前一行符号，确定当前行的符号
            for j in range(2, t + 1):
                p[j][t - j + 1] = p[j - 1][t - j + 1] ^ p[j - 1][t - j + 2]  # 异或操作确定符号
                count += p[j][t - j + 1]
            sum = backtrack(n, t + 1, half, count, sum, p)  # 递归调用下一行
            # 回溯时恢复状态
            for j in range(2, t + 1):
                count -= p[j][t - j + 1]
            count -= i
    return sum


def print_triangle(p, n):
    # 打印符号三角形的函数
    for i in range(1, n + 1):
        for k in range(1, i):
            print(" ", end="")
        for j in range(1, n + 1):
            if p[i][j] == 0 and j <= n - i + 1:
                print("+ ", end="")
            elif p[i][j] == 1 and j <= n - i + 1:
                print("- ", end="")
            else:
                print("  ", end="")
        print()
    print("----------------------------------")


if __name__ == "__main__":
    n = 4  # 设置第一行符号个数
    # n = 7  # 你也可以用 7 测试
    print("不同的符号三角形分别为：")
    total_sum = compute(n)
    print(f"首行 {n} 个符号且符合题目要求的一共有 {total_sum} 种不同的符号三角形")
