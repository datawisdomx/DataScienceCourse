#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:16:03 2021

@author: nitinsinghal
"""
# Chapter 3 - Statistics - Bivariate Analysis
# Correlation and Covariance between US Asset pairs - S&P500 and Nasdaq, S&P500 and Gold

#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

assetdata = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/USAssetMthlyPriceData.csv')

datapair1 = assetdata[['SP500','Nasdaq','Date']]
datapair2 = assetdata[['SP500','Gold','Date']]

# Calculate Correlation and Covariance between S&P500 and Nasdaq
print('Calculating Corrrelation and Covariance between S&P500 and Nasdaq ...')
datapair1Corr = datapair1.corr(method='pearson')
datapair1Cov = datapair1.cov()

# Plot correlation heatmap
print('Plotting correlation, covariance heatmap between S&P500 and Nasdaq ...')
ax = sns.heatmap(datapair1Corr, annot=True, fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

ax = sns.heatmap(datapair1Cov, annot=True, fmt=".2f")
plt.title('Covariance Heatmap')
plt.show()

# Calculate Correlation and Covariance between S&P500 and Gold
print('Calculating Corrrelation and Covariance between S&P500 and Gold ...')
datapair2Corr = datapair2.corr(method='pearson')
datapair2Cov = datapair2.cov()

# Plot correlation heatmap
print('Plotting correlation, covariance heatmap between S&P500 and Gold ...')
ax = sns.heatmap(datapair2Corr, annot=True, fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

ax = sns.heatmap(datapair2Cov, annot=True, fmt=".2f")
plt.title('Covariance Heatmap')
plt.show()


