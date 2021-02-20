#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:31:39 2021

@author: nitinsinghal
"""
# Chapter 1 – Programming – Python
# Read/Write

#Console read/write
username = input('Enter username: ')
print('Username is: ', username)

#File read/write
file = open('/users/nitinsinghal/Downloads/rwtest.txt', 'w')
file.write('Creating the text file with some text...')
file.close()

file = open('/users/nitinsinghal/Downloads/rwtest.txt', 'r')
print(file.read())
file.close()

file = open('/users/nitinsinghal/Downloads/rwtest.txt', 'a')
file.write('\n Writing more text to the file...')
file.close()

file = open('/users/nitinsinghal/Downloads/rwtest.txt', 'r')
print(file.read())
file.close()


#MySQL databse connect, read/write commands
import mysql.connector
cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="passwd",
  database="localdb"
)

cursor = cnx.cursor()

cursor.execute("CREATE TABLE Users (username VARCHAR(255), password VARCHAR(255))")
cursor.execute("INSERT INTO Users (username, password) VALUES ('Tom','jerry3')")
cursor.execute("INSERT INTO Users (username, password) VALUES ('Jerry','tom1')")
cursor.execute("SELECT * FROM Users")
userdata = cursor.fetchall();  
print(userdata)
# close the cursor and disconnect from the server
cursor.close()
cnx.close() 
