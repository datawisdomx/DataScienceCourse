#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 19:05:35 2021

@author: nitinsinghal
"""
# Chapter 10 - Unsupervised Learning - Clustering
# Density GaussianMixture Clustering 

#Import libraries
import pandas as pd
from sklearn.mixture import GaussianMixture 

# Use the data science process steps given in chapter 6 to build the GaussianMixture Clustering model
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
clustermodel = GaussianMixture(n_components=3)
y_pred = clustermodel.fit_predict(X)


