#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:10:24 2021

@author: nitinsinghal
"""
# Chapter 14 - End to End project 1 - Build a Roboadvisor
# Calculate Bond returns - NRR and Annualized for monthy and annual timeframes

# import libraries
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Bond returns calculator. Only for US, UK, EUBund. Bond data available only from Mar '08 for UK. 
# BondNRR = [BondPrice(EoY-SoY)+BondYieldMean(EoY To SoY)]/BondPrice(SoY)
# Bonds calculate yield income (Actual/365) and price gain/loss. Price available for US, UK, EU. Don't know coupon rate

# Bond Annual NRR
def get_BondAnnualNRR(BondYieldPrice):
    print('Calculating Bond Annual NRR ...')
    bondyieldprice = BondYieldPrice
    cntrybondprice = bondyieldprice.filter(regex='Price|Date', axis=1)
    cntrybondyield = bondyieldprice.filter(regex='Yield|Date', axis=1)
        
    # Get list of countries for bond yield/price
    bondcolnames = list(bondyieldprice.columns)
    bondcntry = list()
    n=0
    for col in range(1, len(bondcolnames), 2):
        bondcntry.insert(n,bondcolnames[col][:2])
        n=n+1
    
    for i in range(1, len(bondcntry)+1):
        BondPrice = pd.concat([cntrybondprice.iloc[:,0], cntrybondprice.iloc[:,i]], axis=1)
        BondYield = pd.concat([cntrybondyield.iloc[:,0], cntrybondyield.iloc[:,i]], axis=1)
        colname = BondPrice.columns[1][:-5]
        
        print('Calculating NRR for ',colname,'...')
        BondPrice.drop_duplicates(subset='Date', keep='first', inplace=True)
        BondPrice = BondPrice[~BondPrice.eq(0).any(1)]
        BondPrice.reset_index(drop=True, inplace=True)
        BondPrice['Year'] = pd.to_datetime(BondPrice['Date']).dt.to_period('Y')
        BondPrice = BondPrice.drop(['Date'],axis=1)
        BondSoYdata = BondPrice.groupby('Year').first()
        BondSoYdata['Date'] = BondSoYdata.index
        BondSoYdata.rename(columns={BondSoYdata.columns[0]:colname+'_SoY'}, inplace=True)
        BondEoYdata = BondPrice.groupby('Year').last()
        BondEoYdata['Date'] = BondEoYdata.index
        BondEoYdata.rename(columns={BondEoYdata.columns[0]:colname+'_EoY'}, inplace=True)
        BondSoYEoYPricedata = pd.merge(BondSoYdata, BondEoYdata, how='left', on='Date')
        BondSoYEoYPricedata.reset_index(drop=True, inplace=True)
        
        BondYield.drop_duplicates(subset='Date', keep='first', inplace=True)
        BondYield = BondYield[~BondYield.eq(0).any(1)]
        BondYield.reset_index(drop=True, inplace=True)
        BondYield['Year'] = pd.to_datetime(BondYield['Date']).dt.to_period('Y')
        BondYield = BondYield.drop(['Date'],axis=1)
        BondYielddata = BondYield.groupby('Year').mean()
        BondYielddata['Date'] = BondYielddata.index
        BondYielddata.reset_index(drop=True, inplace=True)
        BondYielddata[colname] = BondYielddata[BondYield.columns[0]].div(100.00)
        BondSoYEoYPricedata = pd.merge(BondSoYEoYPricedata, BondYielddata, how='left', on='Date')
        
        BondSoYEoYPricedata[colname+'_NRR'] = (BondSoYEoYPricedata[colname+'_EoY'] - BondSoYEoYPricedata[colname+'_SoY']+
                           BondYielddata[colname])/BondSoYEoYPricedata[colname+'_SoY']
        # Build the dataframe to return for all bond's annual nrr values
        if(i==1):
            AllBondAnnlNRR = BondSoYEoYPricedata
        else:
            AllBondAnnlNRR = pd.merge(AllBondAnnlNRR, BondSoYEoYPricedata, how='left', on='Date')
    return AllBondAnnlNRR

# Calculate Bond's Predicted Monthly Net Return rate using Curr Month - Prev month value
def get_BondMthlyNRR(BondYieldPrice):
    print('Calculating Bond Monthly NRR ...')
    cntrybondprice = BondYieldPrice.filter(regex='Price|Date', axis=1)
    cntrybondyield = BondYieldPrice.filter(regex='Yield|Date', axis=1)
        
    # Get list of countries for bond yield/price
    bondcolnames = list(BondYieldPrice.columns)
    bondcntry = list()
    n=0
    for col in range(1, len(bondcolnames), 2):
        bondcntry.insert(n,bondcolnames[col][:2])
        n=n+1
    
    for i in range(1, len(bondcntry)+1):
        BondPrice = pd.concat([cntrybondprice.iloc[:,0], cntrybondprice.iloc[:,i]], axis=1)
        BondYield = pd.concat([cntrybondyield.iloc[:,0], cntrybondyield.iloc[:,i]], axis=1)
        colname = BondPrice.columns[1][:-5]
        
        print('Calculating NRR for ',colname,'...')
        BondPrice = BondPrice[~BondPrice.eq(0).any(1)]
        BondPrice.reset_index(drop=True, inplace=True)
        BondPrice['YrMth'] = pd.to_datetime(BondPrice['Date'], yearfirst=True).dt.strftime('%Y-%m')
        BondPrice = BondPrice.drop(['Date'],axis=1)
        BondPredMthlyNRR = pd.DataFrame()
        for j in range(0,(len(BondPrice)-1)):
            BondPredMthlyNRR.loc[j,'Date'] = BondPrice.iloc[j+1,1]
            BondPredMthlyNRR.loc[j,colname+'_SoM'] = BondPrice.iloc[j,0]
            BondPredMthlyNRR.loc[j,colname+'_EoM'] = BondPrice.iloc[j+1,0]
    
        BondYield.drop_duplicates(subset='Date', keep='first', inplace=True)
        BondYield = BondYield[~BondYield.eq(0).any(1)]
        BondYield.reset_index(drop=True, inplace=True)
        BondYield['YrMth'] = pd.to_datetime(BondYield['Date'], yearfirst=True).dt.strftime('%Y-%m')
        BondYield = BondYield.drop(['Date'],axis=1)
        BondYield = BondYield.drop(BondYield.head(1).index)
        BondYield = BondYield.rename({'YrMth':'Date'}, axis='columns')
        BondYield.reset_index(drop=True, inplace=True)
        BondYield[BondYield.columns[0]] = BondYield[BondYield.columns[0]].div(100.00)
        BondYield = BondYield.rename({BondYield.columns[0]:colname+'_Yield'}, axis='columns')
        BondPredMthlyNRR = pd.merge(BondPredMthlyNRR, BondYield, how='left', on='Date')
        BondPredMthlyNRR[colname+'_NRR'] = (BondPredMthlyNRR[colname+'_EoM'] - BondPredMthlyNRR[colname+'_SoM']+
                           BondPredMthlyNRR[colname+'_Yield'])/BondPredMthlyNRR[colname+'_SoM']
        # Build the dataframe to return for all bond's annual nrr values
        if(i==1):
            AllBondPredMthlyNRR = BondPredMthlyNRR
        else:
            AllBondPredMthlyNRR = pd.merge(AllBondPredMthlyNRR, BondPredMthlyNRR, how='left', on='Date')
    return AllBondPredMthlyNRR

# Bond Annualized Return data
# Calculate Annualized return using Monthly Net Return rate
# Asset Annualized Returns AAR = ((1+amr1)*(1+amr2)...*(1+amrn))^1/n - 1. amr = asset monthly return
def get_BondAnnlzdReturn(BondYieldPrice):
    bondyieldprice = BondYieldPrice
    cntrybondprice = bondyieldprice.filter(regex='Price|Date', axis=1)
    cntrybondyield = bondyieldprice.filter(regex='Yield|Date', axis=1)
        
    # Get list of countries for bond yield/price
    bondcolnames = list(bondyieldprice.columns)
    bondcntry = list()
    n=0
    for col in range(1, len(bondcolnames), 2):
        bondcntry.insert(n,bondcolnames[col][:2])
        n=n+1
    
    for i in range(1, len(bondcntry)+1):
        BondPrice = pd.concat([cntrybondprice.iloc[:,0], cntrybondprice.iloc[:,i]], axis=1)
        BondYield = pd.concat([cntrybondyield.iloc[:,0], cntrybondyield.iloc[:,i]], axis=1)
        colname = BondPrice.columns[1][:-5]
        
        print('Calculating NRR for ',colname,'...')
        BondPrice = BondPrice[~BondPrice.eq(0).any(1)]
        bondyear = pd.DatetimeIndex(BondPrice['Date']).year.unique().tolist()
        BondPrice['Year'] = pd.DatetimeIndex(BondPrice['Date']).year
        BondPrice['YrMth'] = pd.to_datetime(BondPrice['Date']).dt.to_period('M')
        BondPrice = BondPrice.drop(['Date'],axis=1)
        BondSoMdata = BondPrice.groupby('YrMth').first()
        BondSoMdata['Date'] = BondSoMdata.index
        BondSoMdata.rename(columns={BondSoMdata.columns[0]:colname+'_SoM', BondSoMdata.columns[1]:colname+'_Year'}, inplace=True)
        BondEoMdata = BondPrice.groupby('YrMth').last()
        BondEoMdata['Date'] = BondEoMdata.index
        BondEoMdata.rename(columns={BondEoMdata.columns[0]:colname+'_EoM'}, inplace=True)
        BondSoMEoMPricedata = pd.merge(BondSoMdata, BondEoMdata, how='left', on='Date')
        BondSoMEoMPricedata.reset_index(drop=True, inplace=True)
        
        BondYield.drop_duplicates(subset='Date', keep='first', inplace=True)
        BondYield = BondYield[~BondYield.eq(0).any(1)]
        BondYield.reset_index(drop=True, inplace=True)
        BondYield['YrMth'] = pd.to_datetime(BondYield['Date']).dt.to_period('M')
        BondYield = BondYield.drop(['Date'],axis=1)
        BondYielddata = BondYield.groupby('YrMth').mean()
        BondYielddata['Date'] = BondYielddata.index
        BondYielddata.reset_index(drop=True, inplace=True)
        BondYielddata[colname] = BondYielddata[BondYield.columns[0]].div(100.00)
        BondYieldPricedata = pd.merge(BondSoMEoMPricedata, BondYielddata, how='left', on='Date')
        
        BondYieldPricedata[colname+'_NRR'] = (BondYieldPricedata[colname+'_EoM'] - BondYieldPricedata[colname+'_SoM']+
                           BondYieldPricedata[colname])/BondYieldPricedata[colname+'_SoM']
        BondMthlyNRR = BondYieldPricedata[['Date', colname+'_NRR', colname+'_Year']]
        
        bondnrrdata = pd.concat([BondMthlyNRR.iloc[:,1], BondMthlyNRR.iloc[:,2]], axis=1)
        BondAnnlzdReturndata = pd.DataFrame(bondyear, columns=['Date'])
    
        for j in range(0,len(bondyear)):
            dfBond = bondnrrdata[(bondnrrdata[colname+'_Year'] == bondyear[j])]
            bondannlzdreturn = 1
            bondannlzdreturnval = 0
            for k in range(0,len(dfBond)):
                bondannlzdreturn = bondannlzdreturn * (1+dfBond.iloc[k,0])
            bondannlzdreturnval = pow(bondannlzdreturn,(1/len(dfBond))) - 1
            BondAnnlzdReturndata.loc[j,colname+'_AnnlzdRtrn'] = bondannlzdreturnval
        
        # Build the dataframe to return for all bond's monthly nrr values
        if(i==1):
            AllBondAnnlzdReturndata = BondAnnlzdReturndata
        else:
            AllBondAnnlzdReturndata = pd.merge(AllBondAnnlzdReturndata, BondAnnlzdReturndata, how='left', on='Date')
    return AllBondAnnlzdReturndata
