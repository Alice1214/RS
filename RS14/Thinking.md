## RS14 Thinking
**1.  当我们思考数据源的时候，都有哪些维度，如果你想要使用爬虫抓取数据，都有哪些工具**

答：对于定向广告，用户没有很明显的意图，而搜索广告具有主动的Query查询。定向广告是基于广告候选集、用户特征、用户行为以及上下文场景对广告的点击情况做出预测，常见的算法模型有DIN、DIEN、DSIN；搜索广告是一个基于query的排序学习问题，常见的模型算法有RankNet，LambdaRank和LambdaMART。

**2. 今天讲解了时间序列预测的两种方式，实际上在数据库内建时间属性后，可以产生时序数据库，请思考什么是时序数据库？为什么时间序列数据成为增长最快的数据类型之一（请思考并分享到班级微信群中）**

答：一般模型：LR、MLR、DNN。

Attention机制模型：DIN、DIEN、DSIN。

**3.  开源是当前重要的Trend，我们使用的statsmodels.tsa，tensorflow/keras都是开源工具
1）你都知道有哪些和AI相关的开源工具？
2）阿里，微软，百度 都有哪些和AI相关的开源工具（包括LightGBM）
3）了解和使用这些工具，对于我们有哪些价值？**

答：用户的兴趣是多样的，对于一个广告商品，只有一部分的历史数据对目前的点击预测有帮助。Attention机制的思想是在pooling的时候，与 candidate Ad 相关的商品权重大一些，与candidate Ad 不相关的商品权重小一些。

原理：在对用户行为的embedding计算上引入了attention network（Activation Unit），通过Attention Unit，对每个兴趣表示赋予不同的权值。Activation Unit输入包括用户行为embedding和候选广告embedding以外，还考虑了他们两个的外积，再通过前馈神经网络，计算得到用户行为的激活权重，最终得到用户行为表示向量。对于不同的candidate ad，得到的用户行为表示向量是不同的。
