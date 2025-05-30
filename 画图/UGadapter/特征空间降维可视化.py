import numpy as np
import matplotlib.pyplot as plt
import torch
from sklearn.manifold import TSNE
import seaborn as sns


# 假设已有数据
# text_means: 原始均值 (n, 1024)
# text_variances: 原始标准差 (n, 1024)
# text_means_optim: 优化后均值 (n, 1024)
# text_variances_optim: 优化后标准差 (n, 1024)

def visualize_feature_distribution(text_means, text_variances, text_means_optim, text_variances_optim, n_samples=10):
    """可视化原始和优化后的特征分布"""
    plt.figure(figsize=(20, 10))

    # 使用t-SNE降维
    combined_means = torch.cat([text_means, text_means_optim], dim=0).detach().cpu().numpy()
    tsne = TSNE(n_components=2, random_state=42, perplexity=5)
    embedded_means = tsne.fit_transform(combined_means)

    # 分割原始和优化后的结果
    orig_means_2d = embedded_means[:n]
    optim_means_2d = embedded_means[n:]

    # 绘制原始分布
    ax1 = plt.subplot(1, 2, 1)
    colors = sns.color_palette("hls", n)

    for i in range(n):
        plt.scatter(orig_means_2d[i, 0], orig_means_2d[i, 1], color=colors[i], s=100, label=f'类别 {i + 1}')
        # 绘制方差椭圆
        variance_mean = text_variances[i].mean().item()
        plt.gca().add_patch(plt.Circle((orig_means_2d[i, 0], orig_means_2d[i, 1]),
                                       variance_mean * 0.5,
                                       color=colors[i], fill=False, alpha=0.5))

    plt.title('原始特征分布', fontsize=15)
    plt.xlabel('t-SNE维度1', fontsize=12)
    plt.ylabel('t-SNE维度2', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # 绘制优化后分布
    ax2 = plt.subplot(1, 2, 2)

    for i in range(n):
        plt.scatter(optim_means_2d[i, 0], optim_means_2d[i, 1], color=colors[i], s=100, label=f'类别 {i + 1}')
        # 绘制方差椭圆
        variance_mean = text_variances_optim[i].mean().item()
        plt.gca().add_patch(plt.Circle((optim_means_2d[i, 0], optim_means_2d[i, 1]),
                                       variance_mean * 0.5,
                                       color=colors[i], fill=False, alpha=0.5))

    plt.title('UGAdapter优化后特征分布', fontsize=15)
    plt.xlabel('t-SNE维度1', fontsize=12)
    plt.ylabel('t-SNE维度2', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # 添加图例
    handles, labels = ax2.get_legend_handles_labels()
    plt.figlegend(handles, labels, loc='lower center', ncol=5, bbox_to_anchor=(0.5, 0.0))

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('feature_distribution.png', dpi=300, bbox_inches='tight')
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
    visualize_feature_distribution(text_means, text_variances, text_means_optim, text_variances_optim)