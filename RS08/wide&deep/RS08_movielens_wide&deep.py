# -*- coding: utf-8 -*-
"""
* Content：使用Wide&Deep模型对movielens进行评分预测
* Author:  HuiHui
* Date:    2020-03-18
* Reference:
* movieslens/movielens_sample数据集：包含多个用户对多部电影的评级数据，也包括电影元数据信息和用户属性信息。
    * userId: 每个用户的id
    * movieId: 每部电影的id
    * rating: 用户评分，是5星制，按半颗星的规模递增(0.5 stars - 5 stars)
    * timestamp: 自1970年1月1日零点后到用户提交评价的时间的秒数
    * 其他：title,genres,gender,age,occupation,zip
    * 数据排序的顺序按照userId，movieId排列的。
"""

import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from deepctr.models import WDL
from deepctr.inputs import SparseFeat, get_feature_names


# 数据读取

# #movielens_sample数据集
# data = pd.read_csv("./movielens_sample.txt")
# sparse_features = ["movie_id", "user_id", "gender", "age", "occupation", "zip"]
# target = ['rating']

# movielens完整数据集
ratings = pd.read_csv("./movielens/ratings.csv")
movies = pd.read_csv("./movielens/movies.csv")
data = pd.merge(ratings,movies,on='movieId')
sparse_features = ["movieId","userId", "genres","title"]
target = ["rating"]

print(data[target])

# 对特征标签进行编码
for feature in sparse_features:
    lbe = LabelEncoder()#将离散型的数据转换成 0 到 n−1 之间的数
    data[feature] = lbe.fit_transform(data[feature])

# 计算每个特征中的不同特征值的个数
fixlen_feature_columns = [SparseFeat(feature, data[feature].nunique()) for feature in sparse_features] #embedding
linear_feature_columns = fixlen_feature_columns
dnn_feature_columns = fixlen_feature_columns
feature_names = get_feature_names(linear_feature_columns + dnn_feature_columns)

# 将数据集切分成训练集和测试集
train, test = train_test_split(data, test_size=0.2)
train_model_input = {name:train[name].values for name in feature_names} #dict
test_model_input = {name:test[name].values for name in feature_names}

# 使用Wide&Deep进行训练
model = WDL(linear_feature_columns, dnn_feature_columns, task='regression')
model.compile("adam", "mse", metrics=['mse'], )
history = model.fit(train_model_input, train[target].values, batch_size=256, epochs=1, verbose=True, validation_split=0.2, )
# 使用Wide&Deep进行预测
pred_ans = model.predict(test_model_input, batch_size=256)
# 输出RMSE或MSE
mse = round(mean_squared_error(test[target].values, pred_ans), 4)
rmse = mse ** 0.5
print("test RMSE", rmse)
