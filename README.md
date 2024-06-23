[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/8oH8aWc3)
## 项目报告

### 题目 

High Dynamic Range Imaging

### 绪论 

项目描述视频
【基于单图像的局部直方图拉伸和空间自适应去噪的无幽灵高动态范围成像】 https://www.bilibili.com/video/BV1mKgrejEo9/?share_source=copy_web&vd_source=38ed91729af2a5379cbc430643f5989c
#### 问题和动机

本次计算机视觉课的期末作业统一布置了High Dynamic Range Imaging的题目，于是我们就去查阅了许多关于HDR的论文。由于我们平时都使用手机去拍照和处理照片，就将目光放到了应用于移动设备上的HDR技术。我们看到了由**Jaehyun Im, Jaehwan Jeon, Member, IEEE, Monson H. Hayes, Fellow, IEEE, and Joonki Paik, Member, IEEE**所作的**Single Image-Based Ghost-Free High Dynamic Range Imaging Using Local Histogram Stretching and Spatially-Adaptive Denoising**这篇论文，对文中提出的HDR方法有了兴趣，作者并没有进行项目开源，查询发现没有复现的项目，于是决定复现文中的方法

#### 背景资料

本篇文章提出了一种基于单一图像的高动态范围成像方法。由于高质量的成像设备在消费电子市场上很流行，因此获取真实照片变得更容易。现实采集的三个基本因素包括：i）高空间分辨率，ii)精确的色彩再现，和iii)高动态范围。HDR成像技术是近年来出现的一种技术，在给数字成像带来一场新的革命中发挥了重要作用。而现有的多种基于图像的HDR方法在获取多个不同曝光的低动态范围图像时，只能在没有相机和物体移动的情况下工作。为了克服这种不现实的限制，本文使用局部直方图拉伸从单个输入图像中制作了三张LDR图像。提出了一种保边空间自适应去噪方法来抑制直方图拉伸过程中放大的噪声。由于该方法从单个输入图像中自生成三个直方图拉伸的LDR图像，因此在曝光时间内相机和物体之间相对运动产生的鬼影被固有地去除。因此，该方法可应用于移动电话相机和消费紧凑型相机等移动成像设备，以嵌入式或后处理软件的形式提供无鬼影的HDR功能。

#### 相关工作

作者在文章中与Debevec，Im，和Bilcu所提出的三种方法进行了比较。
##### P. Debevec and J. Malik, “Recovering high dynamic range radiance maps from photographs
文章主要讨论了一种从多张不同曝光时间的普通照片中恢复高动态范围（HDR）辐射图的方法。具体来说，作者提出了一种算法，可以通过融合多张具有不同曝光设置的照片来生成一张包含更大亮度范围的HDR图像。这样的方法可以克服传统摄影技术在高对比度场景下的局限，捕捉到从最亮到最暗的丰富细节。

##### J. Im, S. Lee, and J. Paik, “Improved elastic registration for ghost artifact free high dynamic range imaging
文章主要讨论了一种改进的弹性配准方法，以解决在生成高动态范围图像过程中出现的鬼影问题。鬼影是由于多张不同曝光时间的照片在合成时因运动或对齐不精确而产生的伪影。这种现象会显著降低HDR图像的质量。

##### R. Bilcu, A. Burian, A. Knuutila, and M. Vehvilainen, “High dynamic range imaging on mobile devices
文章主要探讨了如何在移动设备上实现高动态范围（HDR）成像技术。随着移动设备摄像头性能的提升以及用户对高质量图像需求的增加，HDR技术在移动设备上的应用变得越来越重要。

#### 我们的方法

![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/a1d15dc7-7220-4e4f-9acf-7f2f3d4a7b22)<br>
这是作者在文中提出的基于单个输入图像的无幽灵HDR算法的基本框架，也救是我们复刻项目的方法框架。通过单个输入的图像，得到它的灰度亮度直方图，将它转化到HSV空间中，根据本文提出的具体方法来拉伸它的v通道，再将拉伸过的V通道和H，S通道转化回RGB空间，得到正常，过度曝光，未曝光三张图片，对三张图片进行自适应降噪，然后融合这三张图片得到HDR图像。

### 方法的具体细节

首先我们先复刻论文中的第一步，Local Histogram Stretching，实现在我们的Histogram Stretching.py中<br>
首先使用[4]中最初提出的WHS方法估计了一个合适的拉伸区域，WHS是基于数据分离单元构建的，它将数据集划分为两个子集。H是灰度图像的亮度直方图，数据分离的第一步是设置一个阈值,其定义为：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/b993fc9f-6742-46ea-85d5-a9827b86b8c4)<br>
w表示一个加权因子（作者并未指出加权因子的值，因此我们只能自己尝试一个比较合适的值），M表示H中的数据点的总数，L表示H的维数，等于亮度直方图的256，使用指定的阈值，将H分成两个子集H0和H1：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/dc3f44f9-131c-4dad-a8af-40e596b8dd7e)<br>
之后根据作者提出的公式拉伸V通道，拉伸完后将hsv重新组合转回RGB空间：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/b6f138f3-cf99-43c0-b27d-f34b5446d02f)<br>
我们实现的关于阈值的计算，分割子集以及拉伸v通道：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/c790cac8-6127-4735-9a2d-ba0ec60c4747)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/65bfd9c6-4bb7-4bee-a6a9-0275d5dea5d0)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/b6d1844b-298c-4ebb-bea2-847785015c08)<br>

