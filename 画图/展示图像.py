import os
import random
import matplotlib.pyplot as plt
from PIL import Image

def crop_to_square(image):
    width, height = image.size
    new_size = min(width, height)
    left = (width - new_size)/2
    top = (height - new_size)/2
    right = (width + new_size)/2
    bottom = (height + new_size)/2
    return image.crop((left, top, right, bottom))

def display_random_images(folder_path, num_images=100):
    if not os.path.exists(folder_path):
        print("指定的文件夹不存在")
        return

    files = os.listdir(folder_path)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if not image_files:
        print("文件夹中没有图像文件")
        return

    selected_images = random.sample(image_files, min(num_images, len(image_files)))

    plt.figure(figsize=(10, 10))  # 可以根据需要调整大小

    for i, image in enumerate(selected_images):
        img_path = os.path.join(folder_path, image)
        img = Image.open(img_path)
        img = crop_to_square(img)

        plt.subplot(10, 10, i + 1)  # 5行4列布局
        plt.imshow(img)
        plt.axis('off')
        plt.subplots_adjust(wspace=0, hspace=0)  # 设置子图之间的间隔为0

    plt.show()

# 使用示例
folder_path = r"D:\Data\mini-imagenet\images"  # 替换为您的文件夹路径
display_random_images(folder_path)
