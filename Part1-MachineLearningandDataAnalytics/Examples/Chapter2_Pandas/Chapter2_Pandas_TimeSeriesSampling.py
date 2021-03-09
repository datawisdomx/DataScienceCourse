#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:22:52 2021

@author: nitinsinghal
"""
# Chapter 2 - Pandas - Data Analysis Library
import pandas as pd

#Time series, resample, rolling

timeseriesdfd = pd.DataFrame(pd.date_range('2019-10-01', periods=5, freq='D'))
print(timeseriesdfd)

timeseriesdfm = pd.DataFrame(pd.date_range('2019-10-01', periods=5, freq='M'))
print(timeseriesdfm)

lastday = timeseriesdfd.tail(1)
print(lastday)

print(lastday + pd.Timedelta(days=1))

print(lastday + pd.offsets.BDay())

IndexPrice = pd.DataFrame({'date':['27/3/2019','28/3/2019','29/3/2019','1/4/2019','2/4/2019','3/4/2019','4/4/2019'], 	
                           'price':['10000','10100','10200','10500','9900','9500', '9000']})
IndexPrice['price'] = pd.to_numeric(IndexPrice['price'])
IndexPrice['date'] = pd.to_datetime(IndexPrice['date'], format='%d/%m/%Y')

IndexPrice.set_index(pd.DatetimeIndex(IndexPrice['date']), inplace=True)
IndexPrice.drop(['date'],inplace=True, axis=1)
pricemean = IndexPrice.resample('M').mean()
print(pricemean)

pricemovingavg = IndexPrice.rolling(window=3).mean()
print(pricemovingavg)


