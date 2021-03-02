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
print(myset)
print(myset[0])

myset.add('rat')
print(myset)

myset.remove('cow')
print(myset)

print(myset.pop())

myset.add('cat')
print(myset)

#Tuples
mytuple = (2,4,6,8)
print(mytuple)
print(mytuple[1])

mytuple.remove(2)
mytuple.add(10)
mytuple.pop()


#Dictionary
mydictionary = {'Name': 'Tom', 'Age': '22', 'City': 'London'}
for key, value in mydictionary.items():
    print(key, value)
for value in mydictionary.values():
    print(value)

mydictionary.get('Name')

mydictionary.update({'Name':'Jerry'})
print(mydictionary)

mydictionary.pop('Name')
print(mydictionary)

dictcollection = {
    'person1': {'Name': 'Tom', 'Age': '22', 'City': 'London'},
    'person2': {'Name': 'Jerry', 'Age': '24', 'City': 'New York'},
    'person3': {'Name': 'Bruno', 'Age': '26', 'City': 'Paris'}
   }
for key, value in dictcollection.items():
    print(key, value)

