#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:27:51 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Data Structures

#Sets
myset = {'cow', 'cat', 'dog'}
myset.add('rat')
print(myset)
myset.remove('cow')
print(myset)
print(myset[1])

#Tuples
mytuple = (2,4,6,8)
mytuple.remove(2)
mytuple.add(10)
mytuple.pop()
mytuple[1]