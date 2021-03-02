#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:36:03 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python

# Bubble Sort
def sort_bubble(a):
    a = [1,10,6,4,28,21,15]
    for i in range(len(a)):
        swapped = False
        for j in range(len(a)-1):
            if a[j] > a[j+1]:
                tmp = a[j]
                a[j] = a[j+1]
                a[j+1] = tmp
                swapped = True
        if swapped == False:
            break
    return a

x = [1,10,6,4,28,21,15]
y = sort_bubble(x)
print(y)

# Recursion - Factorial
def factorial(a):
    if(a > 1):
        return a * factorial(a-1)
    else:
        return 1

# Factorial 5 = 5*4*3*2*1 = 120
x = 5
factorialno = factorial(x)
print('Factorial of %d is %d' %(x, factorialno))

# RegEx
import re

text = 'Tom is 22 years old. Tom lives on 22 Tom Street'
# ^ string starts with
a = re.search('^Tom',text)
print(a)
# + one or more occurrences of the string 
b = re.search('Age+',text)
print(b)
# all instances of the string
c = re.findall('Tom',text)
print(c)



