import cv2
import numpy as np

# 设置YUV文件的路径和图像的分辨率
yuv_file_path = '/Users/evern.zhu/Desktop/workspace/log/4k60_nv16.yuv'
width = 1920  # 图像的宽度
height = 1080  # 图像的高度

# 计算YUV420格式中Y, U, V的帧大小
frame_size = width * height + (width // 2) * (height // 2) * 2

# 打开YUV文件
with open(yuv_file_path, 'rb') as file:
    yuv = file.read(frame_size)  # 读取一帧数据

# 将YUV数据转换为NumPy数组
yuv = np.frombuffer(yuv, dtype=np.uint8)

# 重塑和合并Y, U, V通道
y = yuv[0:width * height].reshape((height, width))
u = yuv[width * height:width * height + (width // 2) * (height // 2)].reshape((height // 2, width // 2))
v = yuv[width * height + (width // 2) * (height // 2):].reshape((height // 2, width // 2))
u = cv2.resize(u, (width, height), interpolation=cv2.INTER_LINEAR)
v = cv2.resize(v, (width, height), interpolation=cv2.INTER_LINEAR)

# YUV到RGB的转换
yuv = cv2.merge((y, u, v))
rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_NV12)

# 保存图像
cv2.imwrite('output_image.png', rgb)
