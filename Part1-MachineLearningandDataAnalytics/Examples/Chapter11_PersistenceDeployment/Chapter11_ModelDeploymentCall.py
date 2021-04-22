#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 17:27:57 2021

@author: nitinsinghal
"""
# Chapter 11 - Model Call
# Call deployed model from flask webserver API to return predict value as JSON data

#/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Examples/Chapter11_PersistenceDeployment/Chapter11_ModelDeploymentCall.py

import pandas as pd
import requests
import json

# Load the data to be used for prediction
newpredictiondata = pd.read_csv('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Data/USMacro10yrPriceYield.csv')
X = newpredictiondata.iloc[-1:, 1:7].values
y = newpredictiondata.iloc[-1:, 7].values

predjsondata = json.dumps(X.tolist())

# Pass the flask webserver ip address (localhost)
# This can be passed as an argument during the python execution for flexibility
modelapiurl = 'http://127.0.0.1:5000/api/predict'

response = requests.post(modelapiurl,json=predjsondata)

if(response.status_code == 200):
    print('Response Status: ', response.status_code)
    jsondata = response.json()
    print('Predicted value: ', jsondata)
