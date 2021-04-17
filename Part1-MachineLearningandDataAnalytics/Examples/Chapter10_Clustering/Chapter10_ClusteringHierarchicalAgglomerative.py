#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:32:26 2021

@author: nitinsinghal
"""
# Chapter 10 - Unsupervised Learning - Clustering
# Density Hierarchical Clustering 

#Import libraries
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics
import matplotlib.pyplot as plt

# Use the data science process steps given in chapter 6 to build the Hierarchical Clustering model

# Import the data
data = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/nbarookie5yrsinleague.csv')

# view top 5 rows for basic EDA
print(data.head())

# Data wrangling to replace NaN with 0, drop duplicate rows
data.fillna(0, inplace=True)
data.drop_duplicates(inplace=True)

# Get the X variables for training the clustering model.
# The y variables are only used for accuracy metrics, not for training the model
X = data.iloc[:, [1,3]].values
y = data.iloc[:, -1:].values
y = y.ravel()

# No need to split the data into training and test set as it unsupervised algorithm
# No need to scale the data as different feature scales are used for different clusters

# Using the model fit and predict y values using X 
clustermodel = AgglomerativeClustering(n_clusters=2)
y_pred = clustermodel.fit_predict(X)

# Plot the clusters in 2D
labels = np.unique(clustermodel.labels_)
colours = ['red','green','blue','darkorange','cyan','magenta']
fig, ax = plt.subplots()
for i in labels:
    ax.scatter(X[y_pred == i, 0], X[y_pred == i, 1], c=colours[i], label=i)
x_min, x_max = X[:, 0].min()-2, X[:, 0].max()+2
y_min, y_max = X[:, 1].min()-2, X[:, 1].max()+2
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
plt.title('Clustering Hierarchical')
plt.xlabel('GP')
plt.ylabel('PTS')
plt.legend()
plt.tight_layout()
plt.show()

# Accuracy metrics
print('silhouette_score: ', metrics.silhouette_score(X, clustermodel.labels_, metric='euclidean'))
print('adjusted_rand_score: ', metrics.adjusted_rand_score(y, y_pred))
print('homogeneity_score: ', metrics.homogeneity_score(y, y_pred))
print('completeness_score: ', metrics.completeness_score(y, y_pred))

