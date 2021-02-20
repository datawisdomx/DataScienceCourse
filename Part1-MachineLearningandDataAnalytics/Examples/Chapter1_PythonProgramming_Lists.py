#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:27:51 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Data Structures
# Lists

mylist = [1,2,3,4,5,5,6]
print(mylist[1])
print(mylist[3:])
mylist[6] = 7
mylist[7] = 8
mylist.append(8)
print(mylist)
words = ['car', 'fruit', 'ball']
words.append('book')
print(words)
print(words.pop())
print(words)

#Indexing/Slicing
print(mylist[:])
print(mylist[0])
print(mylist[2:4])
print(mylist[3:])
print(mylist[:3])
print(mylist[-2:])
print(mylist[:-4])