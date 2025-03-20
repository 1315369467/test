import torch
import torch.nn as nn
import torch.optim as optim


# 定义一个简单的线性模型
class SimpleLinearModel(nn.Module):
    def __init__(self):
        super(SimpleLinearModel, self).__init__()
        self.linear = nn.Linear(1, 1)  # 线性层：输入1维，输出1维

    def forward(self, x):
        return self.linear(x)


# 定义损失函数
class CustomLoss(nn.Module):
    def __init__(self, weight=1.0):
        super(CustomLoss, self).__init__()
        self.weight = nn.Parameter(torch.tensor(weight))

    def forward(self, output, target):
        return self.weight * torch.mean((output - target) ** 2)


# 生成一些数据
torch.manual_seed(0)
x = torch.linspace(-1, 1, 100).view(-1, 1)  # 输入数据
y = 3 * x + torch.randn(x.size()) * 0.1  # 真实标签数据

# 初始化模型和可学习参数 b
model = SimpleLinearModel()
b = nn.Parameter(torch.tensor(1.0))  # 可学习参数 b
loss_function = CustomLoss(weight=0.5)
optimizer = optim.SGD(list(model.parameters()) + [b] + list(loss_function.parameters()), lr=0.01)

# 训练模型
num_epochs =10
for epoch in range(num_epochs):
    model.train()

    # 前向传播
    output = model(x) * b
    loss = loss_function(output, y)

    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(loss_function.weight,"and",b)

    if (epoch + 1) % 2 == 0:
        print(
            f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Loss Weight: {loss_function.weight.item():.4f}, b: {b.item():.4f}')

# 打印最终的权重参数
print(f'Final Loss Weight: {loss_function.weight.item():.4f}, Final b: {b.item():.4f}')
