[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/8oH8aWc3)
## 项目报告

### 题目 

High Dynamic Range Imaging

### 绪论 

项目描述视频

#### 问题和动机

本次计算机视觉课的期末作业统一布置了High Dynamic Range Imaging的题目，于是我们就去查阅了许多关于HDR的论文。由于我们平时都使用手机去拍照和处理照片，就将目光放到了应用于移动设备上的HDR技术。我们看到了由**Jaehyun Im, Jaehwan Jeon, Member, IEEE, Monson H. Hayes, Fellow, IEEE, and Joonki Paik, Member, IEEE**所作的**Single Image-Based Ghost-Free High Dynamic Range Imaging Using Local Histogram Stretching and Spatially-Adaptive Denoising**这篇论文，对文中提出的HDR方法有了兴趣，作者并没有进行项目开源，查询发现没有复现的项目，于是决定复现文中的方法

#### 背景资料

本篇文章提出了一种基于单一图像的高动态范围成像方法。由于高质量的成像设备在消费电子市场上很流行，因此获取真实照片变得更容易。现实采集的三个基本因素包括：i）高空间分辨率，ii)精确的色彩再现，和iii)高动态范围。HDR成像技术是近年来出现的一种技术，在给数字成像带来一场新的革命中发挥了重要作用。而现有的多种基于图像的HDR方法在获取多个不同曝光的低动态范围图像时，只能在没有相机和物体移动的情况下工作。为了克服这种不现实的限制，本文使用局部直方图拉伸从单个输入图像中制作了三张LDR图像。提出了一种保边空间自适应去噪方法来抑制直方图拉伸过程中放大的噪声。由于该方法从单个输入图像中自生成三个直方图拉伸的LDR图像，因此在曝光时间内相机和物体之间相对运动产生的鬼影被固有地去除。因此，该方法可应用于移动电话相机和消费紧凑型相机等移动成像设备，以嵌入式或后处理软件的形式提供无鬼影的HDR功能。

#### 相关工作

作者在文章中与Debevec，Im，和Bilcu所提出的三种方法进行了比较。
##### P. Debevec and J. Malik, “Recovering high dynamic range radiance maps from photographs,” 
文章主要讨论了一种从多张不同曝光时间的普通照片中恢复高动态范围（HDR）辐射图的方法。具体来说，作者提出了一种算法，可以通过融合多张具有不同曝光设置的照片来生成一张包含更大亮度范围的HDR图像。这样的方法可以克服传统摄影技术在高对比度场景下的局限，捕捉到从最亮到最暗的丰富细节。

##### J. Im, S. Lee, and J. Paik, “Improved elastic registration for ghost artifact free high dynamic range imaging,” 
文章主要讨论了一种改进的弹性配准方法，以解决在生成高动态范围图像过程中出现的鬼影问题。鬼影是由于多张不同曝光时间的照片在合成时因运动或对齐不精确而产生的伪影。这种现象会显著降低HDR图像的质量。

##### R. Bilcu, A. Burian, A. Knuutila, and M. Vehvilainen, “High dynamic range imaging on mobile devices,” 
文章主要探讨了如何在移动设备上实现高动态范围（HDR）成像技术。随着移动设备摄像头性能的提升以及用户对高质量图像需求的增加，HDR技术在移动设备上的应用变得越来越重要。

#### 我们的方法

![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/a1d15dc7-7220-4e4f-9acf-7f2f3d4a7b22)<br>这是作者在文中提出的基于单个输入图像的无幽灵HDR算法的基本框架，也救是我们复刻项目的方法框架。通过单个输入的图像，得到它的灰度亮度直方图，将它转化到HSV空间中，根据本文提出的具体方法来拉伸它的v通道，得到正常，过度曝光，未曝光三张图片，以及进行自适应降噪，再转回RGB空间，然后融合这三张图片得到HDR图像。

### 方法的具体细节

### 结果

### 总结和讨论

### 个人贡献声明

小组成员：
吴俊毅 负责
吴勇智 负责

### 引用参考

[1] P. Debevec and J. Malik, “Recovering high dynamic range radiance maps from photographs,” Proc. ACM SIGGRAPH, pp. 369-378, August 1997.

[2] J. Im, S. Lee, and J. Paik, “Improved elastic registration for ghost artifact free high dynamic range imaging,” IEEE Trans. Consumer Electronics, vol. 57, May 2011.

[3] R. Bilcu, A. Burian, A. Knuutila, and M. Vehvilainen, “High dynamic range imaging on mobile devices,” IEEE Conf. Electronics, Circuits, Systems, pp. 1312-1315, 2008.

[4] S. Pei, Y. Zeng, and J. Ding, “Color images enhancement using weighted histogram separation,” IEEE Conf. Int. Conf. Image Processing, pp. 2889-2892, 2006.
