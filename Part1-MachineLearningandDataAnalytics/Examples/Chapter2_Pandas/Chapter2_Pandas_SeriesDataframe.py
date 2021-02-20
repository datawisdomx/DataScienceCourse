#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:47:15 2021

@author: nitinsinghal
"""
# Chapter 2 - Pandas - Data Analysis Library
import pandas as pd
import numpy as np

#Series
s = pd.Series([1,2,5,11,16,23])
print(s)
print('s[0] is: ',s[0])
print(s/2)
print(s*s)

si = pd.Series([-11, -8, -5, -2, 1, 4, 7, 10], index=['a', 'b,', 'c','d','e','f','g','h'])
print(si)
print(si[0])
print('si[a] is: ',si['a'])
print('si std dev is: ', np.std(si))

dictionary = {'a':3,'b':'balls','c':7.21,'d':'price','e':'2/9/18'} 
sd = pd.Series(dictionary)
print(sd)

#DataFrame
d = {'item': ['a','b','c','d','e','f'],
     'price': [10, 25, 33.43, 51.2, 9, np.nan],
     'quantity': [48, 12, 7, 3, 80, 100]}
df = pd.DataFrame(d)
print(df)
print(df['price']*10)
df['value'] = df['price']*df['quantity']
print(df)
