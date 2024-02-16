from PIL import Image
import numpy as np

def embed_text_in_bit_plane(image, text, bit_plane):
    """
    在图像的指定位面嵌入文本。
    """
    # 将文本转换为二进制
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    # 展平图像数组
    flat_image = image.flatten()
    # 在指定位面修改位
    for i, bit in enumerate(binary_text):
        if i >= flat_image.size:
            break
        if bit == '1':
            flat_image[i] |= 1 << bit_plane
        else:
            flat_image[i] &= ~(1 << bit_plane)
    return flat_image.reshape(image.shape)

def extract_text_from_bit_plane(image, bit_plane, length):
    """
    从图像的指定位面提取文本。
    """
    # 展平图像数组
    flat_image = image.flatten()
    # 从指定位面提取位
    bits = [(flat_image[i] >> bit_plane) & 1 for i in range(length * 8)]
    # 将位转换为字符
    chars = [chr(int(''.join(str(bit) for bit in bits[i:i + 8]), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

# 加载图像并将其转换为512x512像素的8位灰度图像
image_path = r"D:\Data\mini-imagenet\images\n0153282900000005.jpg"
original_image = Image.open(image_path)
gray_image = original_image.convert("L").resize((512, 512))
image_array = np.array(gray_image)

# 在指定的位面嵌入文本
image_with_text = embed_text_in_bit_plane(image_array, "123", 0)
image_with_text = embed_text_in_bit_plane(image_with_text, "computer science", 1)

# 将修改后的数组转换回图像并显示
modified_image = Image.fromarray(image_with_text)
modified_image.show()

# 从位面提取文本
extracted_text_0 = extract_text_from_bit_plane(image_with_text, 0, len("123"))
extracted_text_1 = extract_text_from_bit_plane(image_with_text, 1, len("computer science"))

print(extracted_text_0, extracted_text_1)
