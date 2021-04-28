#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 17:42:54 2021

@author: nitinsinghal
"""
# Chapter 14 - End to End project 1 - Build a Roboadvisor
# Asset Actual vs Predicted Direction Calculator (Long/Short indicator)

#Import libraries
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Direction - Calculate Predicted vs Actual direction of all actual asset/bond prices
def get_AssetBondActualPredictedDirection(acolnames, allassetpredicteddata, bcolnames, allbondtpredicteddata):
    print('\n Calculating all Assets Predicted vs Actual direction ...')
    AllAssetActPredDirection = pd.DataFrame()
    for i in range(1, len(acolnames)):
        AssetActPredDirection = pd.DataFrame()
        for m in range(0, len(allassetpredicteddata)-1):
            AssetActPredDirection.loc[m, 'Date'] = allassetpredicteddata.loc[m,'Date']
            AssetActPredDirection.loc[m, acolnames[i]+'_PredDirDiff'] = allassetpredicteddata.loc[m, acolnames[i]+'_Pred'] - allassetpredicteddata.loc[m+1, acolnames[i]+'_Pred']
            AssetActPredDirection.loc[m, acolnames[i]+'_ActDirDiff'] = allassetpredicteddata.loc[m, acolnames[i]+'_Act'] - allassetpredicteddata.loc[m+1, acolnames[i]+'_Act']
            if(np.sign(AssetActPredDirection.loc[m, acolnames[i]+'_PredDirDiff']) == np.sign(AssetActPredDirection.loc[m, acolnames[i]+'_ActDirDiff'])):
                AssetActPredDirection.loc[m, acolnames[i]+'_ActPredSameDir'] = 1
            else:
                AssetActPredDirection.loc[m, acolnames[i]+'_ActPredSameDir'] = 0
        if(i==1):
            AllAssetActPredDirection = AssetActPredDirection
        else:
            AllAssetActPredDirection = pd.merge(AllAssetActPredDirection, AssetActPredDirection, how='left', on='Date')
    
    AllBondActPredDirection = pd.DataFrame()
    for j in range(1, len(bcolnames)):
        BondActPredDirection = pd.DataFrame()
        for n in range(0, len(allbondtpredicteddata)-1):
            BondActPredDirection.loc[n, 'Date'] = allbondtpredicteddata.loc[n,'Date']
            BondActPredDirection.loc[n, bcolnames[j]+'_PredDirDiff'] = allbondtpredicteddata.loc[n, bcolnames[j]+'_Pred'] - allbondtpredicteddata.loc[n+1, bcolnames[j]+'_Pred']
            BondActPredDirection.loc[n, bcolnames[j]+'_ActDirDiff'] = allbondtpredicteddata.loc[n, bcolnames[j]+'_Act'] - allbondtpredicteddata.loc[n+1, bcolnames[j]+'_Act']
            if(np.sign( BondActPredDirection.loc[n, bcolnames[j]+'_PredDirDiff']) == np.sign(BondActPredDirection.loc[n, bcolnames[j]+'_ActDirDiff'])):
                BondActPredDirection.loc[n, bcolnames[j]+'_ActPredSameDir'] = 1
            else:
                BondActPredDirection.loc[n, bcolnames[j]+'_ActPredSameDir'] = 0
        if(j==1):
            AllBondActPredDirection = BondActPredDirection
        else:
            AllBondActPredDirection = pd.merge(AllBondActPredDirection, BondActPredDirection, how='left', on='Date')
     
    AllAssetBondActPredDirection = pd.merge(AllAssetActPredDirection, AllBondActPredDirection, how='left', on='Date')
    return AllAssetBondActPredDirection

# Calculate Actual data's predicted values difference and % accuracy 
def get_AssetBondMthlyActualPredDiffAcrcy(allassetactualpreddata, allbondactualpreddata, acolnames, bcolnames):
    print('\n Calculating all Assets Actual-Predicted difference and accuracy ...')
    AllAssetActPredDiffAcrcydata = allassetactualpreddata
    for i in range(1, len(acolnames)):
        AllAssetActPredDiffAcrcydata[acolnames[i]+'_ActPredDiff'] = AllAssetActPredDiffAcrcydata[acolnames[i]+'_Act'] - AllAssetActPredDiffAcrcydata[acolnames[i]+'_Pred']
        AllAssetActPredDiffAcrcydata[acolnames[i]+'_ActPredAcrcy'] = (AllAssetActPredDiffAcrcydata[acolnames[i]+'_Act'] - AllAssetActPredDiffAcrcydata[acolnames[i]+'_Pred'])/AllAssetActPredDiffAcrcydata[acolnames[i]+'_Act']
    
    AllBondActPredDiffAcrcydata = allbondactualpreddata
    for j in range(1, len(bcolnames)):
        AllBondActPredDiffAcrcydata[bcolnames[j]+'_ActPredDiff'] = AllBondActPredDiffAcrcydata[bcolnames[j]+'_Act'] - AllBondActPredDiffAcrcydata[bcolnames[j]+'_Pred']
        AllBondActPredDiffAcrcydata[bcolnames[j]+'_ActPredAcrcy'] = (AllBondActPredDiffAcrcydata[bcolnames[j]+'_Act'] - AllBondActPredDiffAcrcydata[bcolnames[j]+'_Pred'])/AllBondActPredDiffAcrcydata[bcolnames[j]+'_Act']
    
    AllAssetBondActPredDiffAcrcydata = pd.merge(AllAssetActPredDiffAcrcydata, AllBondActPredDiffAcrcydata, how='left', on='Date')
    return AllAssetBondActPredDiffAcrcydata

# Calculate Predicted direction of 3yr forecasts of assets/bonds 
def get_AssetBondPredictedDirection(acolnames, allassetspred3yrdata, bcolnames, allbondspred3yrdata):
    print('\n Calculating all Assets Predicted direction of 3yr forecasts...')
    AllAssetPredDirection = pd.DataFrame()
    for i in range(1, len(acolnames)):
        AssetPredDirection = pd.DataFrame()
        for m in range(0, len(allassetspred3yrdata)-1):
            AssetPredDirection.loc[m, 'Date'] = allassetspred3yrdata.loc[m,'Date']
            AssetPredDirection.loc[m, acolnames[i]+'_PredDiff'] = allassetspred3yrdata.loc[m+1, acolnames[i]] - allassetspred3yrdata.loc[m, acolnames[i]]
            if(np.sign(AssetPredDirection.loc[m, acolnames[i]+'_PredDiff']) < 0):
                AssetPredDirection.loc[m, acolnames[i]+'_PredDir'] = -1
            else:
                AssetPredDirection.loc[m, acolnames[i]+'_PredDir'] = 1
        if(i==1):
            AllAssetPredDirection = AssetPredDirection
        else:
            AllAssetPredDirection = pd.merge(AllAssetPredDirection, AssetPredDirection, how='left', on='Date')
    
    AllBondPredDirection = pd.DataFrame()
    for j in range(1, len(bcolnames)):
        BondPredDirection = pd.DataFrame()
        for n in range(0, len(allbondspred3yrdata)-1):
            BondPredDirection.loc[n, 'Date'] = allbondspred3yrdata.loc[n,'Date']
            BondPredDirection.loc[n, bcolnames[j]+'_PredDiff'] = allbondspred3yrdata.loc[n+1, bcolnames[j]] - allbondspred3yrdata.loc[n, bcolnames[j]]
            if(np.sign(BondPredDirection.loc[n, bcolnames[j]+'_PredDiff']) <0 ):
                BondPredDirection.loc[n, bcolnames[j]+'_PredDir'] = -1
            else:
                BondPredDirection.loc[n, bcolnames[j]+'_PredDir'] = 1
        if(j==1):
            AllBondPredDirection = BondPredDirection
        else:
            AllBondPredDirection = pd.merge(AllBondPredDirection, BondPredDirection, how='left', on='Date')
     
    AllAssetBondPredDirection = pd.merge(AllAssetPredDirection, AllBondPredDirection, how='left', on='Date')
    return AllAssetBondPredDirection
