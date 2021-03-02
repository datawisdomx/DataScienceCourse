#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:20:37 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# DATA TYPES
# String data types, operations

x = 'Simple'
print(x[0], x[1], x[5])
print(x[6])

texta = '    Test this, SAMPLE string. It has    WORDS and numbers 1,2,3. Has spaces   '
textb = 'Concatenate this to string a'

print(texta[1:10])
print(len(texta))
print(texta.strip())
print(texta.split(','))

print(texta.lower())
print(texta.upper())

print(texta.replace('t','z'))

print(texta+textb)

y = 42
print(type(y))

z = str(y)
print(type(z))

