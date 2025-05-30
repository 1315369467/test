import numpy as np
import matplotlib.pyplot as plt
import torch
import networkx as nx
from sklearn.manifold import TSNE
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']


def visualize_category_graph(text_means, text_means_optim, n_classes=10, threshold=0.3):
    """可视化类别间的关系图结构"""
    plt.figure(figsize=(20, 10))

    # 计算类别间的余弦相似度
    def compute_similarity(means):
        norm = torch.norm(means, dim=1, keepdim=True)
        normalized_means = means / norm
        similarity = torch.mm(normalized_means, normalized_means.t())
        return similarity

    # 计算原始和优化后的相似度矩阵
    similarity_orig = compute_similarity(text_means).detach().cpu().numpy()
    similarity_optim = compute_similarity(text_means_optim).detach().cpu().numpy()

    # 使用t-SNE降维获取节点位置
    embedded_means_orig = TSNE(n_components=2, random_state=42, perplexity=5).fit_transform(text_means.detach().cpu().numpy())
    embedded_means_optim = TSNE(n_components=2, random_state=42, perplexity=5).fit_transform(text_means_optim.detach().cpu().numpy())

    # 创建图结构
    def create_graph(similarity, positions, ax, title):
        G = nx.Graph()

        # 添加节点
        for i in range(n_classes):
            G.add_node(i, pos=positions[i])

        # 添加边 (仅添加相似度高于阈值的边)
        for i in range(n_classes):
            for j in range(i + 1, n_classes):
                if similarity[i, j] > threshold:
                    G.add_edge(i, j, weight=similarity[i, j])

        # 获取节点位置
        pos = nx.get_node_attributes(G, 'pos')

        # 绘制节点
        colors = sns.color_palette("hls", n_classes)
        nx.draw_networkx_nodes(G, pos,
                               node_size=[500 + 1000 * torch.mean(text_variances[i]).item() for i in range(n_classes)],
                               node_color=colors,
                               alpha=0.8,
                               ax=ax)

        # 绘制边 (边的粗细表示相似度)
        edges = G.edges(data=True)
        weights = [data['weight'] * 5 for _, _, data in edges]
        nx.draw_networkx_edges(G, pos,
                               edgelist=edges,
                               width=weights,
                               alpha=0.6,
                               edge_color='gray',
                               ax=ax)

        # 添加标签
        labels = {i: f"{i + 1}" for i in range(n_classes)}
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', ax=ax)

        # 设置标题和边界
        ax.set_title(title, fontsize=15)
        ax.set_xlim([min(pos[i][0] for i in range(n_classes)) * 1.2,
                     max(pos[i][0] for i in range(n_classes)) * 1.2])
        ax.set_ylim([min(pos[i][1] for i in range(n_classes)) * 1.2,
                     max(pos[i][1] for i in range(n_classes)) * 1.2])
        ax.axis('off')

    # 绘制原始图
    ax1 = plt.subplot(1, 2, 1)
    create_graph(similarity_orig, embedded_means_orig, ax1, '原始类别关系图')

    # 绘制优化后图
    ax2 = plt.subplot(1, 2, 2)
    create_graph(similarity_optim, embedded_means_optim, ax2, 'UGAdapter优化后类别关系图')

    # 添加相似度热力图
    plt.figure(figsize=(18, 8))

    ax3 = plt.subplot(1, 2, 1)
    sns.heatmap(similarity_orig, annot=True, fmt=".2f", cmap="YlGnBu",
                xticklabels=[f"{i + 1}" for i in range(n_classes)],
                yticklabels=[f"{i + 1}" for i in range(n_classes)],
                ax=ax3)
    ax3.set_title('原始类别相似度矩阵', fontsize=15)

    ax4 = plt.subplot(1, 2, 2)
    sns.heatmap(similarity_optim, annot=True, fmt=".2f", cmap="YlGnBu",
                xticklabels=[f"{i + 1}" for i in range(n_classes)],
                yticklabels=[f"{i + 1}" for i in range(n_classes)],
                ax=ax4)
    ax4.set_title('UGAdapter优化后类别相似度矩阵', fontsize=15)

    plt.tight_layout()
    plt.savefig('category_relationships.png', dpi=300, bbox_inches='tight')
    plt.show()


# 计算相似度变化
def visualize_similarity_changes(text_means, text_means_optim, n_classes=10):
    """可视化类别相似度的变化"""

    # 计算类别间的余弦相似度
    def compute_similarity(means):
        norm = torch.norm(means, dim=1, keepdim=True)
        normalized_means = means / norm
        similarity = torch.mm(normalized_means, normalized_means.t())
        return similarity

    # 计算原始和优化后的相似度矩阵
    similarity_orig = compute_similarity(text_means).detach().cpu().numpy()
    similarity_optim = compute_similarity(text_means_optim).detach().cpu().numpy()

    # 计算变化
    similarity_diff = similarity_optim - similarity_orig

    plt.figure(figsize=(10, 8))
    sns.heatmap(similarity_diff, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                xticklabels=[f"{i + 1}" for i in range(n_classes)],
                yticklabels=[f"{i + 1}" for i in range(n_classes)])
    plt.title('类别相似度变化 (UGAdapter优化后 - 原始)', fontsize=15)
    plt.tight_layout()
    plt.savefig('similarity_changes.png', dpi=300)
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
    n = 20
    text_means = text_means[a:a+n]  # (n, 1024)
    text_variances = torch.sqrt(text_variances[a:a+n]) # (n, 1024)
    text_means_optim = text_means_optim[a:a+n]  # (n, 1024)
    text_variances_optim = torch.sqrt(text_variances_optim[a:a+n]) # (n, 1024)

    # 调用函数
    visualize_category_graph(text_means, text_means_optim)
    visualize_similarity_changes(text_means, text_means_optim)