import numpy as np

def lcs_with_path_numpy(X, Y):
    m = len(X)
    n = len(Y)
    # 使用numpy数组初始化c和b数组
    c = np.zeros((m + 1, n + 1), dtype=int)
    b = np.zeros((m + 1, n + 1), dtype=str)

    # 填充c和b数组
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = '1'  # 从左上方来
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = '2'  # 从上方来
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = '3'  # 从左方来

    # 从b数组回溯找到LCS
    i, j = m, n
    lcs = []
    while i > 0 and j > 0:
        if b[i][j] == '1':
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif b[i][j] == '2':
            i -= 1
        else:
            j -= 1
    lcs.reverse()

    return ''.join(lcs), c, b

# 输入序列
X = "abcacbab"
Y = "bacbacb"
lcs_result_numpy, c_matrix_numpy, b_matrix_numpy = lcs_with_path_numpy(X, Y)

# 输出结果
print(lcs_result_numpy, c_matrix_numpy, b_matrix_numpy)
