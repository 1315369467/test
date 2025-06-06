import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from matplotlib.patches import Ellipse
import matplotlib.colors as mcolors


def plot_gaussian_distributions(ax, means, variances,
                                confidence_intervals=[1, 2],
                                scale_factor=3000,
                                title=""):
    """
    绘制高斯分布可视化图到指定子图
    """
    # 转换为numpy数组
    means_np = means.cpu().numpy()
    variances_np = variances.cpu().numpy()

    # 使用t-SNE降维
    tsne = TSNE(n_components=2, random_state=42, perplexity=6, learning_rate=90)
    means_2d = tsne.fit_transform(means_np)

    # 计算不确定性
    uncertainties = np.mean(variances_np, axis=1)

    # 定义颜色
    colors = list(mcolors.TABLEAU_COLORS.values())

    # 绘制高斯分布
    for idx, (mean_2d, uncertainty) in enumerate(zip(means_2d, uncertainties)):
        color = colors[idx % len(colors)]

        # 绘制更小的中心点
        ax.scatter(mean_2d[0], mean_2d[1], c=[color], s=20)

        # 计算椭圆大小
        width = uncertainty * scale_factor
        height = uncertainty * scale_factor

        # 添加置信椭圆
        for i, sigma in enumerate(sorted(confidence_intervals, reverse=True)):
            alpha = 0.2 + (i * 0.1)
            ellipse = Ellipse(
                xy=mean_2d,
                width=width / sigma,
                height=height / sigma,
                angle=0,
                alpha=alpha,
                facecolor=color
            )
            ax.add_patch(ellipse)

    # 设置标题和比例
    m = 200
    ax.set_aspect('equal')
    ax.set_xlim(-m, m)
    ax.set_ylim(-m, m)
    ax.set_title(title)


if __name__ == "__main__":
    # 读取数据
    dataset = "eurosat"
    text_means = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/text_means_cupl_t.pt').t()
    text_variances = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/text_variances_cupl_t.pt').t()
    text_means_optim = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/graph_text_features_gs_best_16shots.pt').detach().t()
    text_variances_optim = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/graph_text_variances_gs_best_16shots.pt').detach()

    # 选择前 n 个类别
    a = 0
    n = 10
    text_means = text_means[a:a+n]  # (n, 1024)
    text_variances = torch.sqrt(text_variances[a:a+n])
    text_means_optim = text_means_optim[a:a+n]  # (n, 1024)
    text_variances_optim = torch.sqrt(text_variances_optim[a:a+n])

    # 创建对比图
    scale_factor = 4500
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))  # 创建两个子图并排
    plot_gaussian_distributions(
        axes[0], text_means, text_variances,
        confidence_intervals=[1.1, 2],
        scale_factor=scale_factor,
        title="original distribution"
    )
    plot_gaussian_distributions(
        axes[1], text_means_optim, text_variances_optim,
        confidence_intervals=[1.1, 2],
        scale_factor=scale_factor,
        title="optimized distribution"
    )

    # 保存对比图
    plt.savefig('gaussian_distributions_comparison.png',
                dpi=300,
                bbox_inches='tight',
                pad_inches=0.1,
                transparent=True)  # 使用透明背景
    plt.show()
