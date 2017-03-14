# fsfsnm
### CMSC 122 Group Project
##### Federico Scivittaro, Francesco Scivittaro, Nick McDonnell

Our goal is to use process-driven data to forecast future performance for baseball players, as opposed to current methods that use results-driven data such as batting average or home runs. To accomplish this, we will scrape player statistics, both process-driven and results-driven, from websites such as Statcast and FanGraphs and then conduct regression analyses to find which process-driven statistics have the greatest predictive value for forecasting future performance. We will then use that data to create forecasting tools and predict future performance, comparing our effectiveness to that of the classical results-driven forecasting systems.

fangraphs: direcory containing FanGraphs scraping tools and FanGraphs data

find_all_marcels.py: functions for creating and filling files with Marcel projections

get_statcast.py: scrapes BaseballSavant and stores data in a csv file

historical_marcels.db: a SQLite database containing historical Marcels data we did not project

hot-bat: root Django directory

linear-model: directory containing our files for our proprietary projections model

marcel-data: directory containing historical Marcels csv files taken from Baseball Heat Maps

marcel_projector.py: Calculates a Marcel projection for a given player for a given year

presentations: directory containing presentation materials

scraping_util.py: utility functions to help with web scraping and wOBA measurements

statcast_2015.csv: file containing batters' 2015 Statcast data

statcast_2016.csv: file containing battters' 2016 Statcast data