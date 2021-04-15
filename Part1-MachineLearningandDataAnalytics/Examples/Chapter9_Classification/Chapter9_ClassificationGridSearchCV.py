#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:02:02 2021

@author: nitinsinghal
"""
    
# Chapter 9 - Supervised Learning - Classification
# Selecting the Best classifier with tuned hyperparameters using Pipeline and GridSearchCV

#Import libraries
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler #OneHotEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import datetime
import warnings
warnings.filterwarnings('ignore')

# Use the data science process steps given in chapter 6 to build the Classification model
# Classification models being distance based require standardization (scaling) of data

# Import the data
data = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/nbarookie5yrsinleague.csv')

# view top 5 rows for basic EDA
print(data.head())

# Data wrangling to replace NaN with 0, drop duplicate rows
data.fillna(0, inplace=True)
data.drop_duplicates(inplace=True)

# Split the data into depdendent y and independent X variables
X = data.iloc[:, 1:-1].values
y = data.iloc[:, -1:].values

# As y is a column vector and the algorithm expects a 1D array (n,)
# we need to reshape the array using ravel()
y = y.ravel()

# Encode the catgorical data (text or non-numeric data needs to be converted into a binary matrix of ‘n’ categories)
# encoder = OneHotEncoder(drop='first', sparse=False, handle_unknown='error')
# X_encoded = encoder.fit_transform(X)

# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Scale (Standardize) the X values as large values can skew the results by giving them higher weights
# As most estimators expect the data to be normally distributed (mean 0 variance =1)
# Fit the scaler to the training data and and transform it using the calculated mean and variance 
# No need to fit the test data as it should use the same mean and variance as the test data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

####### Create the pipeline to run gridsearchcv for best classifier and hyperparameters ########
pipe_lrc = Pipeline([('clf', LogisticRegression())])

pipe_svc = Pipeline([('clf', SVC())])

pipe_gnb = Pipeline([('clf', GaussianNB())])

pipe_knn = Pipeline([('clf', KNeighborsClassifier())])

pipe_rfc = Pipeline([('clf', RandomForestClassifier())])

pipe_xgb = Pipeline([('clf', XGBClassifier())])

# Set grid search params
grid_params_lrc = [{'clf__solver' : ['lbfgs', 'liblinear'], 
                   'clf__C' : [0.001,0.01]}]

grid_params_svc = [{'clf__kernel' : ['linear','rbf'],
                    'clf__C' : [0.1,0.5]}]

grid_params_gnb = [{}]


grid_params_knn = [{'clf__n_neighbors' : [20,50],
                    'clf__weights' : ['uniform', 'distance']}]

grid_params_rfc = [{'clf__n_estimators' : [200],
                    'clf__min_samples_split' : [2],
                    'clf__min_samples_leaf' : [1,2],
                    'clf__max_features' : ['auto','log2'],
                    'clf__random_state' : [42]}]

grid_params_xgb = [{'clf__objective' : ['binary:logitraw','binary:hinge'],
                    'clf__lambda' : [1,2]}]

# Create grid search
gs_lrc = GridSearchCV(estimator=pipe_lrc,
                     param_grid=grid_params_lrc,
                     scoring='accuracy',
                     cv=10,
                     n_jobs=-1)

gs_svc = GridSearchCV(estimator=pipe_svc,
                      param_grid=grid_params_svc,
                      scoring='accuracy',
                      cv=10,
                      n_jobs=-1)

gs_gnb = GridSearchCV(estimator=pipe_gnb,
                      param_grid=grid_params_gnb,
                      scoring='accuracy',
                      cv=10,
                      n_jobs=-1)

gs_knn = GridSearchCV(estimator=pipe_knn,
                      param_grid=grid_params_knn,
                      scoring='accuracy',
                      cv=10,
                      n_jobs=-1)

gs_rfc = GridSearchCV(estimator=pipe_rfc,
                      param_grid=grid_params_rfc,
                      scoring='accuracy',
                      cv=10,
                      n_jobs=-1)

gs_xgb = GridSearchCV(estimator=pipe_xgb,
                      param_grid=grid_params_xgb,
                      scoring='accuracy',
                      cv=10,
                      n_jobs=-1)

# List of grid pipelines
grids = [gs_lrc, gs_svc, gs_gnb, gs_knn, gs_rfc, gs_xgb] 
# Grid dictionary for pipeline/estimator
grid_dict = {0:'LogisticRegressionClassifier', 1: 'SupportVectorClassifier', 2:'GaussianNaiveBayesClassifier', 3:'KNNClassifier', 
             4:'RandomForestClassifier', 5:'XGBoostClassifier'}

# Fit the pipeline of estimators using gridsearchcv
print('Fitting the gridsearchcv to pipeline of estimators...')
resulterrorgrid = {}

for gsid,gs in enumerate(grids):
    print('\nEstimator: %s. Start time: %s' %(grid_dict[gsid], datetime.datetime.now()))
    gs.fit(X_train, y_train)
    print('\n Best score : %.5f' % gs.best_score_)
    print('\n Best grid params: %s' % gs.best_params_)
    y_pred = gs.predict(X_test)
    # Accuracy score
    accscore = accuracy_score(y_test, y_pred)
    print('accuracy_score: ', accscore)
    # Accuracy metrics
    accmetrics = classification_report(y_test, y_pred)
    print('classification_report: \n', accmetrics)
    # Calculate and plot the confusion matrix for predicted vs test class labels
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    resulterrorgrid[grid_dict[gsid]+'_best_params'] = gs.best_params_
    resulterrorgrid[grid_dict[gsid]+'_best_score'] = gs.best_score_
    resulterrorgrid[grid_dict[gsid]+'_accscore'] = accscore
    resulterrorgrid[grid_dict[gsid]+'_accmetrics'] = accmetrics
    resulterrorgrid[grid_dict[gsid]+'_cm'] = cm
    
print('result grid: ', resulterrorgrid)




