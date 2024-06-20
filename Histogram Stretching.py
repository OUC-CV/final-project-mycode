import cv2
import matplotlib.pyplot as plt
import numpy as np


# 阈值计算
def calculate_threshold(hist, w):
    M = np.sum(hist)
    min_diff = float('inf')
    tau = 0
    for t in range(len(hist)):
        current_diff = abs(w - (1/M) * np.sum(hist[:t+1]))
        if current_diff < min_diff:
            min_diff = current_diff
            tau = t
    return tau


# 直方图拉伸
def Stretching_image(image, w=1):
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)

    # 得到灰度图像的直方图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()

    # 计算阈值 τ
    tau = calculate_threshold(hist, w)
    # 分割子集
    H0 = np.zeros_like(hist)
    H0[:tau] = hist[:tau]
    H1 = np.zeros_like(hist)
    H1[tau:] = hist[tau:]

    min_H0, max_H0 = np.min(H0), tau
    min_H1, max_H1 = np.min(H1), np.max(H1)

    # 拉伸V
    V0 = np.copy(V)
    V1 = np.copy(V)

    V0 = (V0 - min_H0) / (max_H0 - min_H0) * 255
    V1 = (V1 - min_H1) / (max_H1 - min_H1) * 255

    V0 = np.clip(V0,0,255).astype(np.uint8)
    V1 = np.clip(V1,0,255).astype(np.uint8)

    # 将拉伸后的 V 通道应用到 HSV 图像中
    hsv_o = cv2.merge([H, S, V0])
    hsv_n = cv2.merge([H, S, V1])

    # 转换回 RGB 颜色空间
    exposed_image = cv2.cvtColor(hsv_o, cv2.COLOR_HSV2BGR)
    underexposed_image = cv2.cvtColor(hsv_n, cv2.COLOR_HSV2BGR)

    return exposed_image, underexposed_image


# 读取图像
image = cv2.imread('images/fig4.png')
image_o, image_n = Stretching_image(image, w=0.5)

# 显示图像和直方图
cv2.imshow('Original Image', image)
cv2.imshow('Exposed Image', image_o)
cv2.imshow('Underexposed Image', image_n)
cv2.waitKey(0)
cv2.destroyAllWindows()


# 显示直方图
def hist_show(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    plt.plot(hist)
    plt.title('Image Histogram')
    plt.xlim([0, 256])
    plt.show()


hist_show(image)
hist_show(image_o)
hist_show(image_n)
