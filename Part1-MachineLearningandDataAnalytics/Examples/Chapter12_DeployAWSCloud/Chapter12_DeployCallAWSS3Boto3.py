#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 17:21:38 2021

@author: nitinsinghal
"""
# Chapter 12 - Model Deployment
# Deploying on AWS Cloud S3 using Boto3 API

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html 
# Download the latest Boto3 version in your python environment 
# $ pip install boto3
# Setup your AWS authentication credentials using python commands
# $ aws configure or manually in the file ~/.aws/credentials
# Set aws_access_key_id = YOUR_ACCESS_KEY and aws_secret_access_key = YOUR_SECRET_KEY 
# from your AWS security credentials

# import libraries
import logging
import boto3
from botocore.exceptions import ClientError                          
import pandas as pd                               
import joblib

# Create a client for the S3 service
# Now list all the buckets. Assumed that bucket has already been created in S3
s3 = boto3.client('s3')
response = s3.list_buckets()

# We have created only one bucket so we can use that for bucket name parameter
bucket_name = ''

for bucket in response['Buckets']:
    print(bucket["Name"])
    bucket_name = bucket["Name"]

# Deploy the model file to S3
object_name = 'RFRegression.model'
file_name = '/Users/nitinsinghal/Dropbox/DataScienceCourse/Data/RFRegression.model'

if object_name is None:
        object_name = file_name
try:
    response = s3.upload_file(file_name, bucket_name, object_name)
except ClientError as e:
    logging.error(e)
    print(e)

# Download the model file from S3 into local file
object_name = 'RFRegression.model'
file_name = '/Users/nitinsinghal/Downloads/rfregression.model'
try:
    response = s3.download_file(bucket_name, object_name, file_name)
except ClientError as e:
    logging.error(e)
    print(e)

# Use the model file downloaded from S3 to predict with data from a local file (or download from S3)
usmacro10yrpriceyielddata = pd.read_csv('/Users/nitinsinghal/Dropbox/DataScienceCourse/Data/USMacro10yrPriceYield.csv')
X = usmacro10yrpriceyielddata.iloc[221:222, 1:7].values
y_new = usmacro10yrpriceyielddata.iloc[221:222, 7].values
rfmodel = joblib.load('/Users/nitinsinghal/Downloads/rfregression.model')
predictedvalue = rfmodel.predict(X)
print('Predicted value: ', predictedvalue)


