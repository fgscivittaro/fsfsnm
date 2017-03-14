Guide on How the Data Scraper Is Run:

Start Up the Database in 2013_data directory by running the below command:

sqlite3 Overall_sqlcode.sqlite3 -init initdb.sql

This will construct an Overall_sqlcode.sqlite3 file.

To add the 2013 data to the database you run the command

python fangraphs2013.py

Then can move the Database file to 2014_data, 2015_data, 2016_data respectively
running the below commands to update the database

python fangraphs2014.py, python fangraphs2015.py, python fangraphs2016.py 

Then the file database is placed in the base fangraphs folder

Finally, in order to input the marcel and regression data, you run the command
below

python fangraphs.py 

This method, while terribly inefficent, helped me set independent id values for
each of the inputs into the database. This file was then manually moved to
the django folder to be used by the website