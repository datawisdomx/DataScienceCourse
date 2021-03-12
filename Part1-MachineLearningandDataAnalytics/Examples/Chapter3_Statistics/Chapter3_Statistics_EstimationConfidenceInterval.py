#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:03:03 2021

@author: nitinsinghal
"""
# Chapter 3 - Statistics

# import libraries
import pandas as pd
import numpy as np


# Inferential Statistics - Estimation
# Point estimates
df = pd.DataFrame({'frequency': [1,1,0,0,4,7,10,20,24,35,43,29,13,8,3,0,0,0,1,1]})
sample = df.sample(10)

samplemean = np.mean(sample)
populationmean = np.mean(df)
error = samplemean - populationmean
print('SampleMean = %.2f, PopulationMean =  %.2f, Error = %.2f' %(samplemean, populationmean, error))

# Population vs Sample Error measures, using multiple random sampless
populationmean = np.mean(df)
error = []

for i in range(5):
    sample = df.sample(10)
    samplemean = np.mean(sample)
    error.append((samplemean - populationmean)**2)

mse = sum(error)/5
print('MSE = %.2f, RMSE = %.2f'%(mse, np.sqrt(mse)))

# Interval estimate - Confidence intervals
x = np.random.randint(0,1000,size=100)

mean = np.mean(x)
stdev = np.std(x)
print('mean: ',mean, 'std dev: ', stdev)

# z-value for 95% CI is 1.96. Different CI z-values can be obtained online
CIp = mean+1.96*(stdev/np.sqrt(100))
CIn = mean-1.96*(stdev/np.sqrt(100))
print('CI-: ',CIn,'CI+: ',CIp)

