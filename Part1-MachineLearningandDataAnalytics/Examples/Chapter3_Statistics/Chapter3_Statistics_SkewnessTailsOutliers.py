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

# Distribution - Skewness, Tail, Outliers
# +ve Skew. Right tail
df = pd.DataFrame({'noofpeople' : [35,40,45,40,30,25,15,10,5,3,1,0,0,1],
                   'height': [150,155,160,165,170,175,180,185,190,195,200,205,210,215]})

skewdata = pd.Series()
for j in range(150,220,5):
    bintotal = 0
    for i in range(len(df)):
        if((df.loc[i,'height'] >= j) & (df.loc[i,'height'] < j+5)):
            bintotal += df.loc[i,'noofpeople']
    skewdata.loc[j] = bintotal

plt.title('+ve Skew. Right tail. Outlier')
plt.xlabel('Height Intervals of 5cm (150-220)')
plt.ylabel('Total No of People')
skewdata.plot(kind='bar', position=0, width=0.9, figsize=(4,6))
plt.show()

# -ve Skew. Left tail
df = pd.DataFrame({'noofpeople' : [1,0,0,1,3,5,10,15,25,30,40,45,40,35],
                   'height': [150,155,160,165,170,175,180,185,190,195,200,205,210,215]})

skewdata = pd.Series()
for j in range(150,220,5):
    bintotal = 0
    for i in range(len(df)):
        if((df.loc[i,'height'] >= j) & (df.loc[i,'height'] < j+5)):
            bintotal += df.loc[i,'noofpeople']
    skewdata.loc[j] = bintotal

plt.title('-ve Skew. Left tail. Outlier')
plt.xlabel('Height Intervals of 5cm (150-220)')
plt.ylabel('Total No of People')
skewdata.plot(kind='bar', position=0, width=0.9, figsize=(4,6))
plt.show()
