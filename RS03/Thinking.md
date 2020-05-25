## RS03 Thinking
**1.  关联规则中的支持度、置信度和提升度代表的什么，如何计算**

答：支持度代表商品/商品组合出现的频率；其值为某个商品/商品组合出现的次数与总次数之间的比。

​        置信度是指当购买了商品A条件下，购买商品B的概率。

​        提升度lift(A-->B)=P(B|A)/P(B)，代表购买商品A事件对购买商品B的概率的影响，大于1表示有提升，小于1有下降，等于1则无影响。

**2. 关联规则与协同过滤的区别**

答：关联规则是基于transaction，而协同过滤基于用户偏好（评分）；关联规则是计算商品组合的支持度、置信度，也就是Apriori算法，协同过滤计算的是相似度；关联分析没有利用用户的偏好，仅是对购物订单商品进行挖掘。

**3.  为什么我们需要多种推荐算法**

答：推荐问题是一个复杂的问题，可以从商品关联规则、用户偏好、用户行为等多种维度来寻求解决方案，针对不同的应用场景，选择合适的推荐算法或混合多种算法进行推荐，从而得到更好的推荐效果。

**4.  关联规则中的最小支持度、最小置信度该如何确定**

答：是通过实验调试确定的。不同的数据集，最小值支持度差别较大，可能是0.01到0.5之间

可以从高到低输出前20个项集的支持度作为参考；最小置信度可能是0.5到1之间。

**5.  如何通过可视化的方式探索特征之间的相关性**

答：可通过绘制特征间相关系数的热力图来观察。