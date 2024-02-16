import torch
print(torch.cuda.is_available())  #返回True则说明已经安装了cuda
print("torch.__version__  = ", torch.__version__)
print(torch.version.cuda)
print(torch.backends.cudnn.version())
from torch.backends import cudnn
print(cudnn.is_available())  #返回True说明已经安装了cuDNN

# True
# torch.__version__  =  1.7.1+cu110
# 11.0
# 8004
# True

# C:\ProgramData\Anaconda3\envs\torch2\python.exe C:/Users/wang/Desktop/test/coda0.py
# True
# torch.__version__  =  2.0.1+cu117
# 11.7
# 8500
# True