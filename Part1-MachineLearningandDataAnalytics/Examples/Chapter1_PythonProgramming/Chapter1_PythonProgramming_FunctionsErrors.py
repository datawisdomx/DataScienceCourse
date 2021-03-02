#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:31:38 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python

#Functions
def multiply_power(x,y):
    a = x*y
    b = x**y
    return a,b

m,n = multiply_power(7,4)
print(m,n)
m,n = multiply_power(100,2)
print(m,n)

m = lambda a,b : a*b
n = lambda a,b : a**b
print(m(7,4))
print(n(7,4))

#Error Handling
#Syntax Error
for x in range(5):
print(x)

#Exception
def sum_division(a,b):
    x = a+b
    y = 5/x
    print(y)

try:
    sum_division(2, -2)
except Exception as e:
    print('Error type, message: ', type(e), e)

