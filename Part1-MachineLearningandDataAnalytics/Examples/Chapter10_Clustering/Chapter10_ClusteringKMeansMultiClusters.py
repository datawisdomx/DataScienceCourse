#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 10:28:03 2021

@author: nitinsinghal
"""

# Chapter 10 - Unsupervised Learning - Clustering
# KMeans and Kmeans++ Multi Clustering 

#Import libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt

# Use the data science process steps given in chapter 6 to build the Kmeans++ Clustering model
# Import the data
data = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/kaggletortuga_techstudentcategory.csv')

# From the original raw data categories
# beginner_front_end	   0
# beginner_backend	   1
# advanced_front_end	   2
# advanced_backend	   3
# beginner_data_science	4
# advanced_data_science	5

# view top 5 rows for basic EDA
print(data.head())

# Data wrangling to replace NaN with 0, drop duplicate rows
data.fillna(0, inplace=True)
data.drop_duplicates(inplace=True)

# Get the X variables for training the multi clustering model.
# The y variables are only used for accuracy metrics, not for training the model
X = data.iloc[:, 3:-1].values
y = data.iloc[:, -1:].values
y = y.ravel()

# No need to split the data into training and test set as it unsupervised algorithm
# No need to scale the data as different feature scales are used for different clusters

# Plot the Inertia (Within Cluster Sum of Squares) for different no of clusters and 
# different random number for centroid initialization
# Used to identify the elbow of the curve to determine optimal value
# default n_clusters=8, but we can try from 1 to 10 and increase as necessary

for i in (42,50):
    inertia = []
    for j in range(1,20):
        clustermodel = KMeans(init='k-means++', n_clusters=j, n_init=10, max_iter=300, random_state=i).fit(X)
        inertia.append(clustermodel.inertia_)
    fig, ax = plt.subplots()
    ax.plot(range(1,20), inertia)
    plt.title('Inertia(WCSS)- Seed: '+ str(i))
    plt.xlabel('Clusters')
    plt.ylabel('inertia(wcss)')
    plt.tight_layout()
    plt.show()

# Using the model fit and predict y values using X 
clustermodel = KMeans(init='k-means++', n_clusters=6, n_init=10, max_iter=300, random_state=42)
y_pred = clustermodel.fit_predict(X)

# Plot the trained model clusters in 2D
labels = np.unique(clustermodel.labels_)
colours = ['red','green','blue','darkorange','cyan','magenta']
fig, ax = plt.subplots()
for i in labels:
    ax.scatter(X[y_pred == i, 0], X[y_pred == i, 1], c=colours[i], label=i)
ax.scatter(clustermodel.cluster_centers_[:,0],clustermodel.cluster_centers_[:,1],s=100,color='black',label='Centroid')
x_min, x_max = X[:, 0].min()-2, X[:, 0].max()+2
y_min, y_max = X[:, 1].min()-2, X[:, 1].max()+2
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
plt.title('Clustering KMeans++ (Training Set)')
plt.xlabel('X[0] - DS Hours Studied')
plt.ylabel('X[1] - BE Hours Studied')
plt.legend()
plt.tight_layout()
plt.show()

# Accuracy metrics
print('silhouette_score: ', metrics.silhouette_score(X, clustermodel.labels_, metric='euclidean'))
print('adjusted_rand_score: ', metrics.adjusted_rand_score(y, y_pred))
print('homogeneity_score: ', metrics.homogeneity_score(y, y_pred))
print('completeness_score: ', metrics.completeness_score(y, y_pred))

# Predict for a new sample dataset to see accuracy of predictions
testdata = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/kaggletortuga_techstudentcategory_tobescored.csv')
print(testdata.head())

testdata.fillna(0, inplace=True)
testdata.drop_duplicates(inplace=True)

X_test = testdata.iloc[:, 3:-1].values

y_testpred = clustermodel.fit_predict(X_test)

# Plot the test values clusters in 2D using trained model 
labels = np.unique(clustermodel.labels_)
colours = ['red','green','blue','darkorange','cyan','magenta']
fig, ax = plt.subplots()
for i in labels:
    ax.scatter(X_test[y_testpred == i, 0], X_test[y_testpred == i, 1], c=colours[i], label=i)
ax.scatter(clustermodel.cluster_centers_[:,0],clustermodel.cluster_centers_[:,1],s=100,color='black',label='Centroid')
x_min, x_max = X_test[:, 0].min()-2, X_test[:, 0].max()+2
y_min, y_max = X_test[:, 1].min()-2, X_test[:, 1].max()+2
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
plt.title('Clustering KMeans++ (Test Set)')
plt.xlabel('X[0] - DS Hours Studied')
plt.ylabel('X[1] - BE Hours Studied')
plt.legend()
plt.tight_layout()
plt.show()

