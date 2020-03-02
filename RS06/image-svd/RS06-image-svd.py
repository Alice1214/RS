# !/usr/bin/env python
# -*- coding=utf-8 -*-
# Content：选择任意一张图片，对其进行灰度化，然后使用SVD进行图像的重构，当奇异值数量为原有的1%，10%，50%时，输出重构后的图像
# Author:  HuiHui
# Date:    2020-03-02
# Reference:

import numpy as np
from scipy.linalg import svd
from PIL import Image

import matplotlib
matplotlib.use('TkAgg') #⚠️加上plt.show()就能显示
import matplotlib.pyplot as plt

# 取前k个特征，对图像进行还原
def get_image_feature(s,k):
    # 保留s前k个特征值
    s_temp= np.zeros(s.shape[0]) # s.shape[0]表示s的垂直尺寸
    s_temp[0:k] = s[0:k]
    print(s[0:k])
    s = s_temp * np.identity(s.shape[0]) # np.identity（）得到s.shape[0]维的单位矩阵
    # 用新的s，以及p,q重构A
    temp = np.dot(p, s)
    temp = np.dot(temp, q)
    plt.imshow(temp, cmap='gray', interpolation='nearest')
    plt.show()

# 加载256色图片
image = Image.open('/Users/wangdonghui/Desktop/ZGZ/RS/AI-Training-Course/RS06/image-svd/dog.jpg')
# 显示原图片
plt.imshow(image, interpolation='nearest')
plt.show()
#图像灰度化(R=G=B)
gray=image.convert('L')
A = np.array(gray)
print(A)
print("数组的shape",A.shape)
# 显示灰度化图片
plt.imshow(A, cmap ='gray',interpolation='nearest')
plt.show()

# 对图像矩阵A进行奇异值分解，得到p,s,q
p,s,q = svd(A, full_matrices=False) #full_matrices=False,则p,s,q形状为（m,k）(k,)(k,n)，k=min(m,n)
print("s.shape:",s.shape) #⚠️(800*1)
print("p.shape:",p.shape)
print("q.shape:",q.shape)
# 取前k个特征，对图像进行还原
get_image_feature(s, 8)
get_image_feature(s, 80)
get_image_feature(s, 400)




