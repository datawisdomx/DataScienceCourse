#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 19:16:49 2021

@author: nitinsinghal
"""

# Chapter 10 - Unsupervised Learning - Clustering
# KMeans and Kmeans++ Clustering 

#Import libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt

# Use the data science process steps given in chapter 6 to build the Kmeans++ Clustering model
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

# Plot the Inertia (Within Cluster Sum of Squares) for different no of clusters and 
# different random number for centroid initialization
# Used to identify the elbow of the curve to determine optimal value
# default n_clusters=8, but we can try from 1 to 20 and increase as necessary

for i in (42,50):
    inertia = []
    for j in range(1,10):
        clustermodel = KMeans(init='k-means++', n_clusters=j, n_init=10, max_iter=300, random_state=i).fit(X)
        inertia.append(clustermodel.inertia_)
    fig, ax = plt.subplots()
    ax.plot(range(1,10), inertia)
    plt.title('Inertia(WCSS)- Seed: '+ str(i))
    plt.xlabel('Clusters')
    plt.ylabel('inertia(wcss)')
    plt.tight_layout()
    plt.show()

# Using the model fit and predict y values using X 
clustermodel = KMeans(init='k-means++', n_clusters=2, n_init=10, max_iter=300, random_state=42)
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
plt.xlabel('GP')
plt.ylabel('PTS')
plt.legend()
plt.tight_layout()
plt.show()

# Accuracy metrics
print(metrics.silhouette_score(X, clustermodel.labels_, metric='euclidean'))
print(metrics.adjusted_rand_score(y, y_pred))
print(metrics.homogeneity_score(y, y_pred))
print(metrics.completeness_score(y, y_pred))
