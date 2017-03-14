import sqlite3
import re
import numpy as np

from scraping_util import *

def compute_marcel_projection(name, year, db):
    """
    Takes a player's name and computes their Marcel projection for all
    statistics for the year we would like to forecast for.

    Inputs:
        name: (str) the player's name, Firstname Lastname
        year: (int  or str) the future year to project
        db: (str) the SQL database

    Returns: a list containing the player's basic info 
    """

    conn = sqlite3.connect(db)
    c = conn.cursor()

    year = int(year) # If a string is given for year

    one_ya = year - 1
    two_ya = year - 2
    three_ya = year - 3

    one_ya_stats = retrieve_stats(name, one_ya, c)
    two_ya_stats = retrieve_stats(name, two_ya, c)
    three_ya_stats = retrieve_stats(name, three_ya, c)

    league_rates = calculate_league_rates(one_ya, c)

    c.close()
    conn.close()

    if not one_ya_stats and not two_ya_stats and not three_ya_stats:
        final_estimates = round_estimates(league_rates * 200) # We assume 200 PAs

        final_estimates.append(calculate_avg(final_estimates))
        final_estimates.append(calculate_obp(final_estimates))
        final_estimates.append(calculate_slg(final_estimates))
        final_estimates.append(calculate_woba(final_estimates, one_ya))

        final_estimates.insert(0, '0')
        final_estimates.insert(1, name)
        final_estimates.insert(2, 'N/A')
        final_estimates.insert(3, 'N/A')
        final_estimates.insert(4, str(year))
        final_estimates.insert(5, '0')

        return final_estimates

    # Defaults
    third_stats = [0] * 19
    second_stats = [0] * 19
    first_stats = [0] * 19

    weight_3 = 0
    weight_4 = 0
    weight_5 = 0

    three_ya_pa = 0
    two_ya_pa = 0
    one_ya_pa = 0
        
    if three_ya_stats:
        third_stats = weight_stats_by_pa(three_ya_stats[0][4:23])
        three_ya_pa = three_ya_stats[0][6]
        weight_3 = 3
        player_id = three_ya_stats[0][1]
        team = three_ya_stats[0][3]

    if two_ya_stats:
        second_stats = weight_stats_by_pa(two_ya_stats[0][4:23])
        two_ya_pa = two_ya_stats[0][6]
        weight_4 = 4
        player_id = two_ya_stats[0][1]
        team = two_ya_stats[0][3]

    if one_ya_stats:
        first_stats = weight_stats_by_pa(one_ya_stats[0][4:23])
        one_ya_pa = one_ya_stats[0][6]
        weight_5 = 5
        player_id = one_ya_stats[0][1]
        team = one_ya_stats[0][3]

    WEIGHTS = np.array([[5], [4], [3]])
    divisor = weight_5 + weight_4 + weight_3
        
    all_stats = np.array([first_stats, second_stats, third_stats])
    weighted_stats = all_stats * WEIGHTS / divisor
    combined_weighted_stats = np.sum(weighted_stats, axis=0)

    # Scraping for additional data
    url = 'http://www.fangraphs.com/statss.aspx?playerid={}'.format(str(player_id))
    soup = get_soup(url)

    current_age = find_age(soup, year)
    if not current_age:
        current_age = 29

    position = find_position(soup)
    if not position:
        position = 'N/A'

    age_regressed_rates = apply_age_factor(combined_weighted_stats,
                                           current_age)

    rel = calculate_rel(one_ya_pa, two_ya_pa, three_ya_pa)
    final_regressed_rates = rel * age_regressed_rates + (1 - rel) * league_rates

    projected_PAs = 0.5 * one_ya_pa + 0.1 * two_ya_pa + 200

    final_estimates = round_estimates(final_regressed_rates * projected_PAs)

    final_estimates.append(calculate_avg(final_estimates))
    final_estimates.append(calculate_obp(final_estimates))
    final_estimates.append(calculate_slg(final_estimates))
    final_estimates.append(calculate_woba(final_estimates, one_ya))

    final_estimates.insert(0, str(player_id))
    final_estimates.insert(1, name)
    final_estimates.insert(2, position)
    final_estimates.insert(3, team)
    final_estimates.insert(4, str(year))
    final_estimates.insert(5, str(current_age))

    return final_estimates


