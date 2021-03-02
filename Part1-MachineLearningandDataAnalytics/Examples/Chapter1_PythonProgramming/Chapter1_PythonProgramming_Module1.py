#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:13:53 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Modules, Packages

# Module1.py  

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    def details(self):
        print('Book title is: %s and author is: %s' %(self.title, self.author))
    def published(self, date):
        print('Book title is: %s and published date is: %s' %(self.title, date))

print('Module __name__ = %s' %(__name__))
if __name__ == "__main__": 
    print('Module1 is executed')
else: 
    print('Module1 is imported')


