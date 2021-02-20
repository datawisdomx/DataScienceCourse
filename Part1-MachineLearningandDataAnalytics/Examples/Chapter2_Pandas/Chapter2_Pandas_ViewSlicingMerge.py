#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:47:15 2021

@author: nitinsinghal
"""
# Chapter 2 - Pandas - Data Analysis Library
import pandas as pd
import numpy as np

d = {'item': ['a','b','c','d','e','f'],
     'price': [10, 25, 33.43, 51.2, 9, np.nan],
     'quantity': [48, 12, 7, 3, 80, 100]}
df = pd.DataFrame(d)
df['value'] = df['price']*df['quantity']
print(df)

#View
print(df.index)
print(df.columns)
print(df.dtypes)
print(df.head(3))
print(df.tail(4))
df1 = df.copy()
print(df1)

#Indexing/Slicing
df.loc[:,'value']
df.iloc[2, 3]
df[2:]
df[df['price'] > 10]
df[['quantity', 'value']]
df[df['quantity'].isin([7])]

df['price'].apply(lambda a: a*10)
df.sum(axis=0)

#Missing data
df.dropna()
df.fillna(value=20)
df.fillna(df.mean())
df.loc[1,'quantity'] = np.nan
df.loc[4,'quantity'] = np.nan
print(df)
df.fillna(method='bfill')
df.fillna(method='ffill')
print(df)

#Merge
df1 = pd.DataFrame({'item': ['a','b','c','d','e'], 'price': [1,2,3,4,5]})
df2 = pd.DataFrame({'item': ['b','d','e','f','g'], 'price': [6,7,8,9,10]})
df3 = pd.DataFrame({'item': ['a','h','i'], 'price': [11,12,13]})

pd.concat([df1,df2, df3], join='inner', ignore_index=True)
pd.merge(df1, df2, on='item', how='outer')
