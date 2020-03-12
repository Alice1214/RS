# !/usr/bin/env python
# !/usr/bin/env python
# -*- coding=utf-8 -*-
# Content：将Word转换成Vec，然后计算相似度
# Author:  HuiHui
# Date:    2020-03-11
# Reference:

from gensim.models import word2vec
import multiprocessing

# 如果目录中有多个文件，可以使用PathLineSentences
segment_folder = './segment'
sentences = word2vec.PathLineSentences(segment_folder) #如果用列表，当输入量很大的时候，大会占用大量内存，因此用迭代器

# 设置模型参数，进行训练
model = word2vec.Word2Vec(sentences, size=128, window=5, min_count=5,workers=multiprocessing.cpu_count()) #worker训练模型线程数
#'曹操'词向量
print(model['曹操'])
# 计算和曹操最相近的15个词
# ❓每次运行结果都不一样
for key in model.wv.similar_by_word('曹操', topn =15):
    print(key)
print(model.wv.most_similar('曹操'))#输出最相近10个词

# 计算得出曹操+刘备-张飞
print(model.wv.most_similar(positive=['曹操', '刘备'], negative=['张飞']))

# 保存模型
model.save('/Users/wangdonghui/Desktop/ZGZ/RS/AI-Training-Course/RS07/model/word2Vec.model') #要使用绝对路径，否则报错
