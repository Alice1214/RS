## RS10 Thinking
**1.  排序模型按照样本生成方法和损失函数的不同，可以划分成Pointwise,Pairwise, Listwise三类方法，这三类排序方法有何区别？**

答：这三类方法训练的样本不同，要学习（拟合）的数据不同，计算复杂度及适用的场景也不同。

（1）Pointwise，针对单一文档，优点是简单，不足在于没有考虑样本之间的位置信息（doc之间的相对顺序），可以采用多分类或回归算法（GBDT，LR等）；

（2）Pairwise，关注文档的顺序关系，转换为pairwise分类问题，没有考虑文档出现在结果中的位置，排在搜索结果前面的文档更为重要，如果排序错误，代价很高（SVM Rank，RankBoost，RankNet）；

（3）Listwise，将一次Query对应的所有搜索结果列表作为一个训练样例不需要对数据进行Transform，直接优化整个集合序列，优化目标NDCG（ListNet, AdaRank，SoftRank，LambdaRank，LambdaMART）。

**2.  排序模型按照结构划分，可以分为线性排序模型、树模型、深度学习模型，这些模型都有哪些典型的代表？**

答： 

线性排序模型：LR，引入自动二阶交叉特征的FM和FFM

树模型：GBDT和GBDT+LR

深度学习模型：Wide & Deep, DeepFM, NFM

**3.  NDCG如何计算？**

答：

![img](file://localhost/private/var/folders/13/8srvfrhj3wqbd5zcd_vr7l7m0000gn/T/TemporaryItems/msoclip/0/clip_image002.png)

![img](file://localhost/private/var/folders/13/8srvfrhj3wqbd5zcd_vr7l7m0000gn/T/TemporaryItems/msoclip/0/clip_image004.png)

![img](file://localhost/private/var/folders/13/8srvfrhj3wqbd5zcd_vr7l7m0000gn/T/TemporaryItems/msoclip/0/clip_image006.png)

![img](file://localhost/private/var/folders/13/8srvfrhj3wqbd5zcd_vr7l7m0000gn/T/TemporaryItems/msoclip/0/clip_image008.png)

**4.  搜索排序和推荐系统的相同和不同之处有哪些？**

答：推荐系统是发散的、无意识的主动推荐，相比search而言，排序准确性不一定是最重要的，多样性也导致了推荐场景没有像搜索一样适合做 pairwise 的样本，多采用pointwise模型，预测出来的分数，具有实际的物理意义，代表了目标用户点击item的预测概率；

搜索排序是基于某Query进行的结果排序，期望用户选中的在排序结果中是靠前的，是有意识的被动推荐。

**5.  Listwise排序模型能否应用到推荐系统中？**

答：可以。但是Listwise排序模型考虑所有结果的排序顺序，其计算量大，而推荐系统的排序准确性不是最重要的，其多样性也导致了推荐场景没有像搜索一样适合做 pairwise 的样本，一般多采用单点法。

 