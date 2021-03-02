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
x,y,z = 7, 15, 31
x = x + 23
x += 23
print(x)

y = y * 4
y *= 4
print(y)

z = z / 33
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
print(y >= 15)

a,b,c = 'red', 'blue', 'red'
print(a == c)
print(a!= b)
print(a < b)

# Logical or Conditional
x,y,z = 8, 8, 51
print((x == y) and (x != z))
print((x == y) or (x != z))
print((x == y) and (x == z))
print(not((z > y) and (z > x)))

