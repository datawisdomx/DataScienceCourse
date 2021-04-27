#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:25:06 2021

@author: nitinsinghal
"""
# Chapter 14 - End to End project 1 - Build a Roboadvisor
# Predicting Asset prices using diffferent algorithms
# Separate methods for Bonds and other Assets
# Separate methods for prediction using CentralBank Forecast or Actual data

# import libraries
import pandas as pd
import numpy as np
import datetime
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings('ignore')

                    ####### 3 year PREDICTION using Central Bank FORECAST #########

# Predict asset's monthly average price for next 3years using central banks 5MF macro 3 year forecast for US,UK,EU
def get_AssetMthlyPricePredUsingCBFrcst(AllAssetdata, CB5MFActualdata, Macro5MFActualdata):
    colnames = list(AllAssetdata.columns)
    
    print('Forecasting 3 year Forward Prices for each Asset using CentralBank Forecasts ....')
    for i in range(1, len(colnames)):
        assetdata = pd.concat([AllAssetdata.iloc[:,0], AllAssetdata.iloc[:,i]], axis=1)
        # Resample asset price data monthly to calculate the mean
        assetdata.set_index(pd.DatetimeIndex(assetdata['Date']), inplace=True)
        assetdata.drop(['Date'],inplace=True, axis=1)
        assetmthlydata = assetdata.resample('M').mean()
        assetmthlydata['Date'] = assetmthlydata.index
        assetmthlydata['Date'] = pd.to_datetime(assetmthlydata['Date'].dt.strftime('%Y-%m'), format='%Y-%m')
        assetmthlydata.reset_index(drop=True, inplace=True)
        # Use actual macro data before first forecast data month
        CB5MFMergeddata = CB5MFActualdata
        Macro5MFAct = Macro5MFActualdata
        Macro5MFAct = Macro5MFAct[(Macro5MFAct['Date'] < CB5MFMergeddata.head(1)['Date'][0])]
        MergedAssetPred = pd.DataFrame()
        
        # Append one month CBForecast macro to 5MF macro data and predict asset price 
        # Loop till end of CBForecast data
        print('Forecasting for ', colnames[i],' ....')
        
        for j in range(0, len(CB5MFMergeddata)):
            # Append the frst CBForecast macro data row to all macrodata
            appnddate = CB5MFMergeddata.head(1)['Date'][j]
            Macro5MFAct = Macro5MFAct.append(CB5MFMergeddata.head(1), ignore_index=True)
            # Select macro data upto t-1 for predicting asset price for t
            macrocbfdata = Macro5MFAct[(Macro5MFAct['Date'] < appnddate)]
            # Take asset price data upto t-1 for training the model
            assetmthlydata = assetmthlydata[(assetmthlydata['Date'] < appnddate)]
            assetmthlypricedata = assetmthlydata.drop(['Date'], axis=1)
            macromthlydata = macrocbfdata.drop(['Date'], axis=1)
            mergedassetmacro = pd.concat([macromthlydata, assetmthlypricedata], axis=1)
            # Create train test sets. Predict using Random Forest Algorithm
            Xasset = mergedassetmacro.iloc[:, 0:len(mergedassetmacro.columns)-1].values
            yasset = mergedassetmacro.iloc[:,len(mergedassetmacro.columns)-1].values
            X_train, X_test, y_train, y_test = train_test_split(Xasset, yasset, test_size = 0.25)
            rfreg = RandomForestRegressor(n_estimators=1000, criterion='mse', min_samples_leaf=2, max_depth=17,  
                                            min_samples_split=2, max_features='sqrt', random_state=42, n_jobs=-1)
            rfreg.fit(X_train, y_train)
            # Predict next month asset value using latest trained model (t) and CB5MFrcsts macro data for (t+1) 
            X_pred = CB5MFMergeddata.head(1)
            X_pred.drop(['Date'],inplace=True, axis=1)
            rf_pred_nxtmth = rfreg.predict(X_pred)
            asset_predicted = pd.DataFrame([[pd.to_datetime(appnddate), rf_pred_nxtmth[0]]], columns=['Date',colnames[i]])
            MergedAssetPred = MergedAssetPred.append(asset_predicted, ignore_index=True)
            assetmthlydata = assetmthlydata.append(asset_predicted, ignore_index=True)
            # Drop the CBForecast row allready added to all macro data
            CB5MFMergeddata = CB5MFMergeddata.drop(j, axis=0)
        # Build the dataframe to return for all asset's predicted values
        if(i==1):
            AllAssetPreddata = MergedAssetPred
        else:
            AllAssetPreddata = pd.merge(AllAssetPreddata, MergedAssetPred, how='left', on='Date')
    return AllAssetPreddata

# Predict bond's monthly average price and yield for next 3years using central banks 5MF macro 3year forecast for US,UK,EU
def get_BondMthlyPriceYieldPredUsingCBFrcst(BondYieldPricedata, CB5MFActualdata, Macro5MFActualdata):
    bondyieldprice = BondYieldPricedata
    colnames = list(BondYieldPricedata.columns)
    
    print('Forecasting 3 year Forward Prices for each Bond using CentralBank Forecasts ....')
    for i in range(1, len(colnames)):
        bonddata = pd.concat([bondyieldprice.iloc[:,0], bondyieldprice.iloc[:,i]], axis=1)
        # Resample bond price data monthly to calculate the mean
        bonddata.set_index(pd.DatetimeIndex(bonddata['Date']), inplace=True)
        bonddata.drop(['Date'],inplace=True, axis=1)
        bondmthlydata = bonddata.resample('M').mean()
        bondmthlydata['Date'] = bondmthlydata.index
        bondmthlydata['Date'] = pd.to_datetime(bondmthlydata['Date'].dt.strftime('%Y-%m'), format='%Y-%m')
        bondmthlydata.reset_index(drop=True, inplace=True)
        # Use actual macro data before first forecast data month
        CB5MFMergeddata = CB5MFActualdata
        Macro5MFAct = Macro5MFActualdata
        Macro5MFAct = Macro5MFAct[(Macro5MFAct['Date'] < CB5MFMergeddata.head(1)['Date'][0])]
        BondActPreddata = pd.DataFrame()
        
        # Append one month CBForecast macro to 5MF macro data and predict bond price 
        # Loop till end of CBForecast data
        print('Forecasting for ', colnames[i],' ....')
        
        for j in range(0, len(CB5MFMergeddata)):
            # Append the frst CBForecast macro data row to all macrodata
            appnddate = CB5MFMergeddata.head(1)['Date'][j]
            Macro5MFAct = Macro5MFAct.append(CB5MFMergeddata.head(1), ignore_index=True)
            
            # Select macro data upto t-1 for predicting bond price for t
            macrocbfdata = Macro5MFAct[(Macro5MFAct['Date'] < appnddate)]
            
            # Take asset price data upto t-1 for training the model
            bondmthlydata = bondmthlydata[(bondmthlydata['Date'] < appnddate)]
            bondmthlytmin1data = bondmthlydata.drop(['Date'], axis=1)
            macromthlydata = macrocbfdata.drop(['Date'], axis=1)
            mergedbondmacro = pd.concat([macromthlydata, bondmthlytmin1data], axis=1)
            
            # Create train test sets. Predict using Random Forest Algorithm
            Xbond = mergedbondmacro.iloc[:, 0:len(mergedbondmacro.columns)-1].values
            ybond = mergedbondmacro.iloc[:,len(mergedbondmacro.columns)-1].values
            X_train, X_test, y_train, y_test = train_test_split(Xbond, ybond, test_size = 0.25)
            rfreg = RandomForestRegressor(n_estimators=1000, criterion='mse', min_samples_leaf=2, max_depth=17,  
                                            min_samples_split=2, max_features='sqrt', random_state=42, n_jobs=-1)
            rfreg.fit(X_train, y_train)
            # Predict next month bond value using latest trained model (t) and CB5MFrcsts macro data for (t+1) 
            X_pred = CB5MFMergeddata.head(1)
            X_pred.drop(['Date'],inplace=True, axis=1)
            rf_pred_nxtmth = rfreg.predict(X_pred)
            bond_predicted = pd.DataFrame([[pd.to_datetime(appnddate), rf_pred_nxtmth[0]]], columns=['Date',colnames[i]])
            BondActPreddata = BondActPreddata.append(bond_predicted, ignore_index=True)
            bondmthlydata = bondmthlydata.append(bond_predicted, ignore_index=True)
            # Drop the CBForecast row allready added to all macro data
            CB5MFMergeddata = CB5MFMergeddata.drop(j, axis=0)
        # Build the dataframe to return for all bond's predicted values
        if(i==1):
            AllBondPreddata = BondActPreddata
        else:
            AllBondPreddata = pd.merge(AllBondPreddata, BondActPreddata, how='left', on='Date')
    AllBondPreddata.fillna(0, inplace=True)
    return AllBondPreddata

                ###### Get PREDICTED PRICES for ALL ASSETS using ACTUAL data #######

# Predict asset's monthly average price using actual historical Macro data (5MF/All) for US,UK,EU
# Use macro and asset data uptil t-2 to train. Then t-1 macro data to predict asset price for t
# Return predicted, actual, difference and accuracy data 
def get_AssetMthlyPricePredUsingMacroActual(AllAssetdata, Macro5MFActualdata):
    colnames = list(AllAssetdata.columns)
    
    print('Forecasting Prices for each Asset using Actual historical data ....')
    for i in range(1, len(colnames)):
        assetdata = pd.concat([AllAssetdata.iloc[:,0], AllAssetdata.iloc[:,i]], axis=1)
        # Resample asset price data monthly to calculate the mean
        assetdata.set_index(pd.DatetimeIndex(assetdata['Date']), inplace=True)
        assetdata.drop(['Date'],inplace=True, axis=1)
        assetmthlydata = assetdata.resample('M').mean()
        assetmthlydata['Date'] = assetmthlydata.index
        assetmthlydata['Date'] = pd.to_datetime(assetmthlydata['Date'].dt.strftime('%Y-%m'), format='%Y-%m')
        assetmthlydata.reset_index(drop=True, inplace=True)
        # Use actual macro data 
        Macro5MFAct = Macro5MFActualdata
        AssetActPreddata = pd.DataFrame()
       
        # Use 5MF all macro & asset data upto t-2 to train and t-1 macro data to predict t asset price 
        # Loop in reverse, start at last month, drop 1 month each time
        # Till last 1 year (1999) of Macro data is left
        print('Forecasting for ', colnames[i],' ....')
        
        for j in range(len(Macro5MFActualdata)-1, 11, -1):
            # Drop last macro data row from allmacrodata
            traincutoffdate = Macro5MFAct.loc[j-2, 'Date']
            macropreddate = Macro5MFAct.loc[j-1, 'Date']
            assetpreddate = Macro5MFAct.loc[j, 'Date']
            
            # Select macro and asset data upto t-2 for training the model 
            macro5mftraindata = Macro5MFAct[(Macro5MFAct['Date'] <= traincutoffdate)]
            assetmthlytraindata = assetmthlydata[(assetmthlydata['Date'] <= traincutoffdate)]
            assetmthlypricedata = assetmthlytraindata.drop(['Date'], axis=1)
            macromthlydata = macro5mftraindata.drop(['Date'], axis=1)
            mergedassetmacro = pd.concat([macromthlydata, assetmthlypricedata], axis=1)
            
            # Create train test sets. Predict using Random Forest Algorithm
            Xasset = mergedassetmacro.iloc[:, 0:len(mergedassetmacro.columns)-1].values
            yasset = mergedassetmacro.iloc[:,len(mergedassetmacro.columns)-1].values
            X_train, X_test, y_train, y_test = train_test_split(Xasset, yasset, test_size = 0.25)
            rfreg = RandomForestRegressor(n_estimators=1000, criterion='mse', min_samples_leaf=2, max_depth=17,  
                                            min_samples_split=2, max_features='sqrt', random_state=42, n_jobs=-1)
            rfreg.fit(X_train, y_train)
            
            # Take macro data for t-1 to predict asset price for t, using trained model (t-2)
            X_pred = Macro5MFAct[(Macro5MFAct['Date'] == macropreddate)]
            X_pred.drop(['Date'],inplace=True, axis=1)
            rf_pred_t = rfreg.predict(X_pred)
            asset_act_t = assetmthlydata[(assetmthlydata['Date'] == assetpreddate)]
    
            asset_pred_t = pd.DataFrame([[assetpreddate, rf_pred_t[0], asset_act_t.iloc[0,0]]], 
                                        columns=['Date',colnames[i]+'_Pred',colnames[i]+'_Act'])
            AssetActPreddata = AssetActPreddata.append(asset_pred_t, ignore_index=True)    
            # Drop the last (t-1) macrodata row used for prediction
            Macro5MFAct = Macro5MFAct.drop(j, axis=0)
        # Build the dataframe to return for all asset's predicted values
        if(i==1):
            AllAssetActPreddata = AssetActPreddata
        else:
            AllAssetActPreddata = pd.merge(AllAssetActPreddata, AssetActPreddata, how='left', on='Date')
    return AllAssetActPreddata


# Predict bond's monthly average price and yield using actual historical Macro (5MF/All)data for US,UK,EU
# Use macro and asset data uptil t-2 to train. Then t-1 macro data to predict asset price for t
# Return predicted, actual, difference and accuracy data 
def get_BondMthlyPriceYieldPredUsingMacroActual(bondyieldpricedata, Macro5MFActualdata):
    bondyieldprice = bondyieldpricedata
    colnames = list(bondyieldpricedata.columns)

    print('Forecasting Prices for each Bond using Actual historical data ....')
    for i in range(1, len(colnames)):
        bonddata = pd.concat([bondyieldprice.iloc[:,0], bondyieldprice.iloc[:,i]], axis=1)
        # Resample bond price data monthly to calculate the mean
        bonddata = bonddata[~bonddata.eq(0).any(1)]
        bonddata.reset_index(drop=True, inplace=True)
        bonddata.set_index(pd.DatetimeIndex(bonddata['Date']), inplace=True)
        bonddata.drop(['Date'],inplace=True, axis=1)
        bondmthlydata = bonddata.resample('M').mean()
        bondmthlydata['Date'] = bondmthlydata.index
        bondmthlydata['Date'] = pd.to_datetime(bondmthlydata['Date'].dt.strftime('%Y-%m'), format='%Y-%m')
        bondmthlydata.reset_index(drop=True, inplace=True)
        # Use actual macro data
        allmacrovaliddata = Macro5MFActualdata[pd.to_datetime(Macro5MFActualdata['Date']) >= bondmthlydata.loc[0,'Date']]
        MacroAct = allmacrovaliddata
        MacroAct.reset_index(drop=True, inplace=True)
        BondActPreddata = pd.DataFrame()
        
        # Use all macro & bond data upto t-2 to train and t-1 macro data to predict t bond price 
        # Loop in reverse, start at last month, drop 1 month each time
        # Till last 1 year (1999 or mth/year for which bond price are not 0) of Macro data is left
        print('Forecasting for ', colnames[i],' ....')
        
        for j in range(len(allmacrovaliddata)-1, 11, -1):
            # Drop last macro data row from allmacrodata
            traincutoffdate = MacroAct.loc[j-2, 'Date']
            macropreddate = MacroAct.loc[j-1, 'Date']
            bondpreddate = MacroAct.loc[j, 'Date']
            
            # Select macro and bond data upto t-2 for training the model 
            macro5mftraindata = MacroAct[(MacroAct['Date'] <= traincutoffdate)]
            bondmthlytraindata = bondmthlydata[(bondmthlydata['Date'] <= traincutoffdate)]
            bondmthlypriceylddata = bondmthlytraindata.drop(['Date'], axis=1)
            macromthlydata = macro5mftraindata.drop(['Date'], axis=1)
            mergedbondmacro = pd.concat([macromthlydata, bondmthlypriceylddata], axis=1)
            
            # Create train test sets. Predict using Random Forest Algorithm
            Xbond = mergedbondmacro.iloc[:, 0:len(mergedbondmacro.columns)-1].values
            ybond = mergedbondmacro.iloc[:,len(mergedbondmacro.columns)-1].values
            X_train, X_test, y_train, y_test = train_test_split(Xbond, ybond, test_size = 0.25)
            rfreg = RandomForestRegressor(n_estimators=1000, criterion='mse', min_samples_leaf=2, max_depth=17,  
                                            min_samples_split=2, max_features='sqrt', random_state=42, n_jobs=-1)
            rfreg.fit(X_train, y_train)
            
            # Take macro data for t-1 to predict bond price for t, using trained model (t-2)
            X_pred = MacroAct[(MacroAct['Date'] == macropreddate)]
            X_pred.drop(['Date'],inplace=True, axis=1)
            rf_pred_t = rfreg.predict(X_pred)
            bond_act_t = bondmthlydata[(bondmthlydata['Date'] == bondpreddate)]
            
            bond_pred_t = pd.DataFrame([[bondpreddate, rf_pred_t[0], bond_act_t.iloc[0,0]]], 
                                        columns=['Date',colnames[i]+'_Pred',colnames[i]+'_Act'])
            BondActPreddata = BondActPreddata.append(bond_pred_t, ignore_index=True)
            
            # Drop the last (t-1) macrodata row used for prediction
            MacroAct = MacroAct.drop(j, axis=0)
        # Build the dataframe to return for all bond's predicted values
        if(i==1):
            AllBondActPreddata = BondActPreddata
        else:
            AllBondActPreddata = pd.merge(AllBondActPreddata, BondActPreddata, how='left', on='Date')
    AllBondActPreddata.fillna(0, inplace=True)
    return AllBondActPreddata

####### Create the pipeline to run gridsearchcv for best estimator and hyperparameters ########
def get_GridSearchHyperParams(X_train, X_test, y_train, y_test):
    
    pipe_rf = Pipeline([('rgr', RandomForestRegressor(random_state=42))])
    
    pipe_xgb = Pipeline([('rgr', XGBRegressor(objective ='reg:squarederror'))])
    
    # Set grid search params
    grid_params_rf = [{'rgr__n_estimators' : [1000],
                       'rgr__criterion' : ['mse'], 
                       'rgr__min_samples_leaf' : [2,3,4], 
                       'rgr__max_depth' : [16,17,18],
                       'rgr__min_samples_split' : [2,3,4],
                       'rgr__max_features' : ['sqrt', 'log2']}]
    
    grid_params_xgb = [{'rgr__learning_rate' : [0.1,0.2,0.3],
                        'rgr__max_depth' : [3,4,5],
                        'rgr__seed' : [1,2,3]}]
    
    # Create grid search
    gs_rf = GridSearchCV(estimator=pipe_rf,
                         param_grid=grid_params_rf,
                         scoring='neg_mean_squared_error',
                         cv=10,
                         n_jobs=-1)
    
    gs_xgb = GridSearchCV(estimator=pipe_xgb,
                          param_grid=grid_params_xgb,
                          scoring='neg_mean_squared_error',
                          cv=10,
                          n_jobs=-1)
    
    # List of grid pipelines
    grids = [gs_rf, gs_xgb] 
    # Grid dictionary for pipeline/estimator
    grid_dict = {0:'RandomForestRegressor', 1: 'XGBoostRegressor'}
    
    # Fit the pipeline of estimators using gridsearchcv
    print('Fitting the gridsearchcv to pipeline of estimators...')
    mse=0.0
    rmse=0.0
    mae=0.0
    r2 = 0.0
    resulterrorgrid = {}
    
    for gsid,gs in enumerate(grids):
        print('\nEstimator: %s. Start time: %s' %(grid_dict[gsid], datetime.datetime.now()))
        gs.fit(X_train, y_train)
        print('\n Best score : %.5f' % gs.best_score_)
        print('\n Best grid params: %s' % gs.best_params_)
        y_pred = gs.predict(X_test)
        mse = mean_squared_error(y_test , y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test , y_pred)
        r2 = r2_score(y_test , y_pred)
        resulterrorgrid[grid_dict[gsid]+'_best_params'] = gs.best_params_
        resulterrorgrid[grid_dict[gsid]+'_best_score'] = gs.best_score_
        resulterrorgrid[grid_dict[gsid]+'_mse'] = mse
        resulterrorgrid[grid_dict[gsid]+'_rmse'] = rmse
        resulterrorgrid[grid_dict[gsid]+'_mae'] = mae
        resulterrorgrid[grid_dict[gsid]+'_r2'] = r2
        testpreddiff = np.sort(y_pred-y_test, kind='quicksort')
        testpreddiffpct = np.sort((y_pred-y_test)/y_pred, kind='quicksort')
        resulterrorgrid[grid_dict[gsid]+'_testpreddiff'] = testpreddiff
        resulterrorgrid[grid_dict[gsid]+'_testpreddiffpct'] = testpreddiffpct
        print('\n Test set accuracy for best params MSE:%.4f, RMSE:%.4f, MAE:%.4f, R2:%.4f' 
              %(mse, rmse, mae, r2))
    
    return resulterrorgrid

