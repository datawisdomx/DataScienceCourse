#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 09:48:05 2021

@author: nitinsinghal
"""
# Chapter 11 - Model Persistence Load and predict

#Import libraries
import pandas as pd
from joblib import load

# Load the model file for use in prediction
model = load('/Users/nitinsinghal/Dropbox/DataScienceCourse/Data/RFRegression.model')

# Load the new data for predicting using the model file
usmacro10yrpriceyielddata = pd.read_csv('/Users/nitinsinghal/Dropbox/DataScienceCourse/Data/USMacro10yrPriceYield.csv')

# Get the data row for predicting and comparing
X = usmacro10yrpriceyielddata.iloc[221:222, 1:7].values
y_new = usmacro10yrpriceyielddata.iloc[221:222, 7].values
y_pred = model.predict(X)

# Print the result of the prediction for y and compare to actual y value
print('Actual y value: ', y_new, 'Predicted y value: ', y_pred, 'y Pred - Actual %diff: ', (((y_pred-y_new)/y_new)*100))

