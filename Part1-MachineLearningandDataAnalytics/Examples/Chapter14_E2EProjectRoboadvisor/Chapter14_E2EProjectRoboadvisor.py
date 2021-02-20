#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 18:36:07 2021

@author: nitinsinghal
"""

# Chapter 14 - End to End project 1 - Build a Roboadvisor

# RoboAdvisor Algo for multi asset portfolio
# Forecast future macro using past macro and FOMC/ECB/BoE forecasts
# Predict future asset prices using past macro data
# Calculate return of each asset for future timeframe (1m - 1 yr - 5yr - 10yr - 15 yr)
# Scenario analysis for different portfolio weights, for all portfolio returns, for time frame
# Account for correlation.
# Create backtesting logic for each portfolio return

#Import libraries
import sys
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

sys.path.append('/Users/nitinsinghal/Dropbox/DataScienceCourse/')
import Chapter14_RoboadvisorDataLoadWrangling as dw, Chapter14_RoboadvisorAssetPricePrediction as app
import Chapter14_RoboadvisorPortfolioReturnRiskCalculator as prrc, Chapter14_RoboadvisorAssetPredVsActDirectionCalculator as adc

# Load asset data from the data wrangling module
AllAssetdata, AllBondYieldPricedata, PortfolioWeights = dw.asset_data_wrangling()
# Load macro data from the data wrangling module
Macro5MFActualdata, CB5MFActualdata = dw.macro_data_wrangling()

####### 3 year price PREDICTION using Central Bank FORECAST #########
# Calculate predicted forecasts for next 3years, using CB 3yr forecast data for all assets and bonds
print('Start 3yr Asset price prediction using CB Forecasts....', datetime.datetime.now())
AllAssetsPred3Yrdata = app.get_AssetMthlyPricePredUsingCBFrcst(AllAssetdata, CB5MFActualdata, Macro5MFActualdata)
print('Start 3yr Bond price prediction using CB Forecasts....', datetime.datetime.now())
AllBondPred3Yrdata = app.get_BondMthlyPriceYieldPredUsingCBFrcst(AllBondYieldPricedata, CB5MFActualdata, Macro5MFActualdata)
AllAssetBondsPred3Yrdata = pd.merge(AllAssetsPred3Yrdata, AllBondPred3Yrdata, how='left', on='Date')

# Calculate Predicted Portfolio Return for different timeframes (1m-3yr) using CB Forecast data
returnperiod = '3yr'
predstartyear = 2020
cashreturn = 0.0001
PredPortfolioReturn = prrc.get_PortfolioPredictedReturn(AllAssetBondsPred3Yrdata, PortfolioWeights, returnperiod, predstartyear, cashreturn) 
print('\n Predicted Portfolio Weighted Return: ',PredPortfolioReturn*1000)

predportfannlzdreturn = 1.00
for i in range(0,len(PredPortfolioReturn)):
    predportfannlzdreturn = predportfannlzdreturn * (1+PredPortfolioReturn.loc[i,'Return'])
predportfannlzdreturnval = pow(predportfannlzdreturn,(1/len(PredPortfolioReturn))) - 1
print('\n Predicted Portfolio Annualized Return: ',predportfannlzdreturnval*100)

predportfavgreturn = 0.00
for i in range(0,len(PredPortfolioReturn)):
    predportfavgreturn = predportfavgreturn + PredPortfolioReturn.loc[i,'Return']
predportfavgreturnval = predportfavgreturn/len(PredPortfolioReturn)
print('\n  Predicted Average Return: ',predportfavgreturnval*100)

# Calculate Forecast Predicted Portfolio Variance (Volatility) for different timeframes (1m-3yr)
FrcstPredPortfolioVariance = prrc.get_PortfolioPredictedVariance(AllAssetBondsPred3Yrdata, PortfolioWeights, returnperiod, predstartyear)
FrcstPredPortfolioStdDev = np.sqrt(FrcstPredPortfolioVariance)
print('\n FrcstPred Portfolio Variance(Volatility): %.12f, Std Dev: %.12f' %(FrcstPredPortfolioVariance, FrcstPredPortfolioStdDev))

###### Logic for BACKTESTING - actual data used for prediction #######
# Accuracy -> (Predicted - Actual) prices using actual prices and macro data
# Direction -> Calculate Predicted vs Actual direction using actual prices and macro data
# Calculate Predicted vs Actual portfolio return and risk
# Part 2 - Portfolio Optimization - Maximise Return, Minimize Risk

# Get PREDICTED PRICES for ALL ASSETS using ACTUAL data 
print('Start Asset price prediction using actual data....', datetime.datetime.now())
allassetactpreddata = app.get_AssetMthlyPricePredUsingMacroActual(AllAssetdata, Macro5MFActualdata)
print('Start Bond price prediction using actual data....', datetime.datetime.now())
allbondactpreddata = app.get_BondMthlyPriceYieldPredUsingMacroActual(AllBondYieldPricedata, Macro5MFActualdata)
AllAssetBondActPreddata = pd.merge(allassetactpreddata, allbondactpreddata, how='left', on='Date')
print('End of price prediction: ', datetime.datetime.now())

acolnames = list(AllAssetdata.columns)
bcolnames = list(AllBondYieldPricedata.columns)

# For each asset Get predicted vs actual difference and % accuracy data for each month
AllAssetBondActPredDiffAcrcydata = adc.get_AssetBondMthlyActualPredDiffAcrcy(allassetactpreddata, allbondactpreddata, acolnames, bcolnames)

# Get predicted vs actual direction for actual data
AllAssetBondActPredDirection = adc.get_AssetBondActualPredictedDirection(acolnames, allassetactpreddata, bcolnames, allbondactpreddata)

#### DISPLAY BACKTESTING DIRECTION ACCURACY RESULTS ########
# Plot % total months for each year with same direction for Actual and Predicted 

AllAssetSameDirYrly = AllAssetBondActPredDirection.filter(regex='Date|_ActPredSameDir', axis=1)
AllAssetSameDirYrly['Year'] = pd.to_datetime(AllAssetSameDirYrly['Date']).dt.to_period('Y')
AllAssetSameDirYrly = AllAssetSameDirYrly.drop(['Date'],axis=1)
AllAssetSameDirYrlyTotalPct = AllAssetSameDirYrly.groupby('Year').sum()/12
AllAssetSameDirYrlyTotalPct['Year'] = AllAssetSameDirYrlyTotalPct.index
AllAssetSameDirYrlyTotalPct.reset_index(drop=True, inplace=True)
# Plot the results, split by asset group type
assetcrctdiryr = AllAssetSameDirYrlyTotalPct.filter(regex='Date|SP500|Nasdaq|Dax|CAC|FTSE', axis=1)
cmdcrctdiryr = AllAssetSameDirYrlyTotalPct.filter(regex='Date|Wilshire|Gold|OilWTI|GBPUSD|EURUSD', axis=1)
bondcrctdiryr = AllAssetSameDirYrlyTotalPct.filter(regex='Date|US10YrYield|UST10YrPrice|UK10YrYield|UKGilt10YrPrice|EUBund10YrYield|EUBund10YrPrice', axis=1)
plt.figure()
assetcrctdiryr.plot.bar(subplots=True, figsize=(10,10), legend=False, title='Stocks % total months for each year with same direction Act and Pred')
plt.xlabel('Year. 0->2000, 19->2019')
plt.ylabel('% Total out of 12')
plt.show()
cmdcrctdiryr.plot.bar(subplots=True, figsize=(10,10), legend=False, title='Commodities % total months for each year with same direction Act and Pred')
plt.xlabel('Year. 0->2000, 19->2019')
plt.ylabel('% Total out of 12')
plt.show()
bondcrctdiryr.plot.bar(subplots=True, figsize=(10,10), legend=False, title='Bonds % total months for each year with same direction Act and Pred')
plt.xlabel('Year. 0->2000, 19->2019')
plt.ylabel('% Total out of 12')
plt.show()

# Plot % of total years for each month with same direction for Actual and Predicted
AllAssetSameDirMthly = AllAssetBondActPredDirection.filter(regex='Date|_ActPredSameDir', axis=1)
AllAssetSameDirMthly['Month'] = pd.DatetimeIndex(AllAssetSameDirMthly['Date']).month
AllAssetSameDirMthlyTotal = AllAssetSameDirMthly.groupby('Month').sum()
# Calculate % Monthly ActPred Direction across all years
AllAssetSameDirMthlyTotalJan = AllAssetSameDirMthlyTotal[AllAssetSameDirMthlyTotal.index == 1]/19
AllAssetSameDirMthlyTotalNotJan = AllAssetSameDirMthlyTotal[AllAssetSameDirMthlyTotal.index != 1]/20
AllAssetSameDirMthlyPct = AllAssetSameDirMthlyTotalJan.append(AllAssetSameDirMthlyTotalNotJan, ignore_index=True)
AllAssetSameDirMthlyPct['Month'] = AllAssetSameDirMthlyPct.index
AllAssetSameDirMthlyPct.reset_index(drop=True, inplace=True)
# Plot the results, split by asset group type
assetcrctdirmthpct = AllAssetSameDirMthlyPct.filter(regex='Date|SP500|Nasdaq|Dax|CAC|FTSE', axis=1)
cmdcrctdirmthpct = AllAssetSameDirMthlyPct.filter(regex='Date|Wilshire|Gold|OilWTI|GBPUSD|EURUSD', axis=1)
bondcrctdirmthpct = AllAssetSameDirMthlyPct.filter(regex='Date|US10YrYield|UST10YrPrice|UK10YrYield|UKGilt10YrPrice|EUBund10YrYield|EUBund10YrPrice', axis=1)
plt.figure()
assetcrctdirmthpct.plot.bar(subplots=True, figsize=(10,10), legend=False, title='Stocks % total years for each month with same direction Act and Pred')
plt.xlabel('Month. 0->January, 11->December')
plt.ylabel('Total % out of 20 years')
plt.show()
cmdcrctdirmthpct.plot.bar(subplots=True, figsize=(10,10), legend=False, title='Commodities % total years for each month with same direction Act and Pred')
plt.xlabel('Month. 0->January, 11->December')
plt.ylabel('Total % out of 20 years')
plt.show()
bondcrctdirmthpct.plot.bar(subplots=True, figsize=(10,10), legend=False, title='Bonds % total years for each month with same direction Act and Pred')
plt.xlabel('Month. 0->January, 11->December')
plt.ylabel('Total % out of 20 years')
plt.show()

## Backtesting Actual ##
# Calculate Actual data Portfolio Return for different timeframes (1m-3yr-5yr-10yr)
returnperiod = '3yr'
actpredstartyear = 2017
cashreturn = 0.0001
allassetbondactualdata = AllAssetBondActPreddata.filter(regex='Date|_Act', axis=1)
ActPortfolioReturn = prrc.get_PortfolioPredictedReturn(allassetbondactualdata, PortfolioWeights, returnperiod, actpredstartyear, cashreturn) 
print('\n Actual Portfolio Weighted Return: ',ActPortfolioReturn*1000)

actportfannlzdreturn = 1.00
for i in range(0,len(ActPortfolioReturn)):
    actportfannlzdreturn = actportfannlzdreturn * (1+ActPortfolioReturn.loc[i,'Return'])
actportfannlzdreturnval = pow(actportfannlzdreturn,(1/len(ActPortfolioReturn))) - 1
print('\n Actual Portfolio Annualized Return: ',actportfannlzdreturnval*100)

actpredportfavgreturn = 0.00
for i in range(0,len(ActPortfolioReturn)):
    actpredportfavgreturn = actpredportfavgreturn + ActPortfolioReturn.loc[i,'Return']
actpredportfavgreturnval = actpredportfavgreturn/len(ActPortfolioReturn)
print('\n Actual Portfolio Average Return: ',actpredportfavgreturnval*100)

# Calculate Actual Portfolio Variance (Volatility) for different timeframes (1m-3yr-5yr-10yr)
ActPortfolioVariance = prrc.get_PortfolioPredictedVariance(allassetbondactualdata, PortfolioWeights, returnperiod, actpredstartyear)
ActPortfolioStdDev = np.sqrt(ActPortfolioVariance)
print('\n Actual Portfolio Variance(Volatility): %.12f, Std Dev: %.12f' %(ActPortfolioVariance, ActPortfolioStdDev))


## Backtesting Predicted ##
# Calculate Actual data Predicted Portfolio Return for different timeframes (1m-3yr-5yr-10yr)
allassetbondactualpreddata = AllAssetBondActPreddata.filter(regex='Date|_Pred', axis=1)
PredPortfolioReturn = prrc.get_PortfolioPredictedReturn(allassetbondactualpreddata, PortfolioWeights, returnperiod, actpredstartyear, cashreturn) 
print('\n Predicted Portfolio Weighted Return: ',PredPortfolioReturn*1000)

predportfannlzdreturn = 1.00
for i in range(0,len(PredPortfolioReturn)):
    predportfannlzdreturn = predportfannlzdreturn * (1+PredPortfolioReturn.loc[i,'Return'])
predportfannlzdreturnval = pow(predportfannlzdreturn,(1/len(PredPortfolioReturn))) - 1
print('\n Predicted Portfolio Annualized Return: ',predportfannlzdreturnval*100)

predportfavgreturn = 0.00
for i in range(0,len(PredPortfolioReturn)):
    predportfavgreturn = predportfavgreturn + PredPortfolioReturn.loc[i,'Return']
predportfavgreturnval = predportfavgreturn/len(PredPortfolioReturn)
print('\n Predicted Portfolio Average Return: ',predportfavgreturnval*100)

# Calculate Actual data Predicted Portfolio Variance (Volatility) for different timeframes (1m-3yr-5yr-10yr)
PredPortfolioVariance = prrc.get_PortfolioPredictedVariance(allassetbondactualpreddata, PortfolioWeights, returnperiod, actpredstartyear)
PredPortfolioStdDev = np.sqrt(PredPortfolioVariance)
print('\n Predicted Portfolio Variance(Volatility): %.12f, Std Dev: %.12f' %(PredPortfolioVariance, PredPortfolioStdDev))

