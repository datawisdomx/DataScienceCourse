#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:01:08 2021

@author: nitinsinghal
"""
# Chapter 3 - Statistics

# import libraries
import pandas as pd
import matplotlib.pyplot as plt

# Percentile, Percentile Rank
marks = [35,40,28,57,78,63,70,85,92,80,90]
std_marks = 70
marks.sort()
count = 0 
for mark in marks:
    if mark <= std_marks:
        count += 1

percentile_rank = round((count/len(marks))*100)
print('Percentile Rank of student is: ', percentile_rank)

# Boxplot for Quartiles
df = pd.DataFrame({'frequency': [1,1,0,0,4,7,10,20,24,35,43,29,13,8,3,0,0,0,1,1]})
print(df.describe())
df.boxplot(grid=False)
plt.show()
