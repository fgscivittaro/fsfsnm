import csv
import sqlite3
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

## Marcel Data

Marcel = list(csv.reader(open('final_marcel_projections.csv','r')))

## Regression Data

Regression = list(csv.reader(open('wOBA_predictions.csv','r')))



m =  Marcel
r = Regression

for i in range(len(r)):
    r[i].pop(0)

identi = 15990

for player in r:
    player.insert(0,identi)
    identi += 1


for player in m:
    player.insert(0,identi)
    identi +=1



## connecting to the database

# https://docs.python.org/3/library/sqlite3.html

connection = sqlite3.connect('Overall_sqlcode.sqlite3')

cursor = connection.cursor()

# import pdb; pdb.set_trace();
# sqlite3 2016_sqlcode.sqlite3 -init initdb.sql

cursor.executemany("INSERT INTO marcel VALUES (?,?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", m)
cursor.executemany("INSERT INTO regression VALUES (?,?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?)", r)

# Save / commit changes
connection.commit()

# close the connection
connection.close()


# Number of shifts, 
# batted ball data, 
# 2015 stats, 2014 stats
