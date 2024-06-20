import time

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
    #print(tau)
    # 分割子集
    H0 = np.zeros_like(hist)
    H0[:tau] = hist[:tau]
    H1 = np.zeros_like(hist)
    H1[tau:] = hist[tau:]

    min_H0, max_H0 = np.min(H0[:tau]), 255
    min_H1, max_H1 = np.min(H1[tau:]), np.max(H1[tau:])
    #print(min_H0, max_H0,min_H1, max_H1)
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


def adaptive_denoising(img, theta=0.5, ksize=5):
    # 计算局部方差
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = gray / 255.0

    mean = cv2.blur(gray, (ksize, ksize))
    mean_sq = cv2.blur(gray**2, (ksize, ksize))
    local_variance = mean_sq - mean**2

    # 平均滤波器输出
    avg_filtered = cv2.blur(gray, (ksize, ksize))

    # 自适应加权因子alpha
    alpha = 1 / (1 + theta * local_variance)

    # 获取详细的高频区域
    high_freq_detail = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    high_freq_detail = cv2.cvtColor(high_freq_detail, cv2.COLOR_RGB2GRAY)
    cv2.imshow('avg_filtered', avg_filtered)
    cv2.imshow('high_freq_detail', high_freq_detail)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 最终滤波器输出
    output = (1 - alpha) * high_freq_detail + alpha * avg_filtered
    output = (output * 255).astype(np.uint8)
    output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)

    return output


def gaussian_weighting(x, p=5):
    return (10 / p) * np.exp((((x - 127.5)**2) / (127.5**2))*0.5)


def locally_contrast_stretched(img):
    stretched_img = (img - img.min()) * (255 / (img.max() - img.min()))
    #print(img.min(),img.max())
    stretched_img = stretched_img.astype(np.uint8)

    return stretched_img


def hdr_fusion(I_o, I_n, I):
    weights_o = gaussian_weighting(I_o / 255.0)
    weights_n = gaussian_weighting(I_n / 255.0)
    weights_u = gaussian_weighting(I / 255.0)

    O = I_o * weights_o
    N = I_n * weights_n
    I = I * weights_u

    SO = locally_contrast_stretched(I_o)
    SN = locally_contrast_stretched(I_n)
    SI = locally_contrast_stretched(I)

    H = (SO*O + SN*N + SI*I)/(O + N + I)

    return H.astype(np.uint8)


def main():
    # 开始时间
    start_time = time.time()
    image = cv2.imread('images/berlin.png')
    # 拉伸
    image_o, image_n = Stretching_image(image, w=0.5)

    # 显示图像
    cv2.imshow('Original Image', image)
    cv2.imshow('Exposed Image', image_o)
    cv2.imshow('Underexposed Image', image_n)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # 去噪
    #image_o = cv2.blur(image_o, (3,3))
    #image_o = adaptive_denoising(image_o, theta=0.5, ksize=5)
    #cv2.imshow('Exposed Image', image_o)

    # 融合图像
    hdr_image = hdr_fusion(image_o, image_n, image)
    cv2.imshow('hdr_image', hdr_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # 结束时间
    end_time = time.time()

    #运行时间
    print(f"程序运行时间: {end_time - start_time} 秒")


if __name__ == "__main__":
    main()
