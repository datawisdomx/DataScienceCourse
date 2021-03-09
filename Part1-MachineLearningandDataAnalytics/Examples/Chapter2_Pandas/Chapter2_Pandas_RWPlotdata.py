#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:52:14 2021

@author: nitinsinghal
"""
# Chapter 2 - Pandas - Data Analysis Library
import pandas as pd

# Read/Write data
macrodata = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/USInflIR10YrYieldPrice.csv')
print(macrodata.head())

df = macrodata[['date','Price']]
df.to_csv('/Users/nitinsinghal/Downloads/pricedata.csv')

macrojson = macrodata.to_json()
print(macrojson)

#Plot data
macro2yrdata = macrodata[(macrodata['date'] < '2000-12-31')]

macro2yrdata.set_index(macro2yrdata['date'], inplace=True)
macro2yrdata.drop(['date'], inplace=True, axis=1)

macro2yrdata.plot.line(subplots=True, figsize=(6,6), legend=True, title='US Macro data')

macro2yrdata.head(12).plot.bar(subplots=False, figsize=(4,4), legend=False, title='US Macro data')

macro2yrdata.drop(['Price'], inplace=True, axis=1)
macro2yrdata.head(12).plot.bar(subplots=False, figsize=(4,4), legend=False, title='US Macro data')

