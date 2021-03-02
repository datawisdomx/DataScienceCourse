#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:13:54 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# OOPs - Classes, Objects, Inheritance

# Module2.py   
import sys
sys.path.append('/Users/nitinsinghal/DataScienceCourse/Part1-MachineLearningDataAnalytics/Examples/Chapter1_PythonProgramming/')

import Module1

print ('Module2 __name__ = %s' %(__name__))
if __name__ == "__main__": 
    print('Module2 is executed')
else: 
    print('Module2 is imported')

