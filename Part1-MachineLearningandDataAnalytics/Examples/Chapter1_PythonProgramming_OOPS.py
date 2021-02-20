#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:31:39 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python

# OOPs - Classes, Objects, Inheritance
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    def details(self):
        print('Book title is: %s and author is: %s' %(self.title, self.author))
    def published(self, date):
        print('Book title is: %s and published date is: %s' %(self.title, date))

class Fiction(Book):
    def book_category(self, category):
        print('Book title is: %s and category is: %s' %(self.title, category))

comicbook = Book('Tintin','Herge')

print(comicbook.details())
print(comicbook.published(1942))
print(isinstance(comicbook, Book))

fictionbook = Fiction('Foundation', 'Arthur C Clarke')
print(fictionbook.details())
print(fictionbook.book_category('Science Fiction'))
print(isinstance(fictionbook, Book))


# Module1.py  
print('Module1 __name__ = %s' %(__name__))
if __name__ == "__main__": 
    print('Module1 is executed')
else: 
    print('Module1 is imported')

# Module2.py   
import Module1 
print ('Module2 __name__ = %s' %(__name__))
if __name__ == "__main__": 
    print('Module2 is executed')
else: 
    print('Module2 is imported')

# python Module1.py

# python Module2.py