def retrieve_stats(name, year, c):
    """
    Takes a player's name, year, and a cursor object and retrieves all of his
    stats from that year.

    Inputs:
        name: name of the player to project
        year: the year to find stats for
        c: SQL cursor

    Returns:
        List of tuples of statistics for the given player
    """

    query = """
            SELECT * FROM regular_data
            WHERE name = ?
            AND Year = ?
            AND NOT shift
            AND NOT noshift
            AND NOT trad_shift
            AND NOT nontrad_shift
            """

    inputs = (name, year)

    return c.execute(query, inputs).fetchall()


def weight_stats_by_pa(stats):
    """
    Takes in a year's stats and weights them by plate appearances.

    Inputs: list of stats

    Returns: list of stats weighted by plate appearance
    """

    PA = stats[2]

    weighted_stats = []

    for stat in stats:
        weighted_stats.append(stat / PA)

    return weighted_stats


def calculate_rel(PA1, PA2, PA3):
    """
    Takes in the amount of plate appearances for a player over the past three
    seasons and calculates a reliability factor, which we will use to regress
    the players' statisitcs.

    Inputs:
        PA1: PAs from one year ago
        PA2: PAs from two years ago
        PA3: PAs from three years ago

    Returns: a rel value for the player
    """

    total_weighted_PAs = PA1 * 5 + PA2 * 4 + PA3 * 3

    return total_weighted_PAs / (total_weighted_PAs + 1200)


def calculate_league_rates(one_ya, c):
    """
    Calculates weighted league averages using data from all players from the
    previous three years.

    Inputs:
        one_ya: the year before the one we are projecting for
        c: the SQL cursor

    Returns: a 1D-array of weighted league averages
    """

    two_ya = one_ya - 1
    three_ya = one_ya - 2

    query = """
             SELECT * FROM regular_data
             WHERE Year = ?
             AND NOT shift
             AND NOT noshift
             AND NOT trad_shift
             AND NOT nontrad_shift
             """

    one_ya_stats = c.execute(query, (one_ya,)).fetchall()
    two_ya_stats = c.execute(query, (two_ya,)).fetchall()
    three_ya_stats = c.execute(query, (three_ya,)).fetchall()

    full_one_ya_stats = convert_to_array(one_ya_stats)
    full_two_ya_stats = convert_to_array(two_ya_stats)
    full_three_ya_stats = convert_to_array(three_ya_stats)

    one_ya_pa = create_PA_array(full_one_ya_stats)
    two_ya_pa = create_PA_array(full_two_ya_stats)
    three_ya_pa = create_PA_array(full_three_ya_stats)

    weighted_one_ya_stats = full_one_ya_stats / one_ya_pa * 5 / 12
    weighted_two_ya_stats = full_two_ya_stats / two_ya_pa * 4 / 12
    weighted_three_ya_stats = full_three_ya_stats / three_ya_pa * 3 / 12

    one_ya_averages = (np.sum(weighted_one_ya_stats, axis=0)
                       / len(weighted_one_ya_stats))
    two_ya_averages = (np.sum(weighted_two_ya_stats, axis=0)
                       / len(weighted_two_ya_stats))
    three_ya_averages = (np.sum(weighted_three_ya_stats, axis=0)
                       / len(weighted_three_ya_stats))

    all_averages = np.array([one_ya_averages, two_ya_averages, three_ya_averages])
    
    return np.sum(all_averages, axis=0)


def convert_to_array(stats):
    """
    Takes the list of tuples generated by SQL and converts it into an array.

    Inputs: list of tuples of stats

    Returns: array of stats
    """

    full_stats = []

    for statline in stats:
        one_player = []
        for stat in statline[4:23]:
            one_player.append(stat)
        full_stats.append(one_player)

    return np.array(full_stats)


def create_PA_array(stats):
    """
    Takes in an array of stats and generates an array containing a single
    column of the players' PAs.

    Inputs: list of stats

    Returns: 2D array of PAs
    """

    PAs = []

    for row in stats:
        PAs.append([row[2]])

    return np.array(PAs)


