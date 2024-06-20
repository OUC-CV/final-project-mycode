import cv2
import matplotlib.pyplot as plt

image = cv2.imread('images/fig2.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 绘制直方图
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(hist)
plt.title('image hist')
plt.xlim([0, 256])
plt.show()


image_o = cv2.imread('images/fig2_o.png')
gray = cv2.cvtColor(image_o, cv2.COLOR_BGR2GRAY)
# 绘制直方图
hist_o = cv2.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(hist_o)
plt.title('image_o hist')
plt.xlim([0, 256])
plt.ylim([0, 5000])
plt.show()

image_n = cv2.imread('images/fig2_n.png')
gray = cv2.cvtColor(image_n, cv2.COLOR_BGR2GRAY)
# 绘制直方图
hist_n = cv2.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(hist_n)
plt.title('image_n hist')
plt.xlim([0, 256])
plt.ylim([0, 10000])
plt.show()
