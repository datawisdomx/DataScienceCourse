#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:24:54 2021

@author: nitinsinghal
"""
# Chapter 14 - End to End project 1 - Build a Roboadvisor
# Calculate Asset returns (excluding bonds) - NRR and Annualized for monthy and annual timeframes

# import libraries
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Calculate Annual Net Return rate using Start/End of Year value
# AR = (APEoY - APSoy)/APSoY
def get_AssetAnnlNRR(allassetdata):
    print('Calculating Asset Annual NRR ...')
    colnames = list(allassetdata.columns)
    
    for i in range(1, len(colnames)):
        print('Calculating NRR for ',colnames[i],'...')
        assetdata = pd.concat([allassetdata.iloc[:,0], allassetdata.iloc[:,i]], axis=1)
        assetdata['Year'] = pd.to_datetime(assetdata['Date']).dt.to_period('Y')
        assetdata = assetdata.drop(['Date'],axis=1)
        AssetSoYdata = assetdata.groupby('Year').first()
        AssetSoYdata['Date'] = AssetSoYdata.index
        AssetSoYdata.rename(columns={AssetSoYdata.columns[0]:colnames[i]+'_SoY'}, inplace=True)
        AssetEoYdata = assetdata.groupby('Year').last()
        AssetEoYdata['Date'] = AssetEoYdata.index
        AssetEoYdata.rename(columns={AssetEoYdata.columns[0]:colnames[i]+'_EoY'}, inplace=True)
        AssetAnnlNRRdata = pd.merge(AssetSoYdata, AssetEoYdata, how='left', on='Date')
        AssetAnnlNRRdata.reset_index(drop=True, inplace=True)
        AssetAnnlNRRdata = AssetAnnlNRRdata.reindex(columns=['Date',colnames[i]+'_SoY',colnames[i]+'_EoY'])
        AssetAnnlNRRdata[colnames[i]+'_NRR'] = (AssetAnnlNRRdata[colnames[i]+'_EoY'] - 
                          AssetAnnlNRRdata[colnames[i]+'_SoY'])/AssetAnnlNRRdata[colnames[i]+'_SoY']
        if(i==1):
            AllAssetAnnlNRRdata = AssetAnnlNRRdata
        else:
            AllAssetAnnlNRRdata = pd.merge(AllAssetAnnlNRRdata, AssetAnnlNRRdata, how='left', on='Date')
    return AllAssetAnnlNRRdata

# Calculate Asset's Monthly Net Return rate using Curr Month - Prev month value
def get_AssetMthlyNRR(allassetdata):
    print('Calculating Asset Monthly NRR ...')
    colnames = list(allassetdata.columns)
    
    for i in range(1, len(colnames)):
        print('Calculating NRR for ',colnames[i],'...')
        AssetPredMthlyNRR = pd.DataFrame()
        assetdata = pd.concat([allassetdata.iloc[:,0], allassetdata.iloc[:,i]], axis=1)
        assetdata['YrMth'] = pd.to_datetime(assetdata['Date'], yearfirst=True).dt.strftime('%Y-%m')
        assetdata = assetdata.drop(['Date'],axis=1)
        for j in range(0,(len(assetdata)-1)):
            AssetPredMthlyNRR.loc[j,'Date'] = assetdata.iloc[j+1,1]
            AssetPredMthlyNRR.loc[j,colnames[i]+'_SoM'] = assetdata.iloc[j,0]
            AssetPredMthlyNRR.loc[j,colnames[i]+'_EoM'] = assetdata.iloc[j+1,0]
            AssetPredMthlyNRR.loc[j,colnames[i]+'_NRR'] = ((assetdata.iloc[j+1,0] - assetdata.iloc[j,0])/assetdata.iloc[j,0])
        if(i==1):
            AllAssetPredMthlyNRR = AssetPredMthlyNRR
        else:
            AllAssetPredMthlyNRR = pd.merge(AllAssetPredMthlyNRR, AssetPredMthlyNRR, how='left', on='Date')
    return AllAssetPredMthlyNRR

# Average return is the average of monthly returns AvgR = Sum(amr)/n
def get_AssetAvgReturn(allassetdata):
    print('Calculating Asset Average Return ...')
    colnames = list(allassetdata.columns)
    assetyear = pd.DatetimeIndex(allassetdata['Date']).year.unique().tolist()
    
    for i in range(1, len(colnames)):
        print('Calculating Average Return for ',colnames[i],'...')
        assetdata = pd.concat([allassetdata.iloc[:,0], allassetdata.iloc[:,i]], axis=1)
        assetdata['Year'] = pd.DatetimeIndex(assetdata['Date']).year
        assetdata['YrMth'] = pd.to_datetime(assetdata['Date']).dt.to_period('M')
        assetdata = assetdata.drop(['Date'],axis=1)
        AssetSoMdata = assetdata.groupby('YrMth').first()
        AssetSoMdata['Date'] = AssetSoMdata.index
        AssetSoMdata.rename(columns={AssetSoMdata.columns[0]:colnames[i]+'_SoM', AssetSoMdata.columns[1]:colnames[i]+'_Year'}, inplace=True)
        AssetEoMdata = assetdata.groupby('YrMth').last()
        AssetEoMdata['Date'] = AssetEoMdata.index
        AssetEoMdata.rename(columns={AssetEoMdata.columns[0]:colnames[i]+'_EoM'}, inplace=True)
        AssetMthlyNRRdata = pd.merge(AssetSoMdata, AssetEoMdata, how='left', on='Date')
        AssetMthlyNRRdata.reset_index(drop=True, inplace=True)
        AssetMthlyNRRdata = AssetMthlyNRRdata.reindex(columns=['Date',colnames[i]+'_SoM',colnames[i]+'_EoM',colnames[i]+'_Year'])
        AssetMthlyNRRdata[colnames[i]+'_NRR'] = (AssetMthlyNRRdata[colnames[i]+'_EoM'] - 
                          AssetMthlyNRRdata[colnames[i]+'_SoM'])/AssetMthlyNRRdata[colnames[i]+'_SoM']

        assetnrrdata = pd.concat([AssetMthlyNRRdata.iloc[:,3], AssetMthlyNRRdata.iloc[:,4]], axis=1)
        AssetAvgReturndata = pd.DataFrame(assetyear, columns=['Date'])
    
        for j in range(0,len(assetyear)):
            dfAsset = assetnrrdata[(assetnrrdata[colnames[i]+'_Year'] == assetyear[j])]
            assetavgreturn = 0
            assetavgreturnval = 0
            for k in range(0,len(dfAsset)):
                assetavgreturn = assetavgreturn + dfAsset.iloc[k,1]
            assetavgreturnval = assetavgreturn/len(dfAsset)
            AssetAvgReturndata.loc[j,colnames[i]+'_AvgRtrn'] = assetavgreturnval
        if(i==1):
            AllAssetAvgReturndata = AssetAvgReturndata
        else:
            AllAssetAvgReturndata = pd.merge(AllAssetAvgReturndata, AssetAvgReturndata, how='left', on='Date')
    return AllAssetAvgReturndata

# Calculate Annualized return using Monthly Net Return rate
# Asset Annualized Returns AAR = ((1+amr1)*(1+amr2)...*(1+amrn))^1/n - 1. amr = asset monthly return
def get_AssetAnnlzdReturn(allassetdata):
    print('Calculating Asset Annualizd Return ...')
    colnames = list(allassetdata.columns)
    assetyear = pd.DatetimeIndex(allassetdata['Date']).year.unique().tolist()
    
    for i in range(1, len(colnames)):
        print('Calculating Annualizd Return for ',colnames[i],'...')
        assetdata = pd.concat([allassetdata.iloc[:,0], allassetdata.iloc[:,i]], axis=1)
        assetdata['Year'] = pd.DatetimeIndex(assetdata['Date']).year
        assetdata['YrMth'] = pd.to_datetime(assetdata['Date']).dt.to_period('M')
        assetdata = assetdata.drop(['Date'],axis=1)
        AssetSoMdata = assetdata.groupby('YrMth').first()
        AssetSoMdata['Date'] = AssetSoMdata.index
        AssetSoMdata.rename(columns={AssetSoMdata.columns[0]:colnames[i]+'_SoM', AssetSoMdata.columns[1]:colnames[i]+'_Year'}, inplace=True)
        AssetEoMdata = assetdata.groupby('YrMth').last()
        AssetEoMdata['Date'] = AssetEoMdata.index
        AssetEoMdata.rename(columns={AssetEoMdata.columns[0]:colnames[i]+'_EoM'}, inplace=True)
        AssetMthlyNRRdata = pd.merge(AssetSoMdata, AssetEoMdata, how='left', on='Date')
        AssetMthlyNRRdata.reset_index(drop=True, inplace=True)
        AssetMthlyNRRdata = AssetMthlyNRRdata.reindex(columns=['Date',colnames[i]+'_SoM',colnames[i]+'_EoM',colnames[i]+'_Year'])
        AssetMthlyNRRdata[colnames[i]+'_NRR'] = (AssetMthlyNRRdata[colnames[i]+'_EoM'] - 
                          AssetMthlyNRRdata[colnames[i]+'_SoM'])/AssetMthlyNRRdata[colnames[i]+'_SoM']

        assetnrrdata = pd.concat([AssetMthlyNRRdata.iloc[:,3], AssetMthlyNRRdata.iloc[:,4]], axis=1)
        AssetAnnlzdReturndata = pd.DataFrame(assetyear, columns=['Date'])
    
        for j in range(0,len(assetyear)):
            dfAsset = assetnrrdata[(assetnrrdata[colnames[i]+'_Year'] == assetyear[j])]
            assetannlzdreturn = 1
            assetannlzdreturnval = 0
            for k in range(0,len(dfAsset)):
                assetannlzdreturn = assetannlzdreturn * (1+dfAsset.iloc[k,1])
            assetannlzdreturnval = pow(assetannlzdreturn,(1/len(dfAsset))) - 1
            AssetAnnlzdReturndata.loc[j,colnames[i]+'_AnnlzdRtrn'] = assetannlzdreturnval
        if(i==1):
            AllAssetAnnlzdReturndata = AssetAnnlzdReturndata
        else:
            AllAssetAnnlzdReturndata = pd.merge(AllAssetAnnlzdReturndata, AssetAnnlzdReturndata, how='left', on='Date')
    return AllAssetAnnlzdReturndata
