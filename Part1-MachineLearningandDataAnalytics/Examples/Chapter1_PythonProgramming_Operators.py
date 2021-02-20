#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:20:38 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Maths Operators

# Basic
x,y,z = 7, 15, 31
print(x+28)
print(x-y)
print(z/y)
print(y*x)
print(x**3)

# Assignment
x += 23
print(x)
y *= 4
print(y)
z /= 33
print(z)
x %= 11
print(x)
y //= 17
print(y)

# Comparison
x,y,z = 7, 15, 31
print(x == y)
print(x!= y)
print(z > y)
print(x < y)
print(y >= 15)

# Logical or Conditional
print((x == y) and (x != y))
print((x == y) or (x != y))
print(not((z > y) and (y < x)))