#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:27:51 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Data Structures

#Dictionary
mydictionary = {'Name': 'Tom', 'Age': '22', 'City': 'London'}
for key, value in mydictionary.items():
    print(key, value)
for value in mydictionary.values():
    print(value)
mydictionary.get('Name')
mydictionary.update({'Name':'Jerry'})
mydictionary
mydictionary.pop('Name')
mydictionary

dictcollection = {
    'person1': {'Name': 'Tom', 'Age': '22', 'City': 'London'},
    'person2': {'Name': 'Jerry', 'Age': '24', 'City': 'New York'},
    'person3': {'Name': 'Bruno', 'Age': '26', 'City': 'Paris'}
   }
for key, value in dictcollection.items():
    print(key, value)

#Array
myArray=[[1,2],[3,4]]
print(myArray[0])
print(myArray[0][1])
