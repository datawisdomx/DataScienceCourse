#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:01:08 2021

@author: nitinsinghal
"""
# Chapter 3 - Statistics

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Percentile, Percentile Rank
marks = [35,40,28,57,78,63,70,85,92,80,90]
marks.sort()
print(marks)

std_marks = 70

count = 0 
for mark in marks:
    if mark < std_marks:
        count += 1

percentile = round((count/len(marks))*100)
print('Percentile of student is: ', percentile, 'th')
print('Percentile rank of student is: ', percentile)

print(np.percentile(marks, 45))

# Range
x = [1,3,2,5,4,12,9,17,15]
print(max(x)-min(x)) 


# Boxplot for Quartiles
df = pd.DataFrame({'frequency': [1,1,0,0,4,7,10,20,24,35,43,29,13,8,3,0,0,0,1,1]})
print(df.describe())

df.boxplot(grid=False)
plt.show()

