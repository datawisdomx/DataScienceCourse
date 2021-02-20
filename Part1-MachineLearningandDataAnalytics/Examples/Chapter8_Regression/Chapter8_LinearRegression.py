#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:23:29 2020

@author: nitinsinghal
"""

# Chapter 8 - Supervised Learning - Regression
# Linear Regression - Interest rate and Inflation

#Import libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Use the data science process steps given in chapter 6 to build the linear regression model
# Data being a simple 2 variable numeric set, it requires minimal pre-processing

# Import inflation, interest rate and 10 yr bond data for US

usInfl10yrpriceyield = pd.read_csv('/Users/nitinsinghal/Dropbox/DataScienceCourse/Data/USInflIR10YrYieldPrice.csv')

# Split the data into depdendent y and independent X variables
X = usInfl10yrpriceyield.loc[:, 'us_inflation_rate'].values
y = usInfl10yrpriceyield.loc[:, 'Price'].values

# As X, y are 1 dimensional arrays, and the algorithm expects a 2D array
# We need to reshape the array. This can be done using numpy reshape method 
X = X.reshape(-1,1)
y = y.reshape(-1,1)

# Scale (Standardize) the X values as large values can skew the results by giving them higher weights
# As most estimators expect the data to be normally distributed (mean 0 variance =1)
# scaler = StandardScaler()
# Fit the scaler to the training data and and transform it using the calculated mean and variance 
# X_train = scaler.fit_transform(X_train)
# No need to fit the test data as it should use the same mean and variance as the test data
# X_test = scaler.transform(X_test)

# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .25)

# Create the linear regression estimator instance
estimator = LinearRegression()

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
plt.xlim([0, 7])
plt.plot(y_test, color='red', label='Actual values')
plt.plot(y_pred, color='blue', label='Predicted values')
plt.legend()
plt.show()

# Plot the best fit linear regression line for the test data
plt.title('Scatter Plot Regression Line us_inflation_rate vs 10yr Bond Price')
plt.xlabel('us_inflation_rate')
plt.ylabel('10yr Bond Price')
plt.scatter(X_test, y_test,  color='blue')
plt.plot(X_test, y_pred, color='red', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

# Validate the model by predicting the y value for a given X value and see where it lies on the line

y_actual = y[222]
x_actual = X[222]

X_validate = np.array(x_actual).reshape(-1,1)
y_validate = estimator.predict(X_validate)

print('X value: ', X_validate, 'Predicted y value: ', y_validate, 'Actual y value: ', y_actual, 
      'y Pred - Actual: ', (y_validate-y_actual), 'y diff %: ', ((y_validate-y_actual)/y_validate)*100)

