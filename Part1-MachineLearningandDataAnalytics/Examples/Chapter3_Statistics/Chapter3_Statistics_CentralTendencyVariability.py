#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:01:07 2021

@author: nitinsinghal
"""
# Chapter 3 - Statistics

# import libraries
import numpy as np
from statistics import mode

# Central tendency - Mean, Median, Mode. 
x = [1,	3,	2,	5,	4,	12,	9,	5, 17,	3, 15, 5]
mean = sum(x)/len(x)
print('mean = %.2f' %(mean))
print('mean = %.2f' %(np.mean(x)))
print('median = %.2f' %(np.median(x)))
print('mode = %.2f' %(mode(x)))

# Variability - Variance, Standard Deviation
varsum = 0
for i in range(len(x)):
    varsum += (x[i]-mean)**2
var = varsum/len(x)

print('variance = %.2f' %(var))
print('standard deviation = %.2f' %(np.sqrt(var)))
print('variance = %.2f' %(np.var(x)))
print('standard deviation = %.2f' %(np.std(x)))
print('variance with bessel correction = %.2f' %(np.var(x, ddof=1)))
print('standard deviation with bessel correction = %.2f' %(np.std(x, ddof=1)))
