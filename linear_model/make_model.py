# Francesco Scivittaro
# Making our proprietary linear model

import pandas as pd
import statsmodels.formula.api as smf

def make_model(minimum_bbe, sample_percent):
    '''
    Returns a linear model that predicts wOBA (weighted on-base average) of
    baseball players

    Inputs:
        minimum_bbe: An integer representing minimum number of batted ball events 
        needed to qualify a player for use in building the model
        sample_size: An integer representing the percentage of the
        observations that will be used to build and train the model. The 
        remainder of observations will be retained for testing purposes.

    Returns: 
        An object representing the linear model created
    '''
    location = '~/cs122-win-17-fscivittaro42/fsfsnm/'

    fg_batter_stats =  location + 'nsm/2016_data/batter_data.csv'
    fg_batted_balls = location + 'nsm/2016_data/batted_ball_data.csv'
    shifts = location + 'nsm/2016_data/shifts_data.csv'
    statcast = location + 'statcast_data/statcast_2016.csv'

    batter_stats = pd.read_csv(fg_batter_stats)
    batted_balls = pd.read_csv(fg_batted_balls)
    shifts = pd.read_csv(shifts)
    statcast = pd.read_csv(statcast)

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
    'avg_hr_distance':list(statcast_minimum['avg_hr_distance'])
    }

    model_df = pd.DataFrame(statcast_dict)

    batter_stats['shifts_per_pa'] = 

    match_shifts = shifts[shifts['Name'].isin(statcast_minimum['name'])]
    model_df['shifts_per_pa'] = match_shifts

    fangraphs_data = pd.merge(batter_stats, batted_balls, on='player_id')
    fangraphs_data = pd.merge(fangraphs_data, shifts, on='player_id')

    predictions_data = pd.merge(fangraphs_data, statcast_minimum,
        left_on='player_name', right_on='name', right_index=True)

    sample_size = (sample_percent / 100) * len(statcast_minimum)
    training_statcast = statcast_minimum.sample(sample_size, replace = False)

    fangraphs_data = fangraphs_data[fangraphs_data['player_name'].isin(
                                            training_statcast['name'])]

    model_data = pd.merge(fangraphs_data, training_statcast, 
        left_on='player_name', right_on='name', right_index=True)

    lm = smf.ols(formula='wOBA ~ ...', data=model_data).fit()

    make_predictions(lm, predictions_data)

    return fangraphs_data

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


