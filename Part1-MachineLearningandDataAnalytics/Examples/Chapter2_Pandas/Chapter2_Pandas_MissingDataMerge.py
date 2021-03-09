#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:15:07 2021

@author: nitinsinghal
"""
# Chapter 2 - Pandas - Data Analysis Library
# Missing data, Merge

import pandas as pd
import numpy as np

#Missing data
d = {'item': ['a','b','c','d','e','f'],
     'price': [10, 25, 33.43, 51.2, 9, np.nan],
     'quantity': [48, 12, 7, 3, 80, 100]}
df = pd.DataFrame(d)

df.fillna(value=20, inplace=True)
print(df)

df.fillna(df.mean(), inplace=True)
print(df)

df.dropna(inplace=True)
print(df)

df.loc[1,'quantity'] = np.nan
df.loc[4,'quantity'] = np.nan
print(df)

df.fillna(method='bfill', inplace=True)
print(df)

df.fillna(method='ffill', inplace=True)
print(df)

#Merge
df1 = pd.DataFrame({'item': ['a','b','c','d','e'], 'price': [1,2,3,4,5]})
df2 = pd.DataFrame({'item': ['b','d','e','f','g'], 'price': [6,7,8,9,10]})
df3 = pd.DataFrame({'item': ['a','h','i'], 'price': [11,12,13]})

df4 = pd.concat([df1,df2, df3], join='inner', ignore_index=False)
print(df4)

df5 = pd.merge(df1, df2, on='item', how='outer')
print(df5)
