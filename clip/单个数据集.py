import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = 'car.csv'
try:
    data = pd.read_csv(file_path, encoding='utf-8')  # 如果文件是UTF-8编码
except UnicodeDecodeError:
    data = pd.read_csv(file_path, encoding='latin1')  # 尝试Latin-1编码
# 转换列名为数字，方便绘图
data.columns = ["method", "1-shot", "2-shot", "4-shot", "8-shot", "16-shot"]

# 提取数据
x_ticks = [1, 2, 4, 8, 16]  # 横轴为1, 2, 4, 8, 16
x = ["1-shot", "2-shot", "4-shot", "8-shot", "16-shot"]
methods = data["method"]
scores = data[x]
# 绘图
plt.figure(figsize=(6, 6))
for idx, method in enumerate(methods):
    plt.plot(
        x_ticks,  # 横轴为实际值
        scores.iloc[idx],  # 每个方法的y值
        label=method,
        marker="o"
    )

# 添加标题、坐标轴标签、图例和网格
plt.title("StanfordCars")
plt.xlabel("Number of training samples per class")
plt.ylabel("Score(%)")
plt.xticks(x_ticks)  # 设置横轴刻度为1, 2, 4, 8, 16
plt.legend()
plt.grid(True)

# 显示图像
plt.show()