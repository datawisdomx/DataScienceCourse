#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:13:54 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Modules, Packages

# Module2.py   
import sys
sys.path.append('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Examples/Chapter1_PythonProgramming/')

import Chapter1_PythonProgramming_Module1 as mod1

print ('Module __name__ = %s' %(__name__))
if __name__ == "__main__": 
    print('Module2 is executed')
else: 
    print('Module2 is imported')


class Book:
    def __init__(self, genre, datepublished):
        self.genre = genre
        self.datepublished = datepublished
    def details(self, title, author):
        print('This is a %s book pubished in %s' %(self.genre,self.datepublished))
        print('Book title is: %s and author is: %s' %(title, author))

# Calling class method from imported module
module1book = mod1.Book('Innovators Dilemma', 'Clayton Christensen')
print('Printing imported module1, class Book, method details() ...')
module1book.details()

print('Printing current module, class Book, method details() ...')
module2book = Book('Business Strategy',2001)
module2book.details('Good To Great', 'Jim Collins')

