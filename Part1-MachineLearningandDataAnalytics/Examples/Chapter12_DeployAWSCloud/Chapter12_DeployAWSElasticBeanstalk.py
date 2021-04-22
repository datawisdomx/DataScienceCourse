#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:01:42 2021

@author: nitinsinghal
"""
# Chapter 12 - Model Deployment
# Deploying on AWS Cloud using Elastic Beanstalk and flask

# See the Deploying on EB Setup & Settings slides on how to get AWS EB working for python flask application

# Make sure latest pyenv, python, virtualenv, virtualenvwrapper packages are installed
#     $ brew install pyenv
#     $ brew  install python
#     $ pip3 install virtualenv virtualenvwrapper

# EB CLI Installer
# https://github.com/aws/aws-elastic-beanstalk-cli-setup
# 1.1. Prerequisites
#   If you don't have Git, install it
#       $ brew install git
#   Most installation problems on macOS are related to loading and linking OpenSSL and zlib. 
#       brew install zlib openssl readline
#       CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix zlib)/lib"
# 2.1. Clone this repository
#     $ git clone https://github.com/aws/aws-elastic-beanstalk-cli-setup.git
# 4.1. Can I skip the Python installation?
# Yes. If you already have Python installed on your system, after step 2.1., run the following.
#     $ python aws-elastic-beanstalk-cli-setup/scripts/ebcli_installer.py
# Note: To complete installation, ensure `eb` is in PATH. You can ensure this by executing (For zsh, default shell in macos):
#     $ echo 'export PATH="/Users/nitinsinghal/.ebcli-virtual-env/executables:$PATH"' >> ~/.zshenv && source ~/.zshenv

# cp /Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Examples/Chapter12_DeployAWSCloud/Chapter12_DeployAWSElasticBeanstalk.py /Users/nitinsinghal/ebdeploy/ 
# cp /Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Examples/Chapter12_DeployAWSCloud/Procfile /Users/nitinsinghal/ebdeploy/ 

import joblib
import numpy as np
from flask import Flask, request, abort
import json
import logging
import boto3
from botocore.exceptions import ClientError                                                        

s3 = boto3.client('s3')
# response = s3.list_buckets()

# bucket_name = ''
# for bucket in response['Buckets']:
#     bucket_name = bucket["Name"]

object_name = 'RFRegression.model'
file_name = './rfregression.model'
bucket_name = 'elasticbeanstalk-ap-south-1-686429807846'
try:
    response = s3.download_file(bucket_name, object_name, file_name)
except ClientError as e:
    logging.error(e)
    print(e)

# Load the model file
rfmodel = joblib.load('./rfregression.model')

# Create the flask api calls

# Make sure to call Flask class instance 'application as EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route("/")
def index():
    return "Index page of Flask Model Deployment"

@application.route("/hello")
def hello():
    return "Welcome from Flask Model Deployment"

# Get data from POST request and return predicted value
@application.route('/api/predict', methods=['POST'])
def predict():
    if request.is_json:
        jsondata = request.get_json()
        predictedvalue = rfmodel.predict(np.array(json.loads(jsondata)))
        predvalstring = np.array2string(predictedvalue)
    else:
        abort(400)
    return (predvalstring)

if __name__ == "__main__":
    application.run()

