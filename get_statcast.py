# 
# Francesco Scivittaro
# Scraper to grab BaseballSavant information
#

from bs4 import BeautifulSoup  as bs
import requests
import json
import csv

def get_statcast_link(year, minimum_at_bats = 0):
    '''
    Returns a JSON object contaning the statcast data for each player

    Inputs:
        year: The year, 2016 or 2015, for which the statcast data is being collected
        minimum_at_bats: The minimum number of batted ball events necessary
        for a player to be included in the results
    Returns:
        A JSON file
    '''

    assert year == 2016 or year == 2015, "Data only available for 2015 and 2016 seasons" 

    link = ("https://baseballsavant.mlb.com/statcast_leaderboard?year=" + str(year)
    + "&abs=" + str(minimum_at_bats) + "&player_type=batter")

    request = requests.get(link)
    c = request.content
    soup = bs(c, "lxml")

    data_text = soup.find_all("script")[9].text
    data_list = data_text[101:-3]
    obj = json.loads(data_list)

    f = csv.writer(open("statcast_" + str(year) + ".csv", "wt"))

    headers = []
    for i in obj[0].keys():
        headers.append(i)

    f.writerow(headers)

    for json_dict in obj:
        f.writerow([json_dict[headers[0]],
            json_dict[headers[1]],
            json_dict[headers[2]],
            json_dict[headers[3]],
            json_dict[headers[4]],
            json_dict[headers[5]],
            json_dict[headers[6]],
            json_dict[headers[7]],
            json_dict[headers[8]],
            json_dict[headers[9]],
            json_dict[headers[10]],
            json_dict[headers[11]],
            json_dict[headers[12]],
            json_dict[headers[13]],
            json_dict[headers[14]],
            json_dict[headers[15]],
            json_dict[headers[16]],
            json_dict[headers[17]]])