第二步是Edge-Preserving Spatially Adaptive Denoising，在局部直方图拉伸过程中，噪声与亮度水平一起被放大，为了在保留边缘的同时去除噪声，该方法采用空间自适应去噪算法，从有噪声的LDR图像中获取详细的高频区域，并从平均滤波器的结果中获取平坦区域，并在两个滤波器之间进行适当的加权如下：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/78f2a45a-78d6-4f4f-8e8f-bb768ef010f9)<br>
加权因子计算中的调优参数θ在本文中也未提到，也只能尝试出来。文中“the proposed method employs a spatially adaptive denoising algorithm that takes detailed high-frequency regions from a noisy LDR image
and takes flat regions from the result of averaging filter with an appropriate amount of weighting between the two ”提到的“spatially adaptive denoising algorithm”未明确的指向某一个降噪算法，我们采用的是cv2.fastNlMeansDenoisingColored（）降噪算法，该算法能完成文中提到的“takes detailed high-frequency regions”功能，而“averaging filter”我们采用的是cv2.blur（）降噪算法。：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/a55f16c6-a621-44fc-886e-1bb75c46cb30)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/81e04125-8451-4604-b66c-c9fb3e02222a)<br>

第三步是LDR Image Fusion：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/ec53985a-f99e-44f4-a350-b5ae3ab19fbd)<br>
采用局部对比度拉伸LDR图像和原图像的加权的一种算法，然而这里的p标准化常数的值在本文中也没有提及。我们的实现代码如下：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/dac5facb-6500-4771-832e-df9110d41ccd)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/9520403f-0c7d-4af0-b5c6-cf95db342e46)<br>

### 结果

本文中的三张测试图片：
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/73c1b4fc-c575-4adc-abf0-8acf075c0e7e)<br>

本文得到的结果图：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/5d690b66-9c1c-43d3-aeac-1d4c5c60a715)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/4c2a50c4-82c3-415f-aa58-bc344f11d2dc)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/82862e6b-fd48-4892-81e5-b6f466c2c0df)<br>

我们自己的方法使用的就是本文中测试的这三张图片，我们的方法对于作者提到的降噪的部分实现的效果并不理想，降噪实现后所得到图像有重影，以下是包括降噪的部分：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/6c88c5c9-e1e3-4ceb-826e-a0de0bf3d43d)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/51bebbfb-c5e7-47e1-b7c4-65aa38cee8e8)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/58c31867-cbe0-4cb5-b400-caddefeba8ac)<br>

而以下是进行简单的降噪的部分，虽然图片质量比较低，但是混合的效果不错：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/c2b59947-f0c1-4f0f-a650-a30470ac6332)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/cd6200a1-fc0a-408f-951a-31c513e4a36b)<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/2034d597-5b55-4bc1-8f93-d4ec72454d43)<br>

我们程序的运行时间和作者的对比，均略慢于作者：<br>
![image](https://github.com/OUC-CV/final-project-mycode/assets/111495997/ae2a61cb-e492-44df-b51b-fb0b9b6cec71)<br>

### 总结和讨论

本文提出了一种基于单图像的无鬼影HDR方法，利用局部直方图拉伸和保留边缘的空间自适应去噪。由于现有的基于多框架的HDR方法只能在获取多个不同暴露的LDR图像时没有摄像机和物体移动的情况下工作，所以在动态环境中，鬼影伪影是不可避免的。为了解决这一问题，该方法利用局部直方图拉伸技术从单个输入图像中自生成3幅LDR图像。为了抑制直方图拉伸过程中的噪声放大，提出了一种边缘保持空间自适应去噪算法。然后，通过融合三个局部直方图和噪声降低的LDR图像来生成HDR图像。该方法可以利用单一输入图像生成无伪影的HDR图像。因此，该方法易于使用消费相机获取，无需使用三脚架获取LDR图像，并可应用于手机相机和消费紧凑型相机，以嵌入式或po的形式提供无鬼影HDR功能<br>
而我们对本论文的复现基本实现了上述功能，在拉伸直方图的部分效果比较好，而在单独降噪是也有较好的效果，而将两个降噪的结果加权融合后得不到理想的效果，图片中会出现较明显的重影部分，从而也导致hdr融合的结果不好。而去除有问题的降噪后，得到的hdr融合图片的效果还是可观的，说明我们在hdr融合上也基本实现了本文提出的功能。<br>
总的来说这篇论文的复刻还是有一定难度的，首先在使用的照片上，作者没有单独的提供他们实验所用的原图片，我们是从文中直接复制的，图片质量对比原图来说有一定的压缩和下降。其次本次中存在着多个加权参数，作者并未直接在文中提出，需要我们自己定夺，而且文中提到的有些方法我们理解的不是很透彻，可能和作者提出的问题有比较大的偏差，这是我们自身水平所不足导致的。通过本次实验我们学到了许多关于hdr图像处理的新知识和技巧，尝试了许多新的功能，查阅了几篇文献，受益匪浅。

### 个人贡献声明

小组成员：
吴俊毅 负责 论文挑选与阅读 主要代码实现 实验报告 50% <br>
吴勇智 负责 论文挑选与阅读 部分代码实现 项目描述视频

### 引用参考

[1] P. Debevec and J. Malik, “Recovering high dynamic range radiance maps from photographs,” Proc. ACM SIGGRAPH, pp. 369-378, August 1997.<br>

[2] J. Im, S. Lee, and J. Paik, “Improved elastic registration for ghost artifact free high dynamic range imaging,” IEEE Trans. Consumer Electronics, vol. 57, May 2011.<br>

[3] R. Bilcu, A. Burian, A. Knuutila, and M. Vehvilainen, “High dynamic range imaging on mobile devices,” IEEE Conf. Electronics, Circuits, Systems, pp. 1312-1315, 2008.<br>

[4] S. Pei, Y. Zeng, and J. Ding, “Color images enhancement using weighted histogram separation,” IEEE Conf. Int. Conf. Image Processing, pp. 2889-2892, 2006.<br>
