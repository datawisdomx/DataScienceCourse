#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:20:38 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Variables 

x = 527
val = 629.14
language = 'Python'
print(type(x), type(val), type(language))

a, b, c = 10, 5.3, 120.34
print(a,b,c)

m = x-val
n = a*b/c
print(m,n)

# Datetime
import datetime
currentdate = datetime.datetime.now()
print('current date time is: ', currentdate)
currentdate.strftime('Weekday is %A Day is %d Month is %B Year is %Y Time is %H:%M:%S %p')

newdate = datetime.datetime(2019, 12, 11)
print(newdate)

