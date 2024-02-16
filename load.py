import torch

a=torch.load(r"C:\Users\wang\Downloads\mini1.pt1")
print(a)

b=torch.load(r"C:\Users\wang\Downloads\cubfsfeaturesAS1.pt11",map_location=torch.device('cuda:0'))#torch.Size([200, 60, 640])
print(b)