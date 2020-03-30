## RS12 Thinking
**1.  举一个你之前做过的预测例子（用的什么模型，解决什么问题，比如我用LR模型，对员工离职进行了预测，效果如何... 请分享到课程微信群中）**

答：对于定向广告，用户没有很明显的意图，而搜索广告具有主动的Query查询。定向广告是基于广告候选集、用户特征、用户行为以及上下文场景对广告的点击情况做出预测，常见的算法模型有DIN、DIEN、DSIN；搜索广告是一个基于query的排序学习问题，常见的模型算法有RankNet，LambdaRank和LambdaMART。

**2. 请你思考，在你的工作中，需要构建哪些特征（比如用户画像，item特征...），这些特征都包括哪些维度（鼓励分享到微信群中，进行交流）**

答：一般模型：LR、MLR、DNN。

Attention机制模型：DIN、DIEN、DSIN。

**3.  你认为，NGBoost对之后的算法会有怎样的影响？**

答：用户的兴趣是多样的，对于一个广告商品，只有一部分的历史数据对目前的点击预测有帮助。Attention机制的思想是在pooling的时候，与 candidate Ad 相关的商品权重大一些，与candidate Ad 不相关的商品权重小一些。

原理：在对用户行为的embedding计算上引入了attention network（Activation Unit），通过Attention Unit，对每个兴趣表示赋予不同的权值。Activation Unit输入包括用户行为embedding和候选广告embedding以外，还考虑了他们两个的外积，再通过前馈神经网络，计算得到用户行为的激活权重，最终得到用户行为表示向量。对于不同的candidate ad，得到的用户行为表示向量是不同的。
