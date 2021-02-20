#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:16:03 2021

@author: nitinsinghal
"""
# Chapter 3 - Statistics - Bivariate Analysis
# Correlation, Covariance, R2 - between US Stock indices, Bond, Oil, Gold, Real estate and Macro data

#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import os
os.chdir('/Users/nitinsinghal/Dropbox/DataScienceCourse/RoboadvisorData/')

# Format date coumn for each dataframe
def data_formatting(df):
    df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df.sort_values(by=['Date']).reset_index(drop=True, inplace=True)
    return df

# Use the high price from each asset dataframe. Remove ',', '-' characters
def data_cleaning(asset):
    df = asset[['Date','High']]
    if(df['High'].dtype.kind == 'O'):
        df['High'] = df['High'].str.replace('-', '')
        df['High'] = pd.to_numeric(df['High'].str.replace(',', ''))
    return df
    

# LOAD asset and Macro DATA for US
print('Loading asset data ...')

# Asset data
Nasdaqdata = pd.read_csv('Nasdaq.csv')
SP500data = pd.read_csv('SP500.csv')
OilWTIdata = pd.read_csv('OilWTI.csv')
Golddata = pd.read_csv('Gold.csv')
WilshireREdata = pd.read_csv('WilshireREPriceIndex.csv')
US10YrYielddata = pd.read_csv('US10YrYield.csv')
UST10YrPriceddata = pd.read_csv('UST10YrPrice.csv')
USMacrodata = pd.read_csv('USMacrodata.csv')

# DATA WRANGLING - CLEANING, FORMATTING
#Use High price instead of Close as it gives higher range to predict
print('Performing Data Wrangling of Asset Data(Formatting, Cleaning) ...')

Nasdaq = data_cleaning(data_formatting(Nasdaqdata))
Nasdaq = Nasdaq.rename({'High':'Nasdaq'}, axis='columns')
SP500 = data_cleaning(data_formatting(SP500data))
SP500 = SP500.rename({'High':'SP500'}, axis='columns')
OilWTI = data_cleaning(data_formatting(OilWTIdata))
OilWTI = OilWTI.rename({'High':'OilWTI'}, axis='columns')
Gold = data_cleaning(data_formatting(Golddata))
Gold = Gold.rename({'High':'Gold'}, axis='columns')
US10YrYield = data_cleaning(data_formatting(US10YrYielddata))
US10YrYield = US10YrYield.rename({'High':'US10YrYield'}, axis='columns')
UST10YrPrice = data_cleaning(data_formatting(UST10YrPriceddata))
UST10YrPrice = UST10YrPrice.rename({'High':'UST10YrPrice'}, axis='columns')

WilshireREdata = WilshireREdata[~WilshireREdata['High'].str.startswith('.')]
WilshireREdata.reset_index(drop=True, inplace=True)
WilshireRE = data_cleaning(data_formatting(WilshireREdata))
WilshireRE = WilshireRE.rename({'High':'WilshireRE'}, axis='columns')

# Merge Bond Price and Yield into one dataframe for countries
USBondYieldPrice = pd.merge(US10YrYield, UST10YrPrice, how='left', on='Date')
USBondYieldPrice = USBondYieldPrice[(USBondYieldPrice['Date'] > '1998-12-31')]
USBondYieldPrice.drop_duplicates(subset='Date', keep='first', inplace=True)
USBondYieldPrice = USBondYieldPrice[~USBondYieldPrice.eq(0).any(1)]
USBondYieldPrice.reset_index(drop=True, inplace=True)
USBondYieldPrice.fillna(0, inplace=True)

# DATA WRANGLING - MERGING
# Merge all asset price data
print('Merging all asset data ...')

MergedAssetdata = pd.merge(SP500, Nasdaq, how='left', on='Date')
MergedAssetdata = pd.merge(MergedAssetdata, WilshireRE, how='left', on='Date')
MergedAssetdata = pd.merge(MergedAssetdata, Gold, how='left', on='Date')
MergedAssetdata = pd.merge(MergedAssetdata, OilWTI, how='left', on='Date')
MergedAssetdata = MergedAssetdata.fillna(0)

# Resample daily to monthly price using mean
indexdata = MergedAssetdata
indexdata.set_index(pd.DatetimeIndex(indexdata['Date']), inplace=True)
indexdata.drop(['Date'],inplace=True, axis=1)
AssetMthlyPriceData = indexdata.resample('M').mean()
AssetMthlyPriceData['Date'] = AssetMthlyPriceData.index
AssetMthlyPriceData['Date'] = pd.to_datetime(AssetMthlyPriceData['Date'].dt.strftime('%Y-%m'), format='%Y-%m')
AssetMthlyPriceData = AssetMthlyPriceData[(AssetMthlyPriceData['Date'] > '1998-12-31')]
AssetMthlyPriceData = AssetMthlyPriceData[(AssetMthlyPriceData['Date'] < '2019-09-01')]
AssetMthlyPriceData.reset_index(drop=True, inplace=True)

# Take main US macro factors and format the data
USMacro = USMacrodata[['Date', 'us_core_pceinflation_rate', 'us_unemployment_rate',
                           'us_interest_rate','us_retail_sales_yoy', 'us_consumer_confidence']] 
USMacro['Date'] = pd.to_datetime(USMacrodata['Date'],dayfirst=True)
USMacro = USMacro[(USMacro['Date'] > '1998-12-31')]
USMacro = USMacro[(USMacro['Date'] < '2019-09-01')]
USMacro.reset_index(drop=True, inplace=True)
USMacro.fillna(0, inplace=True)

# Merge asset price and macro data
MergedAssetMacroData = pd.merge(USMacro, AssetMthlyPriceData, how='left', on='Date')

# Calculate Correlation, Covariance, R2 between all data
print('Calculating Corrrelation, Covariance, R2 between all data ...')
MergedAssetMacroDataCorr = MergedAssetMacroData.corr(method='pearson')
MergedAssetMacroDataR2 = MergedAssetMacroDataCorr.pow(2)
MergedAssetMacroDataCov = MergedAssetMacroData.cov()

# Plot correlation heatmap
print('Plotting correlation, R2, covariance heatmap ...')
ax = sns.heatmap(MergedAssetMacroDataCorr, annot=True, fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()
ax = sns.heatmap(MergedAssetMacroDataR2, annot=True, fmt=".2f")
plt.title('R2 Heatmap')
plt.show()
ax = sns.heatmap(MergedAssetMacroDataCov, annot=True, fmt=".2f")
plt.title('Covariance Heatmap')
plt.show()




