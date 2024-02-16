import torch
import torch.nn as nn
import torch.optim as optim
import time
# 构建训练集
A = torch.rand(100000, 2, 5).cuda()
cos_angle = (A[:, 0, :] * A[:, 1, :]).sum(dim=1) / torch.sqrt((A[:, 0, :] * A[:, 0, :]).sum(dim=1)
                                                              * (A[:, 1, :] * A[:, 1, :]).sum(dim=1))
ground_truth = torch.acos(cos_angle).view(-1, 1)

# 构建测试集
B = torch.rand(2000, 2, 5).cuda()
cos_angle_B = (B[:, 0, :] * B[:, 1, :]).sum(dim=1) / torch.sqrt((B[:, 0, :] * B[:, 0, :]).sum(dim=1)
                                                                * (B[:, 1, :] * B[:, 1, :]).sum(dim=1))
ground_truth_B = torch.acos(cos_angle_B).view(-1, 1)


# 建立网络
class angleNet(nn.Module):

    def __init__(self):
        super(angleNet, self).__init__()
        self.dense = nn.Sequential(nn.Linear(10, 80),
                                   nn.ReLU(),
                                   nn.Linear(80, 40),
                                   nn.ReLU(),
                                   nn.Linear(40, 80),
                                   nn.ReLU(),
                                   nn.Linear(80, 1))

    def forward(self, x):
        x = x.view(-1, 10)
        x = self.dense(x)
        return x


model = angleNet().cuda()

cost = nn.MSELoss()
optimizer = optim.AdamW(model.parameters())
a=time.time()
# 训练个5000轮
epochs = 100
for epoch in range(epochs):
    optimizer.zero_grad()
    output = model(A)
    loss = cost(output, ground_truth)
    loss.backward()
    optimizer.step()

    print(epoch, loss)

# 测试一下
with torch.no_grad():
    pred = model(B)
    err = cost(pred, ground_truth_B)
    print("err", err)
b=time.time()
print(b-a)

##100
#0.9197409152984619 #2.0505971908569336 #5.801401615142822
##1000
#5.543457984924316 #16.22306537628174 #58.15271711349487
##10000
#50.75450301170349  #
