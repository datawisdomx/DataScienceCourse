#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 18:14:00 2021

@author: nitinsinghal
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/RegressionData.csv')

X = data.loc[:, 'X'].values
y = data.loc[:, 'Y'].values

X = X.reshape(-1,1)
y = y.reshape(-1,1)

estimator = LinearRegression()
estimator.fit(X, y)

y_pred = estimator.predict(X)

plt.title('Scatter Plot and Regression Line US Inflation vs Interest Rate')
plt.xlabel('US Inflation')
plt.ylabel('Interest Rate')
plt.scatter(X, y,  color='blue')
plt.plot(X, y_pred, color='red', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

print('R2: ', estimator.score(X, y))
