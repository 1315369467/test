
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# 定义转换
transform = transforms.Compose([
    # transforms.RandomHorizontalFlip(p=0.5),  # 50%的概率水平翻转
    # transforms.RandomRotation(degrees=(-15, 15)),  # 随机旋转角度范围
    transforms.RandomResizedCrop(84, scale=(0.2, 1.0)),  # 随机裁剪和缩放到指定大小
    # transforms.ColorJitter(brightness=0, contrast=0, saturation=0, hue=0),  # 随机颜色调整
    # transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1), shear=0.1),  # 仿射变换
    # transforms.RandomPerspective(distortion_scale=0.5, p=0.5, interpolation=3),  # 透视变换
])

# 加载图像 (这里以一个示例图像为例)
image_path = r"D:\Data\tiered_imagenet\test\n02105412\n0210541200000658.jpg"
image = Image.open(image_path)

# 应用转换
plt.figure(figsize=(6, 6))
for i in range(15):
    transformed_image = transform(image)

    plt.subplot(4, 4, i+2)
    plt.imshow(transformed_image)


plt.subplot(4, 4, 1)
plt.imshow(image)
plt.show()