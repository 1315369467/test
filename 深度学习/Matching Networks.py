import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 创建一个示例数据集
# 这里我们使用了一个简单的示例数据集，你可以替换为你自己的数据。
# 在实际情况下，你需要加载和预处理你的数据。

# 支持集（Support Set）：每个类别有5个样本，每个样本有2个特征
support_set = torch.randn((5, 2))
# 查询集（Query Set）：需要分类的样本，每个样本有2个特征
query_set = torch.randn((15, 2))


# 定义关系网络
class RelationNetwork(nn.Module):
    def __init__(self):
        super(RelationNetwork, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(2, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, support_set, query_set):
        # 编码支持集和查询集样本
        support_encoded = self.encoder(support_set)
        query_encoded = self.encoder(query_set)

        # 计算两两样本之间的关系得分
        support_encoded = support_encoded.unsqueeze(0).repeat(query_encoded.size(0), 1, 1)
        query_encoded = query_encoded.unsqueeze(1).repeat(1, support_encoded.size(1), 1)
        relation_pairs = torch.cat((support_encoded, query_encoded), dim=2)
        relations = self.fc(relation_pairs).sum(dim=2)

        # 进行分类
        predictions = torch.sigmoid(relations)

        return predictions


# 初始化关系网络
relation_net = RelationNetwork()

# 定义损失函数和优化器
criterion = nn.BCELoss()  # 二分类交叉熵损失
optimizer = optim.Adam(relation_net.parameters(), lr=0.001)

# 训练模型
num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    predictions = relation_net(support_set, query_set)

    # 在这个示例中，我们使用随机生成的标签作为示例标签
    # 在实际应用中，你需要使用真实标签
    labels = torch.randint(0, 15, (15,5), dtype=torch.float32)

    loss = criterion(predictions, labels)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')

# 验证模型
# 在实际应用中，你需要准备一个验证集来评估模型性能。
# 这里只是一个简单的示例，用于说明模型的训练和测试过程。
