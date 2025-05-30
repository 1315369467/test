import torch

a=torch.load(r"C:\Users\wang\Downloads\vssm_tiny_0230_ckpt_epoch_262.pth")
print(a)

# b=torch.load(r"C:\Users\wang\Downloads\cubfsfeaturesAS1.pt11",map_location=torch.device('cuda:0'))#torch.Size([200, 60, 640])
# print(b)