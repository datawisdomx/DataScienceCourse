#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:42:24 2021

@author: nitinsinghal
"""
# Chapter 14 - End to End project 1 - Build a Roboadvisor
# Portfolio Return and Risk Calculator

#Import libraries
import sys
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

sys.path.append('/Users/nitinsinghal/Dropbox/DataScienceCourse/')
import Chapter14_RoboadvisorAssetReturnsCalculator as arc, Chapter14_RoboadvisorBondReturnsCalculator as brc

####### Logic for Portfolio Return  #######
# Portfolio Return = AR1*W1+Ar2*W2+...+ARn*Wn.
# Weight grid Example:  
    # Period 	Stk Ind	Bonds Gold	Rl Est Cash	Cmdt Indx	Tot
    # 3m	    20%	40%	20%	  10%	10%	   0%	0%          100%				
    # Asset = Stock Index, Bond, Gold, Oil, RE, Cash, Cmdt Indx.
# Calculate Annualized, Average return for a period
# Calculate Real (Inflation adjusted) and Nominal returns

# Get Portfolio Predicted Assets Return based on type (index, bond) and return period (yr, m)
def get_PortfolioPredictedAssetsReturn(allassetdata, returnperiod, startyear):
    print('Calculating predicted return for each Asset for period = ',returnperiod,' ...')
    allbonddata = allassetdata.filter(regex='10Yr|Date', axis=1)
    assetportfdata = allassetdata.drop(allassetdata.filter(regex='10Yr', axis=1), axis=1)
    PortfolioPredictedAssetsNRR = pd.DataFrame()

    # Get predicted asset return based on type (index, bond) and return period (yr, m)
    if returnperiod in ('1yr','2yr','3yr'):
        assetannlreturndata = arc.get_AssetAnnlNRR(assetportfdata)
        assetannlreturndata = assetannlreturndata.filter(regex='_NRR|Date', axis=1)
        bondannlreturndata = brc.get_BondAnnualNRR(allbonddata)
        bondannlreturndata =  bondannlreturndata.filter(regex='_NRR|Date', axis=1)
        allassetnrr = pd.merge(assetannlreturndata, bondannlreturndata, how='left', on='Date')
        allassetnrr.fillna(0, inplace=True)
        
        dfast = pd.DataFrame()
        for k, v in allassetnrr['Date'].iteritems():
            dfast.loc[k, 'Date'] = v.to_timestamp().year
        allassetnrr['Date'] = dfast['Date']
        
        if(returnperiod == '1yr'):
            PortfolioPredictedAssetsNRR = allassetnrr[(allassetnrr['Date'] == startyear)]
        elif(returnperiod == '2yr'):
            PortfolioPredictedAssetsNRR = allassetnrr[(allassetnrr['Date'] >= startyear)]
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(PortfolioPredictedAssetsNRR['Date'] <= (startyear+1))]
        elif(returnperiod == '3yr'):
            PortfolioPredictedAssetsNRR = allassetnrr[(allassetnrr['Date'] >= startyear)]
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(PortfolioPredictedAssetsNRR['Date'] <= (startyear+2))]
        PortfolioPredictedAssetsNRR.reset_index(drop=True, inplace=True)
    elif returnperiod in ('3m','6m','9m'):
        assetmthlyreturndata = arc.get_AssetMthlyNRR(assetportfdata)
        assetmthlyreturndata = assetmthlyreturndata.filter(regex='_NRR|Date', axis=1)
        bondmthlyreturndata = brc.get_BondMthlyNRR(allbonddata)
        bondmthlyreturndata = bondmthlyreturndata.filter(regex='_NRR|Date', axis=1)
        allassetnrr = pd.merge(assetmthlyreturndata, bondmthlyreturndata, how='left', on='Date')
        PortfolioPredictedAssetsNRR = allassetnrr[(pd.DatetimeIndex(allassetnrr['Date']).year == startyear)]
        PortfolioPredictedAssetsNRR.reset_index(drop=True, inplace=True)
        if(returnperiod == '3m'):
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(PortfolioPredictedAssetsNRR.index < 3)]
        elif(returnperiod == '6m'):
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(PortfolioPredictedAssetsNRR.index < 6)]
        elif(returnperiod == '9m'):
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(PortfolioPredictedAssetsNRR.index < 9)]
    else:
        print('Invalid return period')
    return PortfolioPredictedAssetsNRR

# Calculate Portfolio Predicted Return for different timeframes (1m-3yr)
def get_PortfolioPredictedReturn(allassetdata, PortfolioWeights, returnperiod, startyear, cashreturn):
    print('Calculating Predicted Portfolio Return ...')
    # Call method to get Portfolio Assets Return based on type (index, bond) and return period (yr, m)
    portfolioassetsnrr = get_PortfolioPredictedAssetsReturn(allassetdata, returnperiod, startyear)
    
    # Calculate portfolio weighted asset nrr return
    portfolioweights = PortfolioWeights[(PortfolioWeights['Period'] == returnperiod)]
    portfolioweights.drop(['Period','Total'], axis=1, inplace=True)
    #portfolioweights.drop(['Period','Total','REIndex','Gold','OilWTI'], axis=1, inplace=True)
    portfolioweights.reset_index(drop=True, inplace=True)
    
    # Filter portfolio assets for one country
    Portfolio = portfolioassetsnrr.filter(regex='Date|Nasdaq|UST10Yr|WilshireRE|Gold|OilWTI', axis=1)
    #Portfolio = portfolioassetsnrr.filter(regex='Date|SP500|UKGilt', axis=1)
    Portfolio['Cash'] = np.array(cashreturn)
    portfoliodates = Portfolio['Date']
    Portfolio = Portfolio.drop(['Date'], axis=1)
    PortfolioPredictedReturn = pd.DataFrame()
    
    for i in range(0, len(portfoliodates)):
        PortfolioPredictedReturn.loc[i, 'Period'] = portfoliodates[i]
        PortfolioPredictedReturn.loc[i, 'Return'] = pd.np.multiply(Portfolio.head(1),portfolioweights).sum(axis=1)[i]
        Portfolio = Portfolio.drop(i, axis=0)
    return PortfolioPredictedReturn

####### Logic for Portfolio Risk (Variance) #######
# Var(Portf) = ∑i=1 to n (VarARi*Wi^2) + ∑i=1 to n∑j=i+1 to n (2*Wi*Wj*Cov(ARi,ARj)) = Volatility
# Cov(AR1, AR2) = CorrCoeffAR1AR2*SDAR1*SDAR2
# Var x = ∑((x-Avgx)^2)/n. Spread from mean. Excess weight to outliers
# Cov(x,y) = ∑[(xi-xavg)*(yi-yavg)]/n-1. Directional relationship between returns of 2 assets
# Correlation Coefficient - Strength of relationship between 2 assets -1 to 1
# Std Dev Portf = Sqrt(Var (Portf)). Dispersion of the returns from the mean. Same unit as data

# Calculate Portfolio Predicted Variance (Volatility) for different timeframes (1m-3yr)
def get_PortfolioPredictedVariance(allassetdata, PortfolioWeights, returnperiod, startyear):
    print('Calculating Predicted Portfolio Risk (Variance) for period = ',returnperiod,' ...')
    allbonddata = allassetdata.filter(regex='10Yr|Date', axis=1)
    assetportfdata = allassetdata.drop(allassetdata.filter(regex='10Yr', axis=1), axis=1)
    PortfolioPredictedAssetsNRR = pd.DataFrame()
    
    # Get portfolio predicted assets monthly return based on type (index, bond)
    assetmthlyreturndata = arc.get_AssetMthlyNRR(assetportfdata)
    assetmthlyreturndata = assetmthlyreturndata.filter(regex='_NRR|Date', axis=1)
    bondmthlyreturndata = brc.get_BondMthlyNRR(allbonddata)
    bondmthlyreturndata = bondmthlyreturndata.filter(regex='_NRR|Date', axis=1)
    allassetnrr = pd.merge(assetmthlyreturndata, bondmthlyreturndata, how='left', on='Date')
    allassetnrr.fillna(0, inplace=True)
    
    # Get portfilio for period (yr, m)
    if returnperiod in ('1yr','2yr','3yr'):
        if(returnperiod == '1yr'):
            PortfolioPredictedAssetsNRR = allassetnrr[(pd.DatetimeIndex(allassetnrr['Date']).year == startyear)]
        elif(returnperiod == '2yr'):
            PortfolioPredictedAssetsNRR = allassetnrr[(pd.DatetimeIndex(allassetnrr['Date']).year >= startyear)]
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(pd.DatetimeIndex(PortfolioPredictedAssetsNRR['Date']).year <= (startyear+1))]
        elif(returnperiod == '3yr'):
            PortfolioPredictedAssetsNRR = allassetnrr[(pd.DatetimeIndex(allassetnrr['Date']).year >= startyear)]
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(pd.DatetimeIndex(PortfolioPredictedAssetsNRR['Date']).year <= (startyear+2))]
        PortfolioPredictedAssetsNRR.reset_index(drop=True, inplace=True)
    elif returnperiod in ('3m','6m','9m'):
        PortfolioPredictedAssetsNRR = allassetnrr[(pd.DatetimeIndex(allassetnrr['Date']).year == startyear)]
        PortfolioPredictedAssetsNRR.reset_index(drop=True, inplace=True)
        if(returnperiod == '3m'):
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(PortfolioPredictedAssetsNRR.index < 3)]
        elif(returnperiod == '6m'):
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(PortfolioPredictedAssetsNRR.index < 6)]
        elif(returnperiod == '9m'):
            PortfolioPredictedAssetsNRR = PortfolioPredictedAssetsNRR[(PortfolioPredictedAssetsNRR.index < 9)]
    else:
        print('Invalid variance period')
    
    # Get portfolio weights
    portfolioweights = PortfolioWeights[(PortfolioWeights['Period'] == returnperiod)]
    portfolioweights.drop(['Period','Total'], axis=1, inplace=True)
    # portfolioweights.drop(['Period','Total','REIndex','Gold','OilWTI'], axis=1, inplace=True)
    portfolioweights.reset_index(drop=True, inplace=True)
    
    # Filter portfolio assets for one country
    Portfolio = PortfolioPredictedAssetsNRR.filter(regex='Date|Nasdaq|UST10Yr|WilshireRE|Gold|OilWTI', axis=1)
    # Portfolio = PortfolioPredictedAssetsNRR.filter(regex='Date|SP500|UKGilt', axis=1)
    
    # Calculate weighted variance for each assets nrr. 
    # Var x = ∑((x-Avgx)^2)/n. Weighted Var = (Vari*Wi^2)
    PredictedAssetsWghtVar = pd.DataFrame()
    for i in range(1, len(Portfolio.columns)):
        colname = Portfolio.columns[i][:-4]
        PredictedAssetsWghtVar.loc[0, colname+'_WghtVar'] = np.square(portfolioweights.iloc[0,i-1]) * Portfolio.iloc[:,i].var()
    
    # Calculate weighted covariance for assetnrr unique pairs. 
    # Cov(AR1,AR2) = CorrCoeffAR1AR2*SDAR1*SDAR2. weighted cov = (2*Wi*Wj*Cov(ARi,ARj)
    rowcount = 0
    for m in range(1, len(Portfolio.columns)-1):
        rowcount += m
    PredictedAssetsWghtCoVar = pd.DataFrame()
    n=0
    while (n<rowcount):
        for i in range(1, len(Portfolio.columns)):
            colname = Portfolio.columns[i][:-4]
            for j in range(i+1, len(Portfolio.columns)):
                AssetsCoVar = Portfolio[[Portfolio.columns[i], Portfolio.columns[j]]].cov().iloc[0,1]
                PredictedAssetsWghtCoVar.loc[n, 'WghtCoVar'] = 2 * portfolioweights.iloc[0,i-1] * portfolioweights.iloc[0,j-1] * AssetsCoVar
                n += 1
    
    # Calculate variance for portfolio 
    # Var(Portf) = ∑i=1 to n (VarARi*Wi^2) + ∑i=1 to n∑j=i+1 to n (2*Wi*Wj*Cov(ARi,ARj))
    PortfolioPredictedAssetsVar = PredictedAssetsWghtVar.sum(axis=1)[0] + PredictedAssetsWghtCoVar.sum(axis=0)[0]
    return PortfolioPredictedAssetsVar
