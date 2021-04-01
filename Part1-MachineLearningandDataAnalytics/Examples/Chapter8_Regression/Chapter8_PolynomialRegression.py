#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:23:29 2020

@author: nitinsinghal
"""

# Chapter 8 - Supervised Learning - Regression
# Polynomial Regression - Bond Price prediction using Inflation rate for US, using a 3rd order linear algebraic equation

#Import libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Use the data science process steps given in chapter 6 to build the polynomial regression model
# Data being a simple 2 variable numeric set, it requires minimal pre-processing

usInfl10yrpriceyield = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/USInflIR10YrYieldPrice.csv')

# Split the data into dependent y and independent X variables
X = usInfl10yrpriceyield.loc[:, 'us_inflation_rate'].values
y = usInfl10yrpriceyield.loc[:, 'Price'].values

# As X, y are 1 dimensional arrays, and the algorithm expects a 2D array
# We need to reshape the array. This can be done using numpy reshape method 
X = X.reshape(-1,1)
y = y.reshape(-1,1)

# Generate the polynomial feature matrix for X using the given degree (Eg: n=3)
poly = PolynomialFeatures(3)
X_poly = poly.fit_transform(X)

# Store the last X, y values as the validation set
X_validate = X_poly[-1:]
y_validate = y[-1:]

# Remove the last value from the training/test set, so that its not used for training
X_poly = X_poly[:-1]
y = y[:-1] 

# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size = 0.25)

# Create the polynomial regression estimator instance
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
plt.xlim([0, 6])
plt.plot(y_test, color='red', label='Actual values')
plt.plot(y_pred, color='blue', label='Predicted values')
plt.legend()
plt.show()

# Validate the model by predicting the y value for a given X value and see where it lies on the line
y_validate_pred = estimator.predict(X_validate)

print('X validation value: ', X_validate, 'Predicted y validation value: ', y_validate_pred, 'Actual y validation value: ', y_validate)
print('y validation Pred - Actual: ', (y_validate_pred-y_validate), 'y validation diff %: ', ((y_validate_pred-y_validate)/y_validate)*100)

