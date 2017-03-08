import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

def get_soup(url):
    """
    Takes in a url and returns the parsed BeautifulSoup code for that url with
    handling capabilities if the request 'bounces'.
    """

    s = requests.Session()

    retries = Retry(
        total = 10,
        backoff_factor = 0.1,
        status_forcelist = [500, 502, 503, 504]
        )

    s.mount('http://', HTTPAdapter(max_retries = retries))

    return BeautifulSoup(s.get(url).text, 'html.parser')


def get_weightings(year):
    """
    Takes in a year (str or int) and returns a list containing the necessary WOBA
    constants for that year.
    """

    url = 'http://www.fangraphs.com/guts.aspx?type=cn'
    soup = get_soup(url)
    year = str(year)

    headers = soup.find('a', text = 'Season').parent.parent
    correct_weightings = soup.find('td', text = year).parent

    def clean_soup(dirty_soup):
        """
        Takes in a soup element and returns a list of desired strings
        extracted from the soup code.
        """

        new_list = []

        for item in dirty_soup:
            new_list.append(item)

        new_list.pop(0)
        new_list.pop()
        final_list = []

        for item in new_list:
            final_list.append(item.get_text())

        return final_list

    header_list = clean_soup(headers)
    weightings_list = clean_soup(correct_weightings)

    weightings_dict = {}

    for header, weighting in zip(header_list, weightings_list):
        weightings_dict[header] = weighting

    return weightings_dict

def convert_name_to_soup(name):
    """
    Takes a player's name and returns the soup for that player's stats page.
    """

    player_url = ('http://www.espn.com/mlb/players?search={}&alltime=true&statusId=1'
    .format(name))

    try:
        return get_stats_soup(player_url)
    except AttributeError:
        return None
    except:
        raise

def get_stats_soup(url):
    """
    Takes in the url of the players' ESPN bio and returns the soup code for the
    player's stats page.
    """

    player_soup = get_soup(url)
    back_half = player_soup.find('a', text = 'Stats').get('href')
    stats_url = 'http://www.espn.com' + back_half

    return get_soup(stats_url)