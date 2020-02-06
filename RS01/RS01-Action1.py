# !/usr/bin/env python
# -*- coding=utf-8 -*-
# Content：针对mnist数据集进行分类，采用CART决策树（工具使用sklearn中的CART）
# Author:  HuiHui
# Date:    2020-01-20
# Reference:

# MNIST数据集：MNIST数据集来自美国国家标准与技术研究所(NIST). 训练集
#              由来自 250 个不同人手写的数字构成, 其中 50% 是高中学生
#              50% 来自人口普查局 (the Census Bureau) 的工作人员. 测
#              试集也是同样比例的手写数字数据。训练数据集共有60000张
#              图片和相应的标签，测试数据集共有10000张图片和相应的标签，
#              并且每个图片都有28*28个像素。
from sklearn.model_selection import train_test_split #划分数据集
from sklearn import preprocessing #预处理
from sklearn.metrics import accuracy_score #度量
from sklearn.datasets import fetch_mldata
from sklearn import tree
import matplotlib
matplotlib.use('TkAgg') #⚠️加上plt.show()就能显示
import matplotlib.pyplot as plt

# 加载mnist数据
mnist = fetch_mldata('MNIST original',data_home='/Users/wangdonghui/Desktop/ZGZ/RS/Lesson/L1/')# 国内网络无法正常访问mldata，需提前下载放到在当前文件夹下面新建的mldata文件夹中
data=mnist.data#具体数据，70000*784

# 数据探索
print(data.shape)
# 查看第一幅图像
image_0=data[0].reshape(28,28) #抓取第一个实例，重新形成28*28数组
print(image_0)
# 第一幅图像代表的数字含义
print(mnist.target[0])
# 将第一幅图像显示出来
plt.gray()
plt.title('Handwritten Digits')
plt.imshow(image_0,cmap=matplotlib.cm.binary,interpolation="nearest")
plt.show()

# 分割数据，将25%的数据作为测试集，其余作为训练集
train_x, test_x, train_y, test_y = train_test_split(data, mnist.target, test_size=0.25, random_state=33)
# 随机数种子：产生该组随机数的编号。每次都填同一个正整数，其他参数一样的情况下得到的随机数组是一样的，
#             但填0或不填，每次都会不一样。

# 采用Z-Score规范化（也称标准差标准化，经过处理的数据的均值为0，标准差为1）
ss = preprocessing.StandardScaler()
train_ss_x = ss.fit_transform(train_x)#不仅计算数据的均值和方差，还会基于计算出来的均值和方差来转换数据，从而把数据转换成标准的正态分布。⚠️这里可以先fit，再transform。
test_ss_x = ss.transform(test_x)#⚠️这里用训练数据的均值和方差来转换。它只进行转换，只是把数据转换成标准的正态分布

# 创建分类器
clf = tree.DecisionTreeClassifier()
clf.fit(train_ss_x, train_y) #根据给定的训练数据和参数拟合模型
predict_y=clf.predict(test_ss_x) #预测
print('LR准确率: %0.4lf' % accuracy_score(predict_y, test_y))#计算准确率

# ❓mnist数据集怎么划分训练集和测试集比较合理
# ❓mnist数据集怎样做数据预处理得到的效果更好
# ❓mnist数据集规模太大，直接用所有数据训练模型会死机怎么处理