#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:47:15 2021

@author: nitinsinghal
"""
# Chapter 2 - Pandas - Data Analysis Library
import pandas as pd
import numpy as np

#Casting, conversion
IndexPrice = pd.DataFrame({'date':['26/11/2019','27/11/2019','29/11/2019','02/12/2019','03/12/2019','04/12/2019'], 	
                           'price':['3134','3145','3147','3143','3087','3103']})
print(IndexPrice.dtypes)

price = IndexPrice['price'].astype('int32')
print(price.dtypes)

IndexPrice['price'] = pd.to_numeric(IndexPrice['price'])
IndexPrice['date'] = pd.to_datetime(IndexPrice['date'], format='%d/%m/%Y')
print(IndexPrice.dtypes)

# Groupby, Aggregate 
IndexPrice['date'] = pd.to_datetime(IndexPrice['date'], format='%d/%m/%Y').dt.to_period('M')
pricegroup = IndexPrice.groupby(['date'])
print(pricegroup.dtypes)

pricegroupmean = pricegroup.mean()
print(pricegroupmean)

pricestats = IndexPrice.groupby(['date']).agg([np.mean,np.std,np.var])
print(pricestats)

