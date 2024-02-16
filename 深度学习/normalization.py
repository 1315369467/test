import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
# 检查是否有可用的 CUDA 设备
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# 创建一个包含 Batch Normalization 的神经网络
class ModelWithBatchNorm(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ModelWithBatchNorm, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)  # 在第一个隐藏层后应用 Batch Normalization
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        return x

# 创建一个包含 Layer Normalization 的神经网络
class ModelWithLayerNorm(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ModelWithLayerNorm, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.ln1 = nn.LayerNorm(hidden_size)  # 在第一个隐藏层后应用 Layer Normalization
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.ln1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        return x


# 定义一个列表来保存每个epoch的损失
train_losses_batch_norm = []
train_losses_layer_norm = []


# 修改训练函数以收集损失
def train(model, train_loader, num_epochs, learning_rate, train_losses):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    model.to(device)  # 将模型移动到 CUDA 设备

    for epoch in range(num_epochs):
        running_loss = 0.0  # 用于累积每个epoch的损失
        for i, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)  # 将数据移动到 CUDA 设备
            optimizer.zero_grad()
            inputs = inputs.view(inputs.size(0), -1)  # 将输入的维度展平
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            if (i + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{len(train_loader)}], Loss: {loss.item():.4f}')

        # 计算并保存每个epoch的平均损失
        epoch_loss = running_loss / len(train_loader)
        train_losses.append(epoch_loss)


# 创建一个虚拟数据集和数据加载器
input_size = 28 * 28
hidden_size = 128
output_size = 10
num_epochs = 10
learning_rate = 0.001
batch_size = 64

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
train_dataset = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)


model_with_batch_norm = ModelWithBatchNorm(input_size, hidden_size, output_size)
model_with_layer_norm = ModelWithLayerNorm(input_size, hidden_size, output_size)

# 训练包含 Batch Normalization 的模型
print("Training Model with Batch Normalization:")
train(model_with_batch_norm, train_loader, num_epochs, learning_rate, train_losses_batch_norm)

# 训练包含 Layer Normalization 的模型
print("Training Model with Layer Normalization:")
train(model_with_layer_norm, train_loader, num_epochs, learning_rate, train_losses_layer_norm)

# 绘制损失曲线
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
plt.figure(figsize=(10, 5))
plt.plot(train_losses_batch_norm, label='Batch Normalization')
plt.plot(train_losses_layer_norm, label='Layer Normalization')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Training Loss')
plt.show()


# 在测试数据集上评估模型性能
def test(model, test_loader):
    model.eval()  # 将模型切换到评估模式
    correct = 0
    total = 0

    with torch.no_grad():  # 在评估模式下不需要计算梯度
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)  # 将数据移动到 CUDA 设备
            inputs = inputs.view(inputs.size(0), -1)  # 将输入的维度展平
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy on test data: {100 * correct / total:.2f}%')

# 创建一个虚拟测试数据集和数据加载器
test_dataset = torchvision.datasets.MNIST(root='./data', train=False, transform=transform, download=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 测试包含 Batch Normalization 的模型
print("Testing Model with Batch Normalization:")
test(model_with_batch_norm, test_loader)

# 测试包含 Layer Normalization 的模型
print("Testing Model with Layer Normalization:")
test(model_with_layer_norm, test_loader)

# Testing Model with Batch Normalization:
# Accuracy on test data: 97.63%
# Testing Model with Layer Normalization:
# Accuracy on test data: 97.57%