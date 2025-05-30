import matplotlib.pyplot as plt
import networkx as nx


def dijkstra_with_path(graph, src):
    """
    使用 Dijkstra 算法找到从源顶点到所有其他顶点的最短路径，并跟踪路径。

    :param graph: 二维列表（邻接矩阵），表示图中各点之间的距离。
    :param src: 源顶点的索引。
    :return: 最短距离列表和路径跟踪列表。
    """
    n = len(graph)
    dist = [float('inf')] * n
    dist[src] = 0
    visited = [False] * n
    # 新增路径跟踪
    parent = [-1] * n

    for _ in range(n):
        u = min_distance(dist, visited)
        visited[u] = True

        for v in range(n):
            if graph[u][v] > 0 and not visited[v] and dist[v] > dist[u] + graph[u][v]:
                dist[v] = dist[u] + graph[u][v]
                parent[v] = u  # 记录到达 v 的最短路径的前一个顶点

    return dist, parent


def min_distance(dist, visited):
    """
    在未访问的顶点中找到具有最小距离的顶点。

    :param dist: 顶点到源点的距离列表。
    :param visited: 访问标记列表。
    :return: 最小距离顶点的索引。
    """
    min_val = float('inf')
    min_index = -1
    for i in range(len(dist)):
        if not visited[i] and dist[i] < min_val:
            min_val = dist[i]
            min_index = i
    return min_index


def print_path(parent, j):
    """
    打印从源顶点到顶点 j 的路径。

    :param parent: 路径跟踪数组。
    :param j: 目标顶点索引。
    :return: None。
    """
    if parent[j] == -1:  # 递归基础情况，源点
        print(j, end='')
        return
    print_path(parent, parent[j])
    print(f" -> {j}", end='')


# 示例图的邻接矩阵
graph = [
    [0, 6, 2, 1, 0],
    [6, 0, 5, 2, 2],
    [2, 5, 0, 3, 5],
    [1, 2, 3, 0, 1],
    [0, 2, 5, 1, 0]
]

# 计算从源点 0 的最短路径和路径跟踪
source_vertex = 1
distances, parents = dijkstra_with_path(graph, source_vertex)

# 打印从源点到所有点的路径
print("Vertex Distance from Source Path")
for i in range(len(distances)):
    print(f"{i} \t {distances[i]} \t", end='')
    print_path(parents, i)
    print()


def visualize_graph_with_shortest_path(graph, source, target):
    """
    使用 networkx 和 matplotlib 可视化图，并高亮显示从源到目标的最短路径。

    :param graph: 二维列表，代表图的邻接矩阵。
    :param source: 源节点索引。
    :param target: 目标节点索引。
    """
    G = nx.DiGraph()  # 创建一个有向图
    n = len(graph)  # 图中的节点数

    # 添加节点
    G.add_nodes_from(range(n))

    # 添加边
    for i in range(n):
        for j in range(n):
            if graph[i][j] != 0:
                G.add_edge(i, j, weight=graph[i][j])

    pos = nx.spring_layout(G)  # 节点位置
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # 计算最短路径并高亮显示
    path = nx.shortest_path(G, source=source, target=target, weight='weight')
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title(f'Shortest path from {source} to {target}')
    plt.show()

    # 输出最短路径和长度
    path_length = nx.shortest_path_length(G, source=source, target=target, weight='weight')
    print("Shortest path:", path)
    print("Path length:", path_length)


# 示例图的邻接矩阵
graph = [
    [0, 6, 0, 1, 0],
    [6, 0, 5, 2, 2],
    [0, 5, 0, 0, 5],
    [1, 2, 0, 0, 1],
    [0, 2, 5, 1, 0]
]

visualize_graph_with_shortest_path(graph, 0, 2)  # 从节点0到节点2的最短路径
