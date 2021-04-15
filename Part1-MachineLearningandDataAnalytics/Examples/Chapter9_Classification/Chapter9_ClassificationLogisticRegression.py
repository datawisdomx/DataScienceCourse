#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:12:15 2021

@author: nitinsinghal
"""

# Chapter 9 - Supervised Learning - Classification
# Logistic Regression Classifier

#Import libraries
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler #OneHotEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score

# Use the data science process steps given in chapter 6 to build the Logistic Regression model
# Classification models being distance based require standardization (scaling) of data

# Import the data
data = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/nbarookie5yrsinleague.csv')
# view top 5 rows for basic EDA
print(data.head())

# Data wrangling to replace NaN with 0, drop duplicate rows
data.fillna(0, inplace=True)
data.drop_duplicates(inplace=True)

# Split the data into depdendent y and independent X variables
X = data.iloc[:, 1:-1].values
y = data.iloc[:, -1:].values

# As y is a column vector and the algorithm expects a 1D array (n,)
# we need to reshape the array using ravel()
y = y.ravel()

# Encode the catgorical data (text or non-numeric data needs to be converted into a binary matrix of ‘n’ categories)
# encoder = OneHotEncoder(drop='first', sparse=False, handle_unknown='error')
# X_encoded = encoder.fit_transform(X)

# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Scale (Standardize) the X values as large values can skew the results by giving them higher weights
# As most estimators expect the data to be normally distributed (mean 0 variance =1)
# Fit the scaler to the training data and and transform it using the calculated mean and variance 
# No need to fit the test data as it should use the same mean and variance as the test data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create the Logistic regression classifier
classifier = LogisticRegression()

# Fit the classifier to the training data to build the model
classifier.fit(X_train, y_train)

# Using the classifier predict y values using the X test data 
y_pred = classifier.predict(X_test)

# Accuracy score
print('accuracy_score: ', accuracy_score(y_test, y_pred))
    
# Accuracy metrics
# The F-1 score is the weighted harmonic mean of the precision and recall, best value at 1 and worst score at 0.
# The support is the number of occurrences of each class in y_test
print('classification_report: \n', classification_report(y_test, y_pred))

# Calculate and plot the confusion matrix for predicted vs test class labels
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
