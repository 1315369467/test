import numpy as np
import matplotlib.pyplot as plt
import torch
import seaborn as sns
import matplotlib as mpl

mpl.rcParams['font.family'] = 'SimHei'
mpl.rcParams['axes.unicode_minus'] = False

def visualize_variance_distribution(text_variances, text_variances_optim, n_classes=10):
    """可视化类别方差在特征维度上的分布"""
    plt.figure(figsize=(18, 12))

    # 为方便可视化，选择前100维特征
    feature_dims = 20

    for i in range(n_classes):
        ax = plt.subplot(3, 4, i + 1)

        # 获取原始和优化后的方差
        var_orig = text_variances[i, :feature_dims].detach().cpu().numpy()
        var_optim = text_variances_optim[i, :feature_dims].detach().cpu().numpy()

        # 绘制方差分布
        x = np.arange(feature_dims)
        plt.bar(x - 0.2, var_orig, 0.4, label='原始方差', alpha=0.7, color='skyblue')
        plt.bar(x + 0.2, var_optim, 0.4, label='优化后方差', alpha=0.7, color='salmon')

        plt.title(f'类别 {i + 1} 特征方差分布', fontsize=12)
        plt.xlabel('特征维度', fontsize=10)
        plt.ylabel('方差大小', fontsize=10)

        # 仅在第一个子图显示图例
        if i == 0:
            plt.legend(fontsize=10)

        plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('variance_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 方差总体变化可视化
    plt.figure(figsize=(12, 6))

    # 计算每个类别在各维度上的方差变化比例
    change_ratio = ((text_variances_optim - text_variances) / text_variances).detach().cpu().numpy()

    # 计算每个类别的平均变化率
    mean_change = np.mean(change_ratio, axis=1)
    median_change = np.median(change_ratio, axis=1)

    # 绘制箱线图显示每个类别的方差变化分布
    plt.subplot(1, 2, 1)
    plt.boxplot([change_ratio[i, :] for i in range(n_classes)],
                labels=[f"{i + 1}" for i in range(n_classes)])
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('各类别方差变化比例分布', fontsize=14)
    plt.xlabel('类别', fontsize=12)
    plt.ylabel('变化比例', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # 绘制平均变化率
    plt.subplot(1, 2, 2)
    x = np.arange(n_classes)
    plt.bar(x, mean_change, 0.4, label='平均变化率', color='skyblue')
    plt.plot(x, median_change, 'ro-', label='中位数变化率')

    plt.axhline(y=0, color='k', linestyle='--')
    plt.title('各类别方差平均变化率', fontsize=14)
    plt.xlabel('类别', fontsize=12)
    plt.ylabel('变化率', fontsize=12)
    plt.xticks(x, [f"{i + 1}" for i in range(n_classes)])
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('variance_change_ratio.png', dpi=300)
    plt.show()

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
    text_variances = torch.sqrt(text_variances[a:a+n]) # (n, 1024)
    text_means_optim = text_means_optim[a:a+n]  # (n, 1024)
    text_variances_optim = torch.sqrt(text_variances_optim[a:a+n]) # (n, 1024)

    # 调用函数
    visualize_variance_distribution(text_variances, text_variances_optim)