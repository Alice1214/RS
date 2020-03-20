# -*- coding: utf-8 -*-
"""
* Content：使用MinHashLSHForest对微博新闻句子进行检索 weibo.txt
           针对某句话进行Query，查找Top-3相似的句子
* Author:  HuiHui
* Date:    2020-03-20
* Reference:

"""
import nltk
from datasketch import MinHash, MinHashLSH, MinHashLSHForest
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba.posseg as pseg
import re

# 读取文件
f = open('./weibos.txt', 'r', encoding='UTF-8')
text = f.read()
# 以句号，叹号，问号作为分隔，去掉\n换行符号
sentences = re.split('[。！？]', text.replace('\n', '')) #句子
# 最后一行如果为空，则删除
if sentences[len(sentences)-1] == '':
    sentences.pop()
#print(sentences)

# 将句子进行分词
def get_item_str(item_text)->str:
    item_str = ""
    item=(pseg.cut(item_text))
    for i in list(item):
        #去掉停用词
        if i.word not in list(stop):
            item_str += i.word
            #tfidf_vectorizer.fit_transform的输入需要空格分隔的单词
            item_str += " "
    return item_str

# 对item_str创建MinHash
def get_minhash(item_str):
    temp = MinHash()
    for d in item_str:
        temp.update(d.encode('utf8'))
    return temp

# 设置停用词
stop=[line.strip() for line in open('./hit_stopwords.txt').readlines()] #❓
print("停用词：",stop)

# 得到分词后的documents
documents = []
for item_text in sentences:
    # 将item_text进行分词
    item_str = get_item_str(item_text)
    documents.append(item_str)
#print(documents)

# 创建LSH Forest及MinHash对象
minhash_list = []
forest = MinHashLSHForest()
for i in range(len(documents)):
    #得到train_documents[i]的MinHash
    temp = get_minhash(documents[i])
    minhash_list.append(temp)
    forest.add(i, temp)  #内容载入LSHForest系统
# index所有key，以便可以进行检索
forest.index()

#查询Top-3相似的句子
query = '换言之，中国足球，不需要名帅，也不需要外籍教练，因为一点儿毛用也没有'
# 将item_text进行分词
item_str = get_item_str(query)
print("query分词结果：",item_str)
# 得到item_str的MinHash
minhash_query = get_minhash(item_str)
print("query minhash 结果：",minhash_query)
# 查询forest中与query相似的Top-3个邻居
result = forest.query(minhash_query, 3)
for i in range(len(result)):
    print(result[i], minhash_query.jaccard(minhash_list[result[i]]), documents[result[i]].replace(' ', ''))
print("Top-3邻居：", result)