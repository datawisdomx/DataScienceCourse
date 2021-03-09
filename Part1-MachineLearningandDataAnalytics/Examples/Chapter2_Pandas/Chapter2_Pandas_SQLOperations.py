#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:25:47 2021

@author: nitinsinghal
"""
# Chapter 2 - Pandas - Data Analysis Library
import pandas as pd

# SQL operations
df1 = pd.DataFrame({'item': ['a','b','c','d','e'],
     'price': [10, 25, 33, 51, 9],
     'quantity': [48, 12, 7, 3, 80]})
df2 = pd.DataFrame({'item': ['b','d','f','g'], 
                    'price': [60,70,80,90],
                    'quantity': [10,20,30,40]})

#Calculate and print value for each item. value = price * quantity 
#SELECT item, price * quantity as value FROM df1;
df1['value'] = df1['price']*df1['quantity'] 
print(df1)

#Select items where price>20 and quantity<10
#SELECT * FROM df1 WHERE price>20 AND quantity<10 ;
print(df1[(df1['price']>20) & (df1['quantity']<10)])

#Select items with lowest 3 prices
#SELECT * FROM df1 ORDER BY price ASC LIMIT 3;
print(df1.sort_values(by='price').head(3))

#Left Join two tables on item. 
#SELECT * FROM df1 LEFT JOIN df2 ON df1.item = df2.item;
dfmerged = pd.merge(df1, df2, on='item', how='left')
print(dfmerged)

#Right Join two tables on item. 
#SELECT * FROM df1 Right JOIN df2 ON df1.item = df2.item;
dfmerged = pd.merge(df1, df2, on='item', how='right')
print(dfmerged)

