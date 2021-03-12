#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 10:00:05 2020

@author: nitinsinghal
"""

# Chapter 3 - Exponential, Logarithm

import numpy as np
import matplotlib.pyplot as plt

#Exponentials
x = np.linspace(-4,4,num=40)

expnx = np.exp(x)
exp2x = np.power(2,x)

plt.plot(x, expnx, label='e^x')
plt.plot(x, exp2x, label='2^x')
plt.legend(loc='upper left')
plt.xlabel('x')
plt.ylabel('e^x, 2^x')
plt.title('Exponential Curve')
plt.show()

#Logarithms
logx = np.log(x)
log10x = np.log10(x)

plt.plot(logx, label='log e(x)')
plt.plot(log10x, label='log 10(x)')
plt.legend(loc='upper left')
plt.xlabel('x')
plt.ylabel('log e(x), log 10(x)')
plt.title('Logarithmic Curve')
plt.show()



