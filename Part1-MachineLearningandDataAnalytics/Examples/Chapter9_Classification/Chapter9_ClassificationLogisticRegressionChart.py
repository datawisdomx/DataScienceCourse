#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:27:05 2020

@author: nitinsinghal
"""
#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10,10,20)
expx = np.exp(-x)
lx = 1/(1+expx)
p=[]
for i in lx: 
    if (i>=0.5):
        p.append(1)
    else:
        p.append(0)

plt.title('Logistic Regression model')
plt.ylabel('Class label of Y')
plt.xlabel('Linear Regression X')
plt.yticks([0,1])
plt.plot(x, lx, color='blue')
plt.scatter(x, p, color='green')
plt.axhline(y=0.5, color='black')
plt.axvline(x=0, color='black')
plt.show()

