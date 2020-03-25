## RS11 Thinking
**1.  电商定向广告和搜索广告有怎样的区别，算法模型是否有差别？**

答：对于定向广告，用户没有很明显的意图，而搜索广告具有主动的Query查询。定向广告是基于广告候选集、用户特征、用户行为以及上下文场景对广告的点击情况做出预测，常见的算法模型有DIN、DIEN、DSIN；搜索广告是一个基于query的排序学习问题，常见的模型算法有RankNet，LambdaRank和LambdaMART。

**2.  定向广告都有哪些常见的使用模型，包括Attention机制模型？**

答：一般模型：LR、MLR、DNN。

Attention机制模型：DIN、DIEN、DSIN。

**3.  DIN中的Attention机制思想和原理是怎样的？**

答：用户的兴趣是多样的，对于一个广告商品，只有一部分的历史数据对目前的点击预测有帮助。Attention机制的思想是在pooling的时候，与 candidate Ad 相关的商品权重大一些，与candidate Ad 不相关的商品权重小一些。

原理：在对用户行为的embedding计算上引入了attention network（Activation Unit），通过Attention Unit，对每个兴趣表示赋予不同的权值。Activation Unit输入包括用户行为embedding和候选广告embedding以外，还考虑了他们两个的外积，再通过前馈神经网络，计算得到用户行为的激活权重，最终得到用户行为表示向量。对于不同的candidate ad，得到的用户行为表示向量是不同的。

**4.  DIEN相比于DIN有哪些创新？**

答：DIEN基于DIN的Attention机制，考虑了用户兴趣随时间的演化。DIEN在 Embedding layer 和 Concatenate layer 之间加入了生成兴趣的兴趣抽取层和模拟兴趣演化的兴趣演化层。兴趣抽取层使用了GRU的结构抽取了每一个时间片内用户的兴趣，并使用auxiliary loss 进行额外的监督，用下一时刻的行为监督当前时刻兴趣的学习，促使GRU在提炼兴趣表达上更高效；兴趣演化层利用序列模型 AUGRU 的结构将不同时间的用户兴趣串联起来，形成兴趣进化的链条，最终把当前时刻的“兴趣向量”输入上层的多层全连接网络，与其他特征一起进行最终的 CTR 预估。

**5.  DSIN关于Session的洞察是怎样的，如何对Session兴趣进行表达？**

答：Sequence视角，可以看到user interest的变化；Session视角，每个Session（将Sequence按照30min间隔划分）中的行为是相近的，而在不同会话之间差别是很大的。

首先通过序列切分层，将Sequence切分成Session；然后在会话兴趣抽取层中，使用带有Bias Encoding（偏置编码）的Self-Attention（自我注意力）机制，提取用户的Session兴趣向量；再通过会话间兴趣交互层，利用Bi-LSTM 对用户的Session之间的交互进行建模，提取带有上下文信息的Session兴趣向量；最后在会话兴趣激活层中，利用Activation Unit（局部激活单元）自适应地学习各种会话兴趣对目标item的权重，得到Session兴趣向量和带有上下文信息的Session兴趣向量。

**6.  如果你来设计淘宝定向广告，会有哪些future work（即下一个阶段的idea）？**

答：设计淘宝定向广告时，可以考虑商品流行度的影响，用户由于从众心理，可能会点击流行度高的商品，但这些行为并不能反映用户的“个性化”兴趣。因此，基于Attention机制，在pooling的时候，将用户点击流行度高的商品的行为进行降权，而提高用户对于流行度低的商品的行为的权重，从而更准确的提取用户的兴趣。