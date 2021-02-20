#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 12:54:22 2021

@author: nitinsinghal
"""
# Chapter 14 - End to End project 1 - Build a Roboadvisor
# Data Loading and Wrangling

# import libraries
import pandas as pd
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
    

def asset_data_wrangling():
    # LOAD asset DATA for each country
    # Macro data - US, UK, EU
    print('Loading asset data ...')
    
    # Asset data
    Nasdaqdata = pd.read_csv('Nasdaq.csv')
    SP500data = pd.read_csv('SP500.csv')
    Russell2000data = pd.read_csv('Russell2000.csv')
    CACdata = pd.read_csv('CAC40.csv')
    FTSEdata = pd.read_csv('FTSE100.csv')
    Daxdata = pd.read_csv('DAX.csv')
    OilWTIdata = pd.read_csv('OilWTI.csv')
    Golddata = pd.read_csv('Gold.csv')
    # Wilshire US Real Estate Securities Price Index (Wilshire US RESI) (WILLRESIPR)
    WilshireREdata = pd.read_csv('WilshireREPriceIndex.csv')
    US10YrYielddata = pd.read_csv('US10YrYield.csv')
    UK10YrYielddata = pd.read_csv('UK10YrYield.csv')
    EUBund10YrYielddata = pd.read_csv('German10YrYield.csv')
    UST10YrPriceddata = pd.read_csv('UST10YrPrice.csv')
    UKGilt10YrPricedata = pd.read_csv('UKGilt10YrPrice.csv')
    EUBund10YrPricedata = pd.read_csv('EUBund10YrPrice.csv')
    PortfolioWeights = pd.read_csv('PortfolioWeights.csv')
    GBPUSDdata = pd.read_csv('GBPUSD.csv')
    EURUSDdata = pd.read_csv('EURUSD.csv')
    
    # DATA WRANGLING - CLEANING, FORMATTING
    #Use High price instead of Close as it gives higher range to predict
    print('Performing Data Wrangling of Asset Data(Formatting, Cleaning) ...')
    
    Nasdaq = data_cleaning(data_formatting(Nasdaqdata))
    Nasdaq = Nasdaq.rename({'High':'Nasdaq'}, axis='columns')
    SP500 = data_cleaning(data_formatting(SP500data))
    SP500 = SP500.rename({'High':'SP500'}, axis='columns')
    Dax = data_cleaning(data_formatting(Daxdata))
    Dax = Dax.rename({'High':'Dax'}, axis='columns')
    CAC = data_cleaning(data_formatting(CACdata))
    CAC = CAC.rename({'High':'CAC'}, axis='columns')
    FTSE = data_cleaning(data_formatting(FTSEdata))
    FTSE = FTSE.rename({'High':'FTSE'}, axis='columns')
    Russell2000 = data_cleaning(data_formatting(Russell2000data))
    Russell2000 = Russell2000.rename({'High':'Russell2000'}, axis='columns')
    OilWTI = data_cleaning(data_formatting(OilWTIdata))
    OilWTI = OilWTI.rename({'High':'OilWTI'}, axis='columns')
    Gold = data_cleaning(data_formatting(Golddata))
    Gold = Gold.rename({'High':'Gold'}, axis='columns')
    US10YrYield = data_cleaning(data_formatting(US10YrYielddata))
    US10YrYield = US10YrYield.rename({'High':'US10YrYield'}, axis='columns')
    UK10YrYield = data_cleaning(data_formatting(UK10YrYielddata))
    UK10YrYield = UK10YrYield.rename({'High':'UK10YrYield'}, axis='columns')
    EUBund10YrYield = data_cleaning(data_formatting(EUBund10YrYielddata))
    EUBund10YrYield = EUBund10YrYield.rename({'High':'EUBund10YrYield'}, axis='columns')
    UST10YrPrice = data_cleaning(data_formatting(UST10YrPriceddata))
    UST10YrPrice = UST10YrPrice.rename({'High':'UST10YrPrice'}, axis='columns')
    UKGilt10YrPrice = data_cleaning(data_formatting(UKGilt10YrPricedata))
    UKGilt10YrPrice = UKGilt10YrPrice.rename({'High':'UKGilt10YrPrice'}, axis='columns')
    EUBund10YrPrice = data_cleaning(data_formatting(EUBund10YrPricedata))
    EUBund10YrPrice = EUBund10YrPrice.rename({'High':'EUBund10YrPrice'}, axis='columns')
    
    GBPUSD = data_formatting(GBPUSDdata)
    GBPUSD = GBPUSD.rename({'High':'GBPUSD'}, axis='columns')
    EURUSD = data_formatting(EURUSDdata)
    EURUSD = EURUSD.rename({'High':'EURUSD'}, axis='columns')
    
    WilshireREdata = WilshireREdata[~WilshireREdata['High'].str.startswith('.')]
    WilshireREdata.reset_index(drop=True, inplace=True)
    WilshireRE = data_cleaning(data_formatting(WilshireREdata))
    WilshireRE = WilshireRE.rename({'High':'WilshireRE'}, axis='columns')
    
    # DATA WRANGLING - MERGING
    #Merge stock, oil, Gold, RE index, Ccy data
    print('Performing Data Wrangling (Merging) ...')
    
    MergedAssetdata = pd.merge(SP500, Nasdaq, how='left', on='Date')
    MergedAssetdata = pd.merge(MergedAssetdata, Dax, how='left', on='Date')
    MergedAssetdata = pd.merge(MergedAssetdata, CAC, how='left', on='Date')
    MergedAssetdata = pd.merge(MergedAssetdata, FTSE, how='left', on='Date')
    MergedAssetdata = pd.merge(MergedAssetdata, WilshireRE, how='left', on='Date')
    MergedAssetdata = pd.merge(MergedAssetdata, Gold, how='left', on='Date')
    MergedAssetdata = pd.merge(MergedAssetdata, OilWTI, how='left', on='Date')
    
    MergedAssetdata = pd.merge(MergedAssetdata, GBPUSD, how='left', on='Date')
    MergedAssetdata = pd.merge(MergedAssetdata, EURUSD, how='left', on='Date')
    MergedAssetdata = MergedAssetdata.fillna(0)
    
    #Get all merged data from 1999, as most indices have data from then 
    MergedAsset99data = MergedAssetdata[(MergedAssetdata['Date'] > '1998-12-31')]
    MergedAsset99data.drop_duplicates(subset='Date', keep='first', inplace=True)
    MergedAsset99data = MergedAsset99data[~MergedAsset99data.eq(0).any(1)]
    MergedAsset99data.reset_index(drop=True, inplace=True)
    AllAsset99data = MergedAsset99data
    
    # Merge Bond Price and Yield into one dataframe for countries
    USBondYieldPrice = pd.merge(US10YrYield, UST10YrPrice, how='left', on='Date')
    UKBondYieldPrice = pd.merge(UK10YrYield, UKGilt10YrPrice, how='left', on='Date')
    EUBundYieldPrice = pd.merge(EUBund10YrYield, EUBund10YrPrice, how='left', on='Date')
    AllBondYieldPricedata = pd.merge(USBondYieldPrice, UKBondYieldPrice, how='left', on='Date')
    AllBondYieldPricedata = pd.merge(AllBondYieldPricedata, EUBundYieldPrice, how='left', on='Date')
    AllBondYieldPricedata = AllBondYieldPricedata[(AllBondYieldPricedata['Date'] > '1998-12-31')]
    AllBondYieldPricedata.drop_duplicates(subset='Date', keep='first', inplace=True)
    AllBondYieldPricedata = AllBondYieldPricedata[~AllBondYieldPricedata.eq(0).any(1)]
    AllBondYieldPricedata.reset_index(drop=True, inplace=True)
    AllBondYieldPricedata.fillna(0, inplace=True)
    
    # Return the clean data after wrangling
    return(AllAsset99data, AllBondYieldPricedata, PortfolioWeights)

def macro_data_wrangling():    
    # LOAD macro DATA for each country - US, UK, EU
    print('Loading macro data ...')
    
    USMacrodata = pd.read_csv('USMacrodata.csv')
    EUMacrodata = pd.read_csv('EUMacrodata.csv')
    UKMacrodata = pd.read_csv('UKMacrodata.csv')
    FedForecastdata = pd.read_csv('FedForecasts.csv')
    EUForecastdata = pd.read_csv('ECBForecasts.csv')
    BoEForecastdata = pd.read_csv('BoEForecasts.csv')
    
    # Take macro data from 1999 and formate date column
    print('Performing Data Wrangling of Macro Data(Formatting, Merging) ...')
    
    USMacro = USMacrodata[['Date','us_gdp_yoy', 'us_industrial_production','us_inflation_rate', 'us_core_pceinflation_rate',
                               'us_interest_rate','us_retail_sales_yoy', 'us_consumer_confidence', 'us_business_confidence',  
                               'us_unemployment_rate', 'us_manufacturing_production']] 
    USMacro = data_formatting(USMacro)
    USMacro = USMacro[(USMacro['Date'] > '1998-12-31')]
    
    EUMacro = EUMacrodata[['Date','eu_gdp_yoy', 'eu_industrial_production','eu_inflation_rate', 'eu_core_inflation_rate',
                               'eu_interest_rate','eu_manufacturing_production','eu_retail_sales_yoy',
                               'eu_consumer_confidence','eu_business_confidence','eu_unemployment_rate']]
    EUMacro = data_formatting(EUMacro)
    EUMacro = EUMacro[(EUMacro['Date'] > '1998-12-31')]
    
    UKMacro = UKMacrodata[['Date','uk_gdp_yoy', 'uk_industrial_production','uk_inflation_rate', 'uk_core_inflation_rate',
                               'uk_interest_rate','uk_manufacturing_production','uk_retail_sales_yoy',
                               'uk_consumer_confidence','uk_business_confidence','uk_unemployment_rate']]
    UKMacro = data_formatting(UKMacro)
    UKMacro = UKMacro[(UKMacro['Date'] > '1998-12-31')]
    
    # merge us, eu, uk macro data files
    Macro99 = pd.merge(USMacro, EUMacro, how='left', on='Date')
    Macro99 = pd.merge(Macro99, UKMacro, how='left', on='Date')
    Macro99.fillna(0, inplace=True)
    
    # DATA WRANGLING - MERGING
    # Use the 5 main macro factors (5MF) to predict asset prices for which cb's publish forecasts
    # Merge the central bank forecasts into one dataframe
    # Add the cb forecasts to the actual for each macro and predict asset price for each month
    
    Macro5MF99act = Macro99[['Date','us_core_pceinflation_rate','us_inflation_rate','us_interest_rate','us_gdp_yoy','us_unemployment_rate', 
                         'eu_core_inflation_rate','eu_inflation_rate','eu_interest_rate','eu_gdp_yoy','eu_unemployment_rate',
                         'uk_core_inflation_rate','uk_inflation_rate','uk_interest_rate','uk_gdp_yoy','uk_unemployment_rate']]
    
    # Merge the Central Bank 5 macro forecast data into one dataframe
    # THIS DATA MUST BE UPDATED WITH ACTUAL EVERY MONTH AND RE-RUN THE ALGO
    print('Performing Data Wrangling of CentralBank Forecast Data(Formatting, Merging) ...')
    
    FedForecastdata = data_formatting(FedForecastdata)
    EUForecastdata = data_formatting(EUForecastdata)
    BoEForecastdata = data_formatting(BoEForecastdata)
    CB5MFMergedactdata = pd.merge(FedForecastdata, EUForecastdata, on='Date', how='left')
    CB5MFMergedactdata = pd.merge(CB5MFMergedactdata, BoEForecastdata, on='Date', how='left')
    
     # Return the clean data after wrangling
    return(Macro5MF99act, CB5MFMergedactdata)