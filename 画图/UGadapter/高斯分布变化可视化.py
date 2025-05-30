import numpy as np
import matplotlib.pyplot as plt
import torch
import seaborn as sns
from matplotlib.patches import Ellipse

plt.rcParams['font.sans-serif'] = ['SimHei']


def visualize_gaussian_changes(text_means, text_variances, text_means_optim, text_variances_optim, n_classes=10,
                               feature_dims=[0, 1]):
    """可视化选定维度特征的高斯分布变化"""
    plt.figure(figsize=(15, 12))
    colors = sns.color_palette("hls", n_classes)

    # 选择两个特征维度进行可视化
    dim1, dim2 = feature_dims

    # 创建网格进行分布可视化
    for i in range(n_classes):
        ax = plt.subplot(3, 4, i + 1)

        # 提取原始和优化后的均值和方差
        mu_orig = text_means[i, [dim1, dim2]].detach().cpu().numpy()
        sigma_orig = text_variances[i, [dim1, dim2]].detach().cpu().numpy()

        mu_optim = text_means_optim[i, [dim1, dim2]].detach().cpu().numpy()
        sigma_optim = text_variances_optim[i, [dim1, dim2]].detach().cpu().numpy()

        # 绘制原始分布
        plt.scatter(mu_orig[0], mu_orig[1], color=colors[i], s=100, marker='o', label='原始均值')
        ellipse_orig = Ellipse(mu_orig, sigma_orig[0] * 2, sigma_orig[1] * 2,
                               edgecolor=colors[i], facecolor='none', alpha=0.7,
                               linestyle='--', linewidth=2, label='原始方差')
        ax.add_patch(ellipse_orig)

        # 绘制优化后分布
        plt.scatter(mu_optim[0], mu_optim[1], color=colors[i], s=100, marker='*', label='优化后均值')
        ellipse_optim = Ellipse(mu_optim, sigma_optim[0] * 2, sigma_optim[1] * 2,
                                edgecolor=colors[i], facecolor='none', alpha=0.7,
                                linestyle='-', linewidth=2, label='优化后方差')
        ax.add_patch(ellipse_optim)

        # 绘制连接线
        plt.plot([mu_orig[0], mu_optim[0]], [mu_orig[1], mu_optim[1]],
                 color=colors[i], linestyle=':', alpha=0.8)

        plt.title(f'类别 {i + 1}', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)

        # 仅在第一个子图中添加图例
        if i == 0:
            plt.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig('gaussian_changes.png', dpi=300, bbox_inches='tight')
    plt.show()


# 计算方差变化幅度
def visualize_variance_changes(text_variances, text_variances_optim, n_classes=10):
    """可视化各类别的方差变化幅度"""
    plt.figure(figsize=(12, 6))

    # 计算每个类别的平均方差
    mean_var_orig = torch.mean(text_variances, dim=1).detach().cpu().numpy()
    mean_var_optim = torch.mean(text_variances_optim, dim=1).detach().cpu().numpy()

    # 计算变化率
    change_ratio = (mean_var_optim - mean_var_orig) / mean_var_orig * 100

    # 绘制柱状图
    bar_width = 0.35
    x = np.arange(n_classes)

    plt.bar(x - bar_width / 2, mean_var_orig, bar_width, label='原始方差', color='skyblue')
    plt.bar(x + bar_width / 2, mean_var_optim, bar_width, label='优化后方差', color='orange')

    # 添加变化率标签
    for i, ratio in enumerate(change_ratio):
        color = 'green' if ratio >= 0 else 'red'
        plt.annotate(f'{ratio:.1f}%',
                     xy=(i, max(mean_var_orig[i], mean_var_optim[i]) + 0.02),
                     ha='center', va='bottom', color=color, fontweight='bold')

    plt.xlabel('类别', fontsize=12)
    plt.ylabel('平均方差', fontsize=12)
    plt.title('UGAdapter前后类别方差变化', fontsize=15)
    plt.xticks(x, [f'类别{i + 1}' for i in range(n_classes)])
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('variance_changes.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    # 读取数据
    dataset = "dtd"

    text_means = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/text_means_cupl_t.pt').t()
    text_variances = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/text_variances_cupl_t.pt').t()
    text_means_optim = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/graph_text_features_gs_best_16shots.pt').detach().t()
    text_variances_optim = torch.load(f'C:/Users/wang/Desktop/Tip-Adapter-main/caches/{dataset}/graph_text_variances_gs_best_16shots.pt').detach()

    # 选择前 n 个类别
    a = 0
    n = 10
    text_means = text_means[a:a+n]  # (n, 1024)
    text_variances = torch.sqrt(text_variances[a:a+n]) # (n, 1024)
    text_means_optim = text_means_optim[a:a+n]  # (n, 1024)
    text_variances_optim = torch.sqrt(text_variances_optim[a:a+n]) # (n, 1024)

    # 调用函数
    visualize_gaussian_changes(text_means, text_variances, text_means_optim, text_variances_optim)
    visualize_variance_changes(text_variances, text_variances_optim)