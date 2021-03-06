#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 17:33:32 2021

@author: nitinsinghal
"""
    
# Chapter 9 - Supervised Learning - Classification
# Logistic Regression Classifier

#Import libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler #OneHotEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

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
#X = data.iloc[:, 1:-1].values
X = data.iloc[:, [1,3]].values
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

# Create the Logistic regression classifier
classifier = LogisticRegression()

# Fit the classifier to the training data to build the model
classifier.fit(X_train, y_train)

# Using the classifier predict y values using the X test data 
y_pred = classifier.predict(X_test)

# Accuracy metrics
print(classification_report(y_test, y_pred))

# Calculate and plot the confusion matrix for predicted vs test class labels
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()


# Plot the training points as a meshgrid with the decision boundary built using predicted values
cm_bright = ListedColormap(['Red', 'Blue'])
x_min, x_max = X_train[:, 0].min() - .5, X_train[:, 0].max() + .5
y_min, y_max = X_train[:, 1].min() - .5, X_train[:, 1].max() + .5
h = .01  # step size in the mesh
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
# Plot the decision boundary
Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()]) 
# Put the result into a color plot
Z = Z.reshape(xx.shape)
fig, ax = plt.subplots()
ax.contourf(xx, yy, Z, cmap=cm_bright, alpha=.5)
ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors='k')
ax.set_xlim(xx.min(), xx.max())
ax.set_ylim(yy.min(), yy.max())
ax.set_xticks(())
ax.set_yticks(())
plt.title('Training set')
plt.xlabel('GP')
plt.ylabel('PTS')
plt.legend(['Red - 0','Blue - 1'], loc='upper left')
plt.show()

# Plot the testing points
x_min, x_max = X_test[:, 0].min()-.5, X_test[:, 0].max()+.5
y_min, y_max = X_test[:, 1].min()-.5, X_test[:, 1].max()+.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
# Plot the decision boundary
Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()]) 
# Put the result into a color plot
Z = Z.reshape(xx.shape)
fig, ax = plt.subplots()
ax.contourf(xx, yy, Z, cmap=cm_bright, alpha=.5)
ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, edgecolors='k')
ax.set_xlim(xx.min(), xx.max())
ax.set_ylim(yy.min(), yy.max())
ax.set_xticks(())
ax.set_yticks(())
plt.title('Test set')
plt.xlabel('GP')
plt.ylabel('PTS')
plt.legend(['Red - 0','Blue - 1'], loc='upper left')
plt.show()

