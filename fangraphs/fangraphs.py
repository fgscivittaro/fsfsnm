#  Marcel and Regression Data adder
'''
Takes Our Regression Data from its csv file as well as the marcel data
and inputs it into the database
'''

import csv
import sqlite3
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

## Marcel Data

Marcel = list(csv.reader(open('final_marcel_projections.csv','r')))

## Regression Data

Regression = list(csv.reader(open('predictions_data.csv','r')))


m =  Marcel
r = Regression
r.pop(0)
m.pop(0)

years = []
for player in range(len(m)):
    years.append([m[player][1], m[player][3]])

for i in range(len(r)):
    r[i].pop(0)

''' This value identi is used to provide a unique id value for each independent
row of data added. This value is increased in each of the following scrapers for
2014,2015, and 2016

Columns were added to the main data in order to distinguish shift data from
non shift data, and to distinguish year value of the data'''

identi = 15990

for player in r:
    player.insert(0,identi)
    identi += 1


for player in m:
    player.insert(0,identi)
    identi +=1


## connecting to the database

'''
This part of the code establishes a connection to our database and then
adds the respective nessecary information to the sql database file
'''
# https://docs.python.org/3/library/sqlite3.html

connection = sqlite3.connect('Overall_sqlcode.sqlite3')

cursor = connection.cursor()

cursor.executemany("INSERT INTO marcel VALUES (?,?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)", m)
cursor.executemany("INSERT INTO regression VALUES (?,?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?)", r)

# Save / commit changes
connection.commit()

# close the connection
connection.close()

