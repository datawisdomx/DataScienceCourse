#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:30:22 2021

@author: nitinsinghal
"""
# Chapter 10 - Unsupervised Learning - Clustering
# Density DBSCAN Clustering 

#Import libraries
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics

# Use the data science process steps given in chapter 6 to build the Density DBSCAN Clustering model
# Clustering models being distance based require standardization (scaling) of data

# Import the data
data = pd.read_csv('/Users/nitinsinghal/Dropbox/DataScienceCourse/Data/nbarookie5yrsinleague.csv')

# view top 5 rows for basic EDA
print(data.head())

# Data wrangling to replace NaN with 0, drop duplicate rows
data.fillna(0, inplace=True)
data.drop_duplicates(inplace=True)

# Get the X variables. No need to split into X and y
X = data.iloc[:, [1,3]].values
y = data.iloc[:, -1:].values
y = y.ravel()

# No need to split the data into training and test set as it unsupervised algorithm
# No need to scale the data as different feature scales are used for different clusters

# Using the model fit and predict y values using X 
clustermodel = DBSCAN()
y_pred = clustermodel.fit_predict(X)

# Accuracy metrics
print(metrics.silhouette_score(X, clustermodel.labels_, metric='euclidean'))
print(metrics.adjusted_rand_score(y, y_pred))
print(metrics.homogeneity_score(y, y_pred))
print(metrics.completeness_score(y, y_pred))

# Plot the clusters in 2D
labels = np.unique(clustermodel.labels_)
