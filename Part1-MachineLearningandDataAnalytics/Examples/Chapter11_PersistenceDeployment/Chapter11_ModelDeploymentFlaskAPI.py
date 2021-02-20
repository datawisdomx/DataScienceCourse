#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 10:26:32 2021

@author: nitinsinghal
"""
# Chapter 11 - Model Deployment
# Deploying ML model to production using Flask, Joblib

# Flask Webserver API setup steps
    # This file can be deployed on a webserver using flask commands from the terminal (command prompt) $
    # Go to the folder containing the flaskapi python file
    # Then execute the below commands on the terminal prompt
    # $ export FLASK_APP=/Chapter14_ModelDeploymentFlaskAPI.py
    # $ flask run
    # The webserver will run on localhost - http://127.0.0.1:5000/
    # Now call the api from deploymentcall python file



import joblib
import numpy as np
from flask import Flask, request, abort
import json

# Load the model file
rfmodel = joblib.load('/Users/nitinsinghal/Dropbox/DataScienceCourse/Data/RFRegression.model')

# Create the flask api calls
app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

# Get data from POST request and return predicted value
@app.route('/api/predict', methods=['POST'])
def predict():
    if request.is_json:
        jsondata = request.get_json()
        predictedvalue = rfmodel.predict(np.array(json.loads(jsondata)))
        predvalstring = np.array2string(predictedvalue)
    else:
        abort(400)
    return (predvalstring)

if __name__ == "__main__":
    app.run(debug = True)


