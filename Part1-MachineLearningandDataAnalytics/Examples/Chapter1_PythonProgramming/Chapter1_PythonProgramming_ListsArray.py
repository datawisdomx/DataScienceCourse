#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:27:51 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Data Structures
# Lists

mylist = [1,3,6,8,9,9,15]
print(mylist)
print(mylist[1])

mylist[5] = 18
print(mylist)

mylist.append(32)
print(mylist)

words = ['car', 'fruit', 'ball']
print(words)
print(words[2])

words.append('book')
print(words)

print(words.pop())
print(words)

combolist = [2,10,78.5,-54.2,'bat','city']
print(combolist)

#Indexing/Slicing
print(mylist[:])
print(mylist[0])

print(mylist[2:4])
print(mylist[3:])
print(mylist[:3])

print(mylist[-2:])
print(mylist[:-4])

print(words[1])
print(words[0:2])
print(words[-2])


#Array - not native. Created using lists
myArray=[[1,2],[3,4],[5,6]]
print(myArray)
print(myArray[0])
print(myArray[0][1])

comboarray = [[1,-9,3.6],['orange','apple'],[-173,0,83.14,'john','sea']]
print(comboarray)
print(comboarray[1])
print(comboarray[2][3])
