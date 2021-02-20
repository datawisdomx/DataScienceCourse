#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 17:35:10 2021

@author: nitinsinghal
"""

# Chapter 4 - Probability

import numpy as np
import random

#Central Limit Theorem
# 0 - Head, 1 - Tail
n = [10,100,1000,10000,100000,1000000,10000000]
result = []
for j in range(len(n)):
    for i in range(1,n[j]):
        toss = random.choice([0,1])
        result.append(toss)
    print(n[j], ' tosses - ', 'Heads:', result.count(0), 'Tails:', result.count(1), 
          'Head %:', result.count(0)/n[j])
