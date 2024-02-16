class Graph:
    def __init__(self, vertices):
        self.V = vertices  # 初始化图的顶点数
        self.graph = []    # 初始化边的列表

    def add_edge(self, u, v, w):
        """
        添加一条边到图中
        u: 边的起点
        v: 边的终点
        w: 边的权重
        """
        self.graph.append([u, v, w])

    def find_parent(self, parent, i):
        """
        找到节点i的根节点
        parent: 父节点数组
        i: 节点
        """
        if parent[i] == i:  # 如果节点i是根节点
            return i
        return self.find_parent(parent, parent[i])  # 递归查找根节点

    def union(self, parent, rank, x, y):
        """
        将两个集合合并
        parent: 父节点数组
        rank: 秩数组
        x: 集合x的根节点
        y: 集合y的根节点
        """
        x_root = self.find_parent(parent, x)
        y_root = self.find_parent(parent, y)

        if rank[x_root] < rank[y_root]:  # 如果x的秩小于y的秩
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:  # 如果x的秩大于y的秩
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    def kruskal(self):
        result = []  # 存储最小生成树的边
        i, e = 0, 0  # i用于迭代图的边，e用于记录已经加入生成树的边数

        # 对边按照权重升序排序
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []  # 存储顶点的父节点
        rank = []    # 存储顶点的秩

        for node in range(self.V):
            parent.append(node)  # 初始化每个顶点的父节点为自己
            rank.append(0)      # 初始化每个顶点的秩为0

        while e < self.V - 1:  # 当生成树中的边数小于顶点数减一时
            u, v, w = self.graph[i]
            i += 1
            x = self.find_parent(parent, u)
            y = self.find_parent(parent, v)

            if x != y:  # 如果边的两个顶点不在同一集合中
                e += 1
                result.append([u, v, w])  # 将边添加到生成树中
                self.union(parent, rank, x, y)  # 合并两个集合

        print("修建道路方案:")
        for u, v, w in result:
            print(f"从{u}到{v}的距离为{w}单位距离")

# 创建一个包含6个顶点的图
g = Graph(6)

# 添加各楼栋之间的距离
g.add_edge(0, 1, 2)
g.add_edge(0, 2, 4)
g.add_edge(1, 2, 1)
g.add_edge(1, 3, 7)
g.add_edge(2, 4, 3)
g.add_edge(3, 4, 2)
g.add_edge(3, 5, 5)
g.add_edge(4, 5, 6)

# 使用克鲁斯卡尔算法找到最短路径方案
g.kruskal()
