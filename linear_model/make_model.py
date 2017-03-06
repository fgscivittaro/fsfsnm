# Francesco Scivittaro
# Making our proprietary linear model

import pandas as pd
import statsmodels.formula.api as smf
import csv

all_poss_ivs = ['avg_distance', 'avg_exit_vel','barrels_per_bbe', 
    'fbld_avg_exit_vel', 'gb_avg_exit_vel', 'max_distance', 'max_exit_vel', 
    'min_hit_speed', 'LD_per', 'GB_per', 'FB_per', 'IFFB_per', 'PULL_per',
    'CENT_per', 'OPPO_per','SOFT_per', 'MED_per', 'HARD_per', 'bb_rate', 'k_rate',
    'shift_rate']
exit_vel_ivs = ['avg_distance', 'avg_exit_vel','barrels_per_bbe',
    'fbld_avg_exit_vel', 'gb_avg_exit_vel', 'max_distance','max_exit_vel',
    'min_hit_speed', 'LD_per', 'GB_per', 'FB_per', 'IFFB_per', 'PULL_per',
    'CENT_per', 'OPPO_per', 'bb_rate', 'k_rate','shift_rate']

binning_ivs = ['LD_per', 'GB_per', 'FB_per', 'IFFB_per', 'PULL_per','CENT_per', 'OPPO_per', 
    'SOFT_per', 'MED_per', 'HARD_per', 'bb_rate', 'k_rate','shift_rate']

skinny_ivs = ['barrels_per_bbe', 'bb_rate','k_rate', 'shift_rate']

best_model = ['avg_distance', 'k_rate', 'bb_rate', 'avg_exit_vel', 
    'barrels_per_bbe', 'LD_per']

def make_model(year, sample_percent, vars_list):
    '''
    Returns a linear model that predicts wOBA (weighted on-base average) of
    baseball players

    Inputs:
        minimum_bbe: An integer representing minimum number of batted ball events 
        needed to qualify a player for use in building the model
        sample_size: An integer representing the percentage of the
        observations that will be used to build and train the model. The 
        remainder of observations will be retained for testing purposes.
        vars: A list of independent variables for the regression
    Returns: 
        An object representing the linear model created
    '''
    minimum_bbe = 30
    location = '~/cs122-win-17-fscivittaro42/fsfsnm/'

    fg_batter_stats =  location + 'nsm/' + str(year) + '_data/batter_data.csv'
    fg_batted_balls = (location + 'nsm/' + str(year) + 
                        '_data/batted_ball_data.csv')
    shifts = location + 'nsm/' + str(year) + '_data/shift_data.csv'
    wOBA = location + 'nsm/' + str(year) + '_data/woBA.csv'
    statcast = location + 'statcast_data/statcast_' + str(year) + '.csv'

    batter_stats = pd.read_csv(fg_batter_stats)
    batted_balls = pd.read_csv(fg_batted_balls)
    shifts = pd.read_csv(shifts)
    statcast = pd.read_csv(statcast)
    wOBA = pd.read_csv(wOBA)

    if year == 2015:
        addendum_loc = location + 'linear_model/insert_shift.csv'
        shifts_addendum = pd.read_csv(addendum_loc)
        shifts = shifts.append(shifts_addendum)

    statcast_minimum = statcast[statcast['attempts'] >= minimum_bbe]
    statcast_dict = {
    'barrels_per_bbe': list(statcast_minimum['brl_percent']),
    'avg_exit_vel': list(statcast_minimum['avg_hit_speed']),
    'min_hit_speed':list(statcast_minimum['min_hit_speed']),
    'player_name':list(statcast_minimum['name']),
    'max_distance':list(statcast_minimum['max_distance']),
    'gb_avg_exit_vel':list(statcast_minimum['gb']),
    'avg_distance':list(statcast_minimum['avg_distance']),
    'fbld_avg_exit_vel':list(statcast_minimum['fbld']),
    'max_exit_vel':list(statcast_minimum['max_hit_speed']),
    }

    model_df = pd.DataFrame(statcast_dict)

    fg_data = pd.merge(batter_stats, batted_balls, on=['PlayerID', 'Name'])
    fg_data = pd.merge(fg_data, shifts, on=['PlayerID', 'Name'])
    fg_data = pd.merge(fg_data, wOBA, on=['PlayerID', 'Name'])

    fg_data = fg_data[fg_data['PA'] >= 30]

    extras = fg_data['BB'] + fg_data['IBB'] + fg_data['HBP']
    fg_data['bb_rate'] = extras / fg_data['PA']
    fg_data['k_rate'] = fg_data['SO'] / fg_data['PA']
    fg_data['shift_rate'] = fg_data['shift_PA'] / fg_data['PA']

    with open('find_replace_' + str(year) + '.csv', 'r') as f:
        reader = csv.reader(f)
        for rows in reader:
            find = rows[0]
            replace = rows[1]
            fg_data.replace(to_replace=find, value=replace, inplace=True)

    fg_match = fg_data[fg_data['Name'].isin(model_df['player_name'])]

    model_df = pd.merge(model_df, fg_match, left_on='player_name', 
                        right_on='Name')

    model_df['barrels_per_bbe'] = model_df['barrels_per_bbe'].map(
                                                    change_percent)
    model_df['SOFT_per'] = model_df['SOFT_per'].map(change_percent)
    model_df['MED_per'] = model_df['MED_per'].map(change_percent)
    model_df['HARD_per'] = model_df['HARD_per'].map(change_percent)
    model_df['OPPO_per'] = model_df['OPPO_per'].map(change_percent)
    model_df['CENT_per'] = model_df['CENT_per'].map(change_percent)
    model_df['PULL_per'] = model_df['PULL_per'].map(change_percent)

    formula_str = 'WoBA ~ ' + ' + '.join(vars_list)
    lm = smf.ols(formula_str, data = model_df).fit()
    
    return lm

def change_percent(data):
    '''
    Converts percentage values to a decimal value

    Inputs:
        data: A string representing a percentage
    Returns:
        A fractional representation of the percentage
    '''
    return float(str(data).strip('%'))/100

def make_predictions(model, batters_df, col_name=False):
    '''
    Writes a CSV file containing each batter and their projected wOBA based
    off of our model

    Inputs:
        model: The object representing our linear model
        batters_df: A dataframe containing the inputs to be used for 
        predictions
    Returns:
        A SQL command line representing the schema to create the predictions
        table
    '''
    predictions = []

    batters_list = list(batters_df['name'])
    pred_data = list(pd.DataFrame({'input': [batters_df['input']]}))

    f = csv.writer(open("predictions.csv", "wt"))
    
    if col_name:
        f.writerow(["player_name", "expected_wOBA"])

    for i in range(len(batters_df)):
        f.writerow([batters_list[i], ppred_data[i]])

    command_str = "CREATE TABLE predictions(player_name TEXT, prediction REAL, PRIMARY KEY (player_name));"

    return command_str


