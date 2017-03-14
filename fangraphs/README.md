# fsfsnm/fangraphs
### CMSC 122 Group Project
##### Federico Scivittaro, Francesco Scivittaro, Nick McDonnell

### Guide on How the Data Scraper Is Run

Start up the database in the `2013_data directory` by running the below command:

<pre><code>
sqlite3 Overall_sqlcode.sqlite3 -init initdb.sql
</code></pre>

This will construct an `Overall_sqlcode.sqlite3` file. To add the 2013 data to the database, run `python fangraphs2013.py`

Move the database file to `2014_data`, `2015_data`, and `2016_data` respectively, running the below commands to update the database:

<pre><code>
python fangraphs2014.py
python fangraphs2015.py
python fangraphs2016.py 
</code></pre>

The database file is then placed in the base `fangraphs` folder. Finally, in order to input the marcel and regression data, run the command `python fangraphs.py`

This method, while inefficent, helped us set independent ID values for each of the inputs into the database. This file was then manually moved to the django folder to be used by the website.

### Contains

2013_data: directory for scraping and handling 2013 data

2014_data: directory for scraping and handling 2014 data

2015_data: directory for scraping and handling 2015 data

2016_data: directory for scraping and handling 2016 data

fangraphs.py: generates SQLite3 database from Marcels and regression data

final_marcel_projections.csv: file containing 2016 and 2017 Marcels data

Overall_sqlcode.sqlite3: SQLite3 database containing all data necessary for our Django interface and website

predictions_data.csv: file containing our proprietary projections for 2016 and 2017

test.csv: small data file used to test fangraphs.py and the SQL database construction