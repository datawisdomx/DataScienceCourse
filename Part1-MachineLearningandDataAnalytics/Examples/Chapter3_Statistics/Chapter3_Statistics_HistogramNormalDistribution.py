#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:01:07 2021

@author: nitinsinghal
"""
# Chapter 3 - Statistics

# import libraries
import pandas as pd
import matplotlib.pyplot as plt

# Histogram
df = pd.DataFrame({'students' : [1,	3,	2,	5,	4,	12,	9,	17,	15,	11,	4,	10,	4,	2,	1], 
                   'marks' : [9, 21,	30,	40,	45,	50,	55,	60,	65,	70,	75,	80,	85,	90,	95]})

histdata = pd.DataFrame(columns=['bins','frequency'])

for j in range(10):  
    bintotal = 0
    for i in range(len(df)):
        if((df.loc[i,'marks'] >= j*10) & (df.loc[i,'marks'] < (j*10)+10)):
            bintotal += df.loc[i,'students']
    histdata.loc[j, 'frequency'] = bintotal
    histdata.loc[j, 'bins'] = j*10

histdata.plot.bar(x='bins', y='frequency', rot=0, position=0, width=0.9, title='Total No of Students in intervals of 10 Marks',
                  xlabel='Intervals of 10 Marks (0-100)', ylabel='Total No of Students')

# Normal distribution
df = pd.DataFrame({'noofpeople' : [10,20,30,40,50,60,50,40,30,20,10],
                   'height': [150,155,160,165,170,175,180,185,190,195,200]})

normaldata = pd.Series()
for j in range(150,205,5):
    bintotal = 0
    for i in range(len(df)):
        if((df.loc[i,'height'] >= j) & (df.loc[i,'height'] < j+5)):
            bintotal += df.loc[i,'noofpeople']
    normaldata.loc[j] = bintotal

plt.title('Normal Distribution - Total No of People in Height intervals')
plt.xlabel('Height Intervals of 5cm (150-220)')
plt.ylabel('Total No of People')
normaldata.plot(kind='bar', position=0, width=0.9, figsize=(4,6))
plt.show()

