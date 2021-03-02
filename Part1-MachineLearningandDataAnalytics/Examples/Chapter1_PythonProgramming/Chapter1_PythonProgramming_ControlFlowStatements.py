#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:27:51 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Control Flow Statements

a = 61
if (a<60):
    print('C')
elif (a<80):
    print('B')
else:
    print('A')

a = 1
while a<5:
    print(a)
    a += 1

words = ['tennis', 'golf', 'football', 'f1']
for word in words:
   print(word)

for a in range(1, 10, 2):
   print(a**2)

#List Comprehension
#Get even numbers
b = []
for a in range(10):
    if(a%2==0):
        b.append(a)
print(b)

b = [a for a in range(10) if(a%2==0)]
print(b)


