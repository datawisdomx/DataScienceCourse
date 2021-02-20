#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:47:16 2021

@author: nitinsinghal
"""
# Chapter 2 - Pandas - Data Analysis Library
import pandas as pd

#Text data - String
sa = pd.Series(['   Test','this SAMPLE','series  '], dtype='string')
sb = pd.Series(['Concat','to','series a'],dtype='string')

print(sa)
print(sa.str.get(0))
print(sa.str.len())
print(sa.str.strip())
print(sa.str.split(' '))
print(sa.str.lower())
print(sa.str.upper())
print(sa.str.replace('t','z'))
print(sa.str.cat(sep=','))
print(pd.concat([sa,sb], ignore_index=True))

#Iteration, Key Value
s = pd.Series([1,2,3,5,7])
for i in range(len(s)):
    print(s[i])
df = pd.DataFrame({'item': ['a','h','i'], 'price': [11,12,13]})
for key, value in df.items():
    print(key)
    print(value)
for key, value in df.iterrows():
    print(key)
    print(value)

#Sorting
df = pd.DataFrame({'item': ['j','c','n','q'], 'price': [19,7,41,3]})
print(df)
pricesort = df.sort_values(by='price')
print(pricesort)
priceidxsrt = pricesort.sort_index()
print(priceidxsrt)
