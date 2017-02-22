import sqlite3
import numpy as np

def compute_marcel_projection(name, position, year, db):
    """
    Takes a player's name and computes their Marcel projection for all
    statistics. Also takes in whether the player is "a "hitter" or "pitcher"
    and the year we would like to forecast for.

    Inputs:
        name: (str) the player's name, Firstname Lastname
        position: (str) either 'hitter' or 'pitcher'
        year: (int) the future year to project
        db: the SQL database
    """

    conn = sqlite3.connect(db)
    c = conn.cursor()

    firstname, lastname = name.split()
    position = position.replace("er", "ing")
    year = int(year)

    one_ya = year - 1
    two_ya = year - 2
    three_ya = year - 3
    WEIGHTS = np.array([[5/12], [4/12], [3/12]])

    one_ya_stats = retrieve_stats(firstname,
                                  lastname,
                                  position,
                                  one_ya,
                                  c)
    two_ya_stats = retrieve_stats(firstname,
                                  lastname,
                                  position,
                                  two_ya,
                                  c)
    three_ya_stats = retrieve_stats(firstname,
                                    lastname,
                                    position,
                                    three_ya,
                                    c)

    league_rates = calculate_league_rates(position, year, c)

    c.close()
    conn.close()

    if not one_ya_stats and not two_ya_stats and not three_ya_stats:
        return league_rates * 250 # We assume 200 PAs

    if one_ya_stats:
        first_stats = weight_stats_by_pa(one_ya_stats[0][7:])
        current_age = one_ya_stats[5] + 1
        one_ya_pa = one_ya_stats[11]
    else:
        first_stats = [0] * 21
        current_age = None
        one_ya_pa = 0

    if two_ya_stats:
        second_stats = weight_stats_by_pa(two_ya_stats[0][7:])
        two_ya_pa = two_ya_stats[11]
    else:
        second_stats = [0] * 21
        two_ya_pa = 0

    if three_ya_stats:
        third_stats = weight_stats_by_pa(three_ya_stats[0][7:])
        three_ya_pa = three_ya_stats[11]
    else:
        third_stats = [0] * 21
        three_ya_pa = 0

    all_stats = np.array([first_stats, second_stats, third_stats])

    final_weighted_stats = all_stats * WEIGHTS
    combined_weighted_stats = np.sum(final_weighted_stats, axis=0)

    age_regressed_rates = apply_age_factor(combined_weighted_stats,
                                           current_age)

    rel = calculate_rel(one_ya_pa, two_ya_pa, three_ya_pa)

    regressed_rates = ((rel * age_regressed_rates) + 
                      ((1 - rel) * league_rates))

    projected_PAs = one_ya_pa * age_regressed_rates[4]

    return age_regressed_rates * projected_PAs


def retrieve_stats(firstname, lastname, position, year, cursor):
    """
    Takes a player's name, position, year, and a cursor onject and retrieves
    all of their stats from that year.
    """

    query = """
            SELECT * FROM marcel_{}
            WHERE FirstName = '{}'
            AND LastName = '{}'
            AND Year = {}
            """.format(position, firstname, lastname, year)

    return cursor.execute(query).fetchall()


def weight_stats_by_pa(stats):
    """
    Takes in a year's stats and weights them by plate appearances.
    """

    PA = stats[4]

    weighted_stats = []

    for stat in stats:
        weighted_stats.append(stat / PA)

    return weighted_stats


def calculate_rel(PA1, PA2, PA3):
    """
    Takes in the amount of plate appearances for a player over the past three
    seasons and calculates a reliability factor, which we will use to regress
    the players' statisitcs.
    """

    total_weighted_PAs = PA1 * 5 + PA2 * 4 + PA3 * 3

    return total_weighted_PAs / (total_weighted_PAs + 1200)


def calculate_league_rates(position, year, cursor):
    """
    Calculates weighted league averages using data from all players.
    """

    one_ya = year - 1
    two_ya = year - 2
    three_ya = year - 3

    query1 = """
             SELECT * FROM marcel_{}
             WHERE Year = {}
             """.format(position, one_ya)

    query2 = """
             SELECT * FROM marcel_{}
             WHERE Year = {}
             """.format(position, two_ya)

    query3 = """
             SELECT * FROM marcel_{}
             WHERE Year = {}
             """.format(position, three_ya)

    one_ya_stats = cursor.execute(query1).fetchall()
    two_ya_stats = cursor.execute(query2).fetchall()
    three_ya_stats = cursor.execute(query3).fetchall()

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

    return np.add(one_ya_averages, two_ya_averages, three_ya_averages)


def convert_to_array(stats):
    """
    Takes the list of tuples generated by SQL and converts it into an array.
    """

    full_stats = []

    for statline in stats:
        one_player = []
        for stat in statline[7:]:
            one_player.append(stat)
        full_stats.append(one_player)

    return np.array(full_stats)


def create_PA_array(stats):
    """
    Takes in an array of stats and generates an array containing a single
    column of the players' PAs.
    """

    PAs = []

    for row in stats:
        PAs.append([row[4]])

    return np.array(PAs)


def apply_age_factor(stats, age):
    """
    Takes in an array of statistics and applies an age factor to all stats
    based on the player's age.
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