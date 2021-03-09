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
print(df.dtypes)
print(df.index)
print(df.columns)
print(df.axes)

print(df.head(3))
print(df.tail(4))
df1 = df.copy()
print(df1)

#Indexing/Slicing
df.loc[:,'value']
df.iloc[2, 3]
df[2:]
df[['quantity', 'value']]

# conditional operations
print(df[df['price'] > 10])
print(df[df['quantity'].isin([7])])

df.loc[6,'item'] = 'g'
df.iloc[6,1] = 70
df.iloc[6,2] = 20
df.loc[6,'value'] = 70*20
print(df)

# Apply Function
df['price'] = df['price'].apply(lambda a: a*10)
print(df)

# Using axis. 0 means index or rows, 1 means columns.
print(df.sum(axis=0))


