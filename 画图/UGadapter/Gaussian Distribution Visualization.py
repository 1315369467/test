import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from matplotlib.patches import Ellipse
import matplotlib.colors as mcolors


def plot_gaussian_distributions(means, variances,
                                confidence_intervals=[1, 2],
                                scale_factor=3000,
                                figsize=(5, 5)):
    """
    绘制纯净的高斯分布可视化图
    """
    # 转换为numpy数组
    means_np = means.cpu().numpy()
    variances_np = variances.cpu().numpy()

    # 使用t-SNE降维
    tsne = TSNE(n_components=2, random_state=42, perplexity=3)
    means_2d = tsne.fit_transform(means_np)
    # 计算不确定性
    uncertainties = np.mean(variances_np, axis=1)

    # 创建纯净的图形
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()

    # 移除所有坐标轴和标记
    # ax.set_axis_off()

    # 定义颜色
    colors = list(mcolors.TABLEAU_COLORS.values())

    # 绘制高斯分布
    for idx, (mean_2d, uncertainty) in enumerate(zip(means_2d, uncertainties)):
        color = colors[idx % len(colors)]

        # 绘制更小的中心点
        ax.scatter(mean_2d[0], mean_2d[1], c=[color], s=50)

        # 计算椭圆大小
        width = uncertainty * scale_factor
        height = uncertainty * scale_factor

        # 添加置信椭圆
        for i, sigma in enumerate(sorted(confidence_intervals, reverse=True)):
            alpha = 0.1 + (i * 0.2)
            ellipse = Ellipse(
                xy=mean_2d,
                width=width / sigma,
                height=height / sigma,
                angle=0,
                alpha=alpha,
                facecolor=color
            )
            ax.add_patch(ellipse)

    # 保持圆形比例
    ax.set_aspect('equal')
    # 手动设置X轴和Y轴范围
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)


    plt.show()

    return fig


if __name__ == "__main__":
    # 读取数据
    # dataset = "dtd"
    dataset = "eurosat"
    text_means = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/text_means_cupl_t.pt').t()
    text_variances = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/text_variances_cupl_t.pt').t()
    # text_means = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/graph_text_features_gs_best_16shots.pt').detach().t()
    # text_variances = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/graph_text_variances_gs_best_16shots.pt').detach().t()

    n = 10
    text_means = text_means[:n] #(n,1024)
    text_variances = torch.sqrt(text_variances[:n])

    # 创建可视化
    fig = plot_gaussian_distributions(
        text_means,
        text_variances,
        confidence_intervals=[1, 2],
        scale_factor=3000,
        figsize=(5, 5)
    )

    # 保存无边界的图像
    plt.savefig('gaussian_distributions.png',
                dpi=300,
                bbox_inches='tight',
                pad_inches=0,
                transparent=True)  # 使用透明背景