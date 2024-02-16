import cv2

# 初始化摄像头
camera = cv2.VideoCapture(0)  # 0代表默认摄像头

# 检查摄像头是否成功初始化
if not camera.isOpened():
    print("无法打开摄像头")
    exit()

# 捕获图像
ret, frame = camera.read()

# 检查图像是否成功捕获
if not ret:
    print("无法捕获图像")
    camera.release()
    exit()

# 保存自拍照片
cv2.imwrite("selfie.jpg", frame)

# 释放摄像头
camera.release()

# 关闭所有OpenCV窗口
cv2.destroyAllWindows()

print("自拍照片已保存为selfie.jpg")