def apply_age_factor(stats, age):
    """
    Takes in an array of statistics and applies an age factor to all stats
    based on the player's age.

    Inputs:
        stats: list of stats
        age: the player's age

    Returns: list of age adjusted stats
    """

    if not age:
        age_adj = 1
    elif age < 29:
        age_adj = 1 - (age - 29) * (0.006)
    elif age > 29:
        age_adj = 1 - (age - 29) * (0.003)
    else:
        age_adj = 1

    return stats * age_adj


def round_estimates(stats_array):
    """
    Rounds the final estimates for players' projections.

    Inputs: array of stats

    Returns: list of rounded (to whole numbers) stats
    """

    rounded_list = []

    for stat in stats_array:
        rounded = '%.0f' % stat
        rounded_list.append(rounded)

    return rounded_list


def calculate_avg(stats):
    """
    Calculates batting average from a list of statitstics that include hits
    and at-bats.

    Inputs: list of stats

    Returns: estimate for batting average
    """

    hits = int(stats[3])
    ab = int(stats[1])

    return "%.3f" % (hits / ab)


def calculate_obp(stats):
    """
    Calculates on-base percentage from a list of statistics that includes the
    necessary data.

    Inputs: list of stats

    Returns: estimate for OBP
    """

    hits = int(stats[3])
    bb = int(stats[10])
    hbp = int(stats[13])
    ab = int(stats[1])
    sf = int(stats[14])

    numer = hits + bb + hbp
    denom = ab + bb + hbp + sf

    return "%.3f" % (numer / denom)


def calculate_slg(stats):
    """
    Calculates slugging percentage from a list of statitstics that includes
    the necessary data.

    Inputs: list of stats

    Returns: estimate for SLG%
    """

    singles = int(stats[4])
    doubles = int(stats[5])
    triples = int(stats[6])
    hr = int(stats[7])
    ab = int(stats[1])

    total_bases = 1 * singles + 2 * doubles + 3 * triples + 4 * hr

    return "%.3f" % (total_bases / ab)


def calculate_woba(stats, one_ya):
    """
    Calculates wOBA from a list of statistics that includes the necessary
    data.

    Inputs:
        stats: list of stats
        one_ya: year before the one we are projecting for

    Returns: estimate for WOBA
    """

    weightings = get_weightings(one_ya) # Finds weightings from FanGraphs

    uBB = float(stats[10]) - float(stats[11]) # Subtract intentional walks
    HBP = float(stats[13])
    singles = float(stats[4])
    doubles = float(stats[5])
    triples = float(stats[6])
    HR = float(stats[7])
    AB = float(stats[1])
    SF = float(stats[14])

    wBB = float(weightings['wBB'])
    wHBP = float(weightings['wHBP'])
    w1B = float(weightings['w1B'])
    w2B = float(weightings['w2B'])
    w3B = float(weightings['w3B'])
    wHR = float(weightings['wHR'])

    numerator = ((wBB * uBB) + (wHBP * HBP) + (w1B * singles) +
                 (w2B * doubles) + (w3B * triples) + (wHR * HR))

    denominator = AB + uBB + SF + HBP

    return "%.3f" % (numerator / denominator)


def find_age(soup, year):
    """
    Finds a player's age by scraping his FanGraphs webpage.

    Inputs:
        soup: a player's FanGraphs soup code
        year: the year we are projecting for

    Returns: the player's age
    """

    step1 = soup.find('strong', text='Birthdate:')

    if not step1:
        return None

    step2 = step1.next.next

    if not step2:
        return None

    match = re.search('([0-9]{4})', step2)

    if match:
        birth_year = match.group(1)
        return year - int(birth_year)
    else:
        return None


def find_position(soup):
    """
    Scrapes the player's position from his FanGraphs webpage.

    Inputs: the player's FanGraphs soup code

    Returns: the player's position
    """

    step1 = soup.find('strong', text='Position:')

    if not step1:
        return 'N/A'

    step2 = step1.next.next

    if step2:
        return step2.strip()
    else:
        return 'N/A'