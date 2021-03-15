#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 17:35:10 2021

@author: nitinsinghal
"""

# Chapter 4 - Probability

import pandas as pd
import random

#Central Limit Theorem
# 0 - Head, 1 - Tail
n = [10,100,1000,10000,100000,1000000]
for j in range(len(n)):
    result = []
    for i in range(n[j]):
        toss = random.choice([0,1])
        result.append(toss)
    print(' tosses - ',n[j], ', Head% :', result.count(0)/n[j], ', Tails% :', result.count(1)/n[j])

# PMF - Probability Mass Function
df = pd.DataFrame({'students' : [1,	3,	2,	5,	4,	12,	9,	17,	15,	11,	4,	10,	4,	2,	1], 
                   'marks' : [9, 21,	30,	40,	45,	50,	55,	60,	65,	70,	75,	80,	85,	90,	95]})

df['students'] = df['students']/df['students'].sum()

histdata = pd.DataFrame(columns=['bins','probability'])

for j in range(10):  
    bintotal = 0
    for i in range(len(df)):
        if((df.loc[i,'marks'] >= j*10) & (df.loc[i,'marks'] < (j*10)+10)):
            bintotal += df.loc[i,'students']
    histdata.loc[j, 'probability'] = bintotal
    histdata.loc[j, 'bins'] = j*10

histdata.plot.bar(x='bins', y='probability', rot=0, position=0, width=0.9, title='Probability Mass Function of Students in intervals of 10 Marks',
                  xlabel='Intervals of 10 Marks (0-100)', ylabel='Probability of Students')
