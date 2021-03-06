#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 17:33:32 2021

@author: nitinsinghal
"""
    
# Chapter 9 - Supervised Learning - Classification
# KNN Classifier 

#Import libraries
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler #OneHotEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score

# Use the data science process steps given in chapter 6 to build the KNN model
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

# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Scale (Standardize) the X values as large values can skew the results by giving them higher weights
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create the KNN Classifier 
classifier = KNeighborsClassifier()

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

