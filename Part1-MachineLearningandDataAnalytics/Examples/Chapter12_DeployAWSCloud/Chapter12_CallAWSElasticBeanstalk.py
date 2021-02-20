#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 22:05:23 2021

@author: nitinsinghal
"""

# Chapter 12 - Model Call AWS Cloud Elastic Beanstalk 
# Call deployed model from flask webserver API to return predict value as JSON data

import pandas as pd
import requests
import json
import logging
import boto3
from botocore.exceptions import ClientError                                                        

s3 = boto3.client('s3')
response = s3.list_buckets()

bucket_name = ''
for bucket in response['Buckets']:
    bucket_name = bucket["Name"]

object_name = 'USMacro10yrPriceYield.csv'
file_name = './predictdata.csv'
try:
    response = s3.download_file(bucket_name, object_name, file_name)
except ClientError as e:
    logging.error(e)
    print(e)

# Load the data to be used for prediction
predictdata = pd.read_csv('./predictdata.csv')
X = predictdata.iloc[221:222, 1:7].values
y_new = predictdata.iloc[221:222, 7].values

predjsondata = json.dumps(X.tolist())

# Pass the flask webserver ip address (localhost or EB application webserver)
# This can be passed as an argument during the python execution for flexibility

# modelapiurl = 'http://127.0.0.1:5000/api/predict'
modelapiurl = 'http://ebdeploy-app-env.eba-pu4ztqmw.ap-south-1.elasticbeanstalk.com/api/predict'

try:
    response = requests.post(modelapiurl,json=predjsondata)
    if(response.status_code == 200):
        jsondata = response.json()
        print('Model Predicted value: ', jsondata)
    else:
        print('Response Status: ', response.status_code)
except ClientError as e:
    logging.error(e)
    print('Error when calling deployed model file: ', e)
