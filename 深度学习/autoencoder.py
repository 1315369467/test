import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.autograd import Variable

# 定义自编码器模型
class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 128),  # 输入图像大小为28x28，将其压缩到128维
            nn.ReLU(True)
        )
        self.decoder = nn.Sequential(
            nn.Linear(128, 28 * 28),  # 将编码后的数据解压回原始大小
            nn.Sigmoid()  # 使用Sigmoid函数进行解压
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

# 加载MNIST数据集
transform = transforms.Compose([transforms.ToTensor()])  # 转换图像为张量
train_dataset = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)

# 初始化自编码器模型和优化器
autoencoder = Autoencoder()
optimizer = optim.Adam(autoencoder.parameters(), lr=0.001)
criterion = nn.BCELoss()  # 二元交叉熵损失用于像素级别的重构

# 训练自编码器
num_epochs = 1
for epoch in range(num_epochs):
    for data in train_loader:
        img, _ = data
        img = img.view(img.size(0), -1)  # 展平图像
        img = Variable(img)
        output = autoencoder(img)
        loss = criterion(output, img)  # 计算重构误差
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))

# 使用自编码器进行图像重构
import matplotlib.pyplot as plt
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# 随机选择一个图像
test_image = train_dataset[0][0].view(1, -1)
reconstructed_image = autoencoder(test_image)
reconstructed_image = reconstructed_image.view(28, 28).data.numpy()

# 可视化原始图像和重构图像
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.imshow(test_image.view(28, 28).numpy(), cmap='gray')
plt.title('Original Image')
plt.subplot(1, 2, 2)
plt.imshow(reconstructed_image, cmap='gray')
plt.title('Reconstructed Image')
plt.show()
