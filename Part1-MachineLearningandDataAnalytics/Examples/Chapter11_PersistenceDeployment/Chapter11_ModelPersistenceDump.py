#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 09:46:04 2021

@author: nitinsinghal
"""

# Chapter 11 - Model Persistence Dump
# Random Forest Regression - Interest rate and other macroeconomic data for US

#Import libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from joblib import dump

# Import inflation and interest rate data for US
usmacro10yrpriceyielddata = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/USMacro10yrPriceYield.csv')

# Split the data into depdendent y and independent X variables
X = usmacro10yrpriceyielddata.iloc[:, 1:7].values
y = usmacro10yrpriceyielddata.iloc[:, 7].values

# As y is a 1 dimensional array, and the algorithm expects a 2D array
# we need to reshape the array. Using numpy reshape method this can be done easily
y = y.reshape(-1,1)

# Remove the last value from the training/test set, so that its not used for training
X = X[:-1]
y =y[:-1]

# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Create the random forest regressor
estimator = RandomForestRegressor(n_estimators=100, criterion='mse', min_samples_leaf=1, min_samples_split=2, 
                                            max_features='auto', random_state=42, n_jobs=-1)

# Fit the estimator to the training data to build the model
estimator.fit(X_train, y_train)

# Using the estimator predict y values using the X test data 
y_pred = estimator.predict(X_test)

# Calculate error metrics for predicted y values vs y test data
mse = mean_squared_error(y_test , y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test , y_pred)
r2 = r2_score(y_test , y_pred)
print('MSE:%.4f, RMSE:%.4f, MAE:%.4f, R2:%.4f' %(mse, rmse, mae, r2))
plt.title('Linear Regression - us_inflation_rate vs 10yr Bond Price')
plt.xlabel('us_inflation_rate')
plt.ylabel('10yr Bond Price')
plt.ylim([90, 140])
plt.xlim([0, 6])
plt.plot(y_test, color='red', label='Actual values')
plt.plot(y_pred, color='blue', label='Predicted values')
plt.legend()
plt.show()

#Feature Importance
rfimp = estimator.feature_importances_
featimp = pd.DataFrame(rfimp)
featimp = featimp.rename({0:'FeatImp'}, axis='columns')
featimp.index = usmacro10yrpriceyielddata.columns[1:7]
featimp = featimp.sort_values(by=['FeatImp'])
featimp.plot(kind='bar')

# Save the model file for production deployment
model_location = '/Users/nitinsinghal/Downloads/RFRegression.model'
dump(estimator, model_location)
