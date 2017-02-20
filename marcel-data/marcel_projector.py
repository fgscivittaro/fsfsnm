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

    if one_ya_stats:
        first_stats = weight_stats_by_pa(one_ya_stats[0][7:])
        current_age = one_ya_stats[0][5] + 1
    else:
        first_stats = [0] * 21
        current_age = None

    if two_ya_stats:
        second_stats = weight_stats_by_pa(two_ya_stats[0][7:])
    else:
        second_stats = [0] * 21

    if three_ya_stats:
        third_stats = weight_stats_by_pa(three_ya_stats[0][7:])
    else:
        third_stats = [0] * 21

    all_stats = np.array([first_stats, second_stats, third_stats])

    final_weighted_stats = all_stats * WEIGHTS
    combined_weighted_stats = np.sum(final_weighted_stats, axis=0)

    c.close()
    conn.close()

    return combined_weighted_stats


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