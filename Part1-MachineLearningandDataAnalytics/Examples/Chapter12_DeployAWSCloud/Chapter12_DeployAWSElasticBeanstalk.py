#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:01:42 2021

@author: nitinsinghal
"""
# Chapter 12 - Model Deployment
# Deploying model and REST API's on AWS Cloud using Elastic Beanstalk, S3, flask and uWSGI

# See the Deploying on EB Setup & Settings slides on how to get AWS EB working for python flask application
# Make sure latest pyenv, python, virtualenv, virtualenvwrapper packages are installed
# EB CLI Installer - https://github.com/aws/aws-elastic-beanstalk-cli-setup

import joblib
import numpy as np
from flask import Flask, request, abort
import json
import logging
import boto3
from botocore.exceptions import ClientError                                                        

s3 = boto3.client('s3')

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
    return "Home page of DataWisdomX's Data Science Course Model Deployment on Elastic Beanstalk"

@application.route("/hello")
def hello():
    return "Welcome from Data Science Course Model Deployment on Elastic Beanstalk"

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

