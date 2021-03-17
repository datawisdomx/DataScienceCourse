#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:57:30 2021

@author: nitinsinghal
"""
# Chapter 7 - Data Wrangling

#Import libraries
import pandas as pd

data = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/DataWranglingSample.csv')

total = data['SP500'] + data['WilshireRE']

print(data.dtypes)

data = data.astype(float)

data['Nasdaq'] = data['Nasdaq'].str.replace(',', '')
data['Nasdaq'] = data['Nasdaq'].str.replace('$', '')
data['Nasdaq'] = pd.to_numeric(data['Nasdaq'])

data['WilshireRE'] = data['WilshireRE'].str.replace('cc', '')
data['WilshireRE'] = pd.to_numeric(data['WilshireRE'])

data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

data.fillna(0, inplace=True)



