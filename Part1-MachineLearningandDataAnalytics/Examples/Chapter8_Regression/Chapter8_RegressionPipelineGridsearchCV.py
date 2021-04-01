#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 16:40:00 2021

@author: nitinsinghal
"""
# Chapter 8 - Supervised Learning - Regression - Bond Price prediction using macroeconomic data for US
# Selecting the Best estimator with tuned hyperparameters using Pipeline and GridSearchCV

#Import libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import datetime
import warnings
warnings.filterwarnings('ignore')

# Use the data science process steps given in chapter 6 to build the Regression model
# Data being already cleaned requires minimal pre-processing

# Import Bond Price and macroeconomic data for US
usmacro10yrpriceyielddata = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/USMacro10yrPriceYield.csv')

# Split the data into depdendent y and independent X variables
X = usmacro10yrpriceyielddata.iloc[:, 1:7].values
y = usmacro10yrpriceyielddata.iloc[:, 7].values

# As y is a 1 dimensional array, and the algorithm expects a 2D array
# we need to reshape the array. Using numpy reshape method this can be done easily
y = y.reshape(-1,1)

# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)


####### Create the pipeline to run gridsearchcv for best estimator and hyperparameters ########
pipe_rf = Pipeline([('rgr', RandomForestRegressor())])

pipe_xgb = Pipeline([('rgr', XGBRegressor())])

pipe_mlr = Pipeline([('rgr', LinearRegression())])

pipe_l2 = Pipeline([('rgr', Ridge())])

pipe_l1 = Pipeline([('rgr', Lasso())])

# Set grid search params
grid_params_rf = [{'rgr__n_estimators' : [100,200],
                   'rgr__criterion' : ['mse'], 
                   'rgr__min_samples_leaf' : [1,2], 
                   'rgr__max_depth' : [10,11],
                   'rgr__min_samples_split' : [2,3],
                   'rgr__max_features' : ['sqrt', 'log2'],
                   'rgr__random_state' : [42]}]

grid_params_xgb = [{'rgr__objective' : ['reg:squarederror'],
                    'rgr__learning_rate' : [0.1,0.3],
                    'rgr__max_depth' : [5,6],
                    'rgr__seed' : [1,2]}]

grid_params_mlr = [{}]

grid_params_l2 = [{'rgr__alpha' : [5,10,20],
                   'rgr__solver' : ['auto','lsqr']}]

grid_params_l1 = [{'rgr__alpha' : [0.1,0.5,1]}]

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

gs_mlr = GridSearchCV(estimator=pipe_mlr,
                      param_grid=grid_params_mlr,
                      scoring='neg_mean_squared_error',
                      cv=10,
                      n_jobs=-1)

gs_l2 = GridSearchCV(estimator=pipe_l2,
                      param_grid=grid_params_l2,
                      scoring='neg_mean_squared_error',
                      cv=10,
                      n_jobs=-1)

gs_l1 = GridSearchCV(estimator=pipe_l1,
                      param_grid=grid_params_l1,
                      scoring='neg_mean_squared_error',
                      cv=10,
                      n_jobs=-1)

# List of grid pipelines
grids = [gs_rf, gs_xgb, gs_mlr, gs_l2, gs_l1] 
# Grid dictionary for pipeline/estimator
grid_dict = {0:'RandomForestRegressor', 1: 'XGBoostRegressor', 2: 'MultipleLinearRegressor', 3: 'L2RidgeRegressor', 4: 'L1LassoRegressor'}

# Fit the pipeline of estimators using gridsearchcv
print('Fitting the gridsearchcv to pipeline of estimators...')
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

print('\n', resulterrorgrid)
