#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 22:05:23 2021

@author: nitinsinghal
"""

# Chapter 12 - Model Call AWS Cloud Elastic Beanstalk 
# Call deployed model from Elastic Beanstalk uWSGI webserver REST API to return predict value as JSON data

import pandas as pd
import requests
import json
import logging
import boto3
from botocore.exceptions import ClientError                                                        

s3 = boto3.client('s3')

object_name = 'USMacro10yrPriceYield.csv'
file_name = './predictdata.csv'
bucket_name = 'elasticbeanstalk-ap-south-1-686429807846'

try:
    response = s3.download_file(bucket_name, object_name, file_name)
except ClientError as e:
    logging.error(e)
    print(e)

# Load the data to be used for prediction
newpredictiondata = pd.read_csv('./predictdata.csv')
X = newpredictiondata.iloc[-1:, 1:7].values
y = newpredictiondata.iloc[-1:, 7].values

predjsondata = json.dumps(X.tolist())

# Pass the flask webserver ip address (localhost or EB application webserver)
# This can be passed as an argument during the python execution for flexibility

modelapiurl = 'http://ebdsmodeldeploy1-dev.ap-south-1.elasticbeanstalk.com/api/predict'

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
