# Francesco Scivittaro
# Making our proprietary linear model

import pandas as pd
import statsmodels.formula.api as smf
import csv
import numpy as np
import matplotlib.pyplot as plt

outlier = 'Chris Parmelee'

all_poss_ivs = ['avg_distance', 'avg_exit_vel','barrels_per_bbe', 
    'fbld_avg_exit_vel', 'gb_avg_exit_vel', 'max_distance', 'max_exit_vel', 
    'min_hit_speed', 'LD_per', 'GB_per', 'FB_per', 'IFFB_per', 'PULL_per',
    'CENT_per', 'OPPO_per','SOFT_per', 'MED_per', 'HARD_per', 'bb_rate', 'k_rate',
    'shift_rate']

best_model = ['avg_distance', 'k_rate', 'bb_rate', 'avg_exit_vel', 
    'barrels_per_bbe', 'LD_per']


def write_predictions_csv():
    '''
    Writes a csv file containing the predictions and model inputs of the
    regression

    Returns:
        A command string that can be used to write the schema of the SQL
        database containing the data
    '''
    lm2016, model_df_2016, corr, r = make_model(2016, 70, best_model)
    lm2015, model_df_2015, corr2, r = make_model(2015, 70, best_model)

    preds_2017 = make_predictions(lm2016, model_df_2016)
    preds_2016 = make_predictions(lm2015, model_df_2015)

    preds_2017['year'] = 2017
    preds_2016['year'] = 2016

    predictions = preds_2017.append(preds_2016, ignore_index=True)
    predictions.index.name = 'unique_id'

    predictions = predictions.round(3)
    predictions.to_csv('predictions_data.csv')

    cols = list(predictions.columns)
    cols.remove('Team_x')
    cols.insert(2,'Team')
    cols = ['unique_id'] + cols

    command_str = ('CREATE TABLE predictions(' + ', '.join(cols) +
                    ', PRIMARY KEY (unique_id));')

    return command_str

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
    fg_data = pd.merge(fg_data, shifts, left_on=['PlayerID', 'Name'], 
                        right_on=['PlayerID_shift', 'Name_shift'])
    fg_data = pd.merge(fg_data, wOBA, on=['PlayerID', 'Name'])

    fg_data = fg_data[fg_data['PA'] >= 30]

    extras = fg_data['BB'] + fg_data['IBB'] + fg_data['HBP']
    fg_data['bb_rate'] = extras / fg_data['PA']
    fg_data['k_rate'] = fg_data['SO'] / fg_data['PA']
    fg_data['shift_rate'] = fg_data['PA_shift'] / fg_data['PA']

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
    
    fraction = sample_percent / 100
    training_df = model_df.sample(frac=fraction, replace=False)
    testing_df = model_df[~model_df.isin(training_df)].dropna()

    formula_str = 'wOBA ~ ' + ' + '.join(vars_list)
    lm = smf.ols(formula_str, data = model_df).fit()

    tested = lm.predict(testing_df)
    testing_df['predictions'] = tested

    corr = np.corrcoef(testing_df['wOBA'], list(tested))[0, 1]
    test_r_squared = smf.ols('wOBA ~ predictions', data = testing_df).fit()

    return lm, model_df, corr, test_r_squared.rsquared

def change_percent(data):
    '''
    Converts percentage values to a decimal value

    Inputs:
        data: A string representing a percentage
    Returns:
        A fractional representation of the percentage
    '''
    return float(str(data).strip('%'))/100

def make_predictions(lm, batters_df):
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
    predictions_df = batters_df[["Name", "PlayerID", "Team_x"] + best_model]
    predictions_df.loc[predictions_df.Team_x == '- - -', 'Team_x'] = 'FA'

    expected_wOBA = lm.predict(predictions_df)

    predictions_df['x_wOBA'] = expected_wOBA

    return predictions_df

def calc_future_accuracy(df_2015, remove_outlier = False):
    '''
    Calculates measures of the accuracy of statcast regression projections 
    for 2016 against the actual observed wOBAs in 2016.

    Inputs:
        df_2015: The dataframe containing the predicted wOBA
        remove_outlier: A boolean variable that is True if outliers should be
        removed and defaults to False
    Returns:
        corr: The correlation coefficient between the predicted wOBAs and the
        observed ones
        lm: A univariate linear model between the predictions and observations
    '''
    location = '~/cs122-win-17-fscivittaro42/fsfsnm/'
    wOBA = location + 'nsm/2016_data/woBA.csv'

    actual_woba = pd.read_csv(wOBA)

    accuracy_df = pd.merge(df_2015, actual_woba, on=['PlayerID', 'Name'])

    if remove_outlier:
        accuracy_df = accuracy_df[accuracy_df['Name'] != outlier]

    corr = np.corrcoef(accuracy_df['wOBA'], accuracy_df['x_wOBA'])[0, 1]
    lm = smf.ols('wOBA ~ x_wOBA', data = accuracy_df).fit()

    return corr, lm

def calc_marcel_accuracy(remove_outlier = False):
    '''
    Calculates measures of the accuracy of marcel projections 
    for 2016 against the actual observed wOBAs in 2016.

    Inputs:
        remove_outlier: A boolean variable that is True if outliers should be
        removed and defaults to False
    Returns:
        corr: The correlation coefficient between the predicted wOBAs and the
        observed ones
        lm: A univariate linear model between the predictions and observations
    '''
    location = '~/cs122-win-17-fscivittaro42/fsfsnm/'
    wOBA = location + 'nsm/2016_data/woBA.csv'

    actual_woba = pd.read_csv(wOBA)
    marcel_woba = pd.read_csv('marcel_woba.csv')

    marcel_woba = marcel_woba[marcel_woba['year'] == 2016]

    accuracy_df = pd.merge(actual_woba, marcel_woba, 
        left_on=['PlayerID', 'Name'], right_on=['player_id', 'name'])

    if remove_outlier:
        accuracy_df = accuracy_df[accuracy_df['Name'] != outlier]

    corr = np.corrcoef(accuracy_df['wOBA'], accuracy_df['woba'])[0, 1]
    lm = smf.ols('wOBA ~ woba', data = accuracy_df).fit()

    return corr, lm

def plot_predictions(accuracy_df, col1, col2, filename):
    '''
    '''
    x = accuracy_df[col1]
    y = accuracy_df[col2]

    fig, ax = plt.subplots()
    fit = np.polyfit(x, y, deg=1)
    ax.plot(x, fit[0] * x + fit[1], color='red')
    ax.scatter(x, y)

    plt.xlabel('Actual 2016 wOBA')
    plt.ylabel('Predicted 2016 wOBA')
    plt.title('Predicted vs Actual wOBAs - 2016')

    fig.show()
    fig.savefig(filename)



'''
To put the CSV file into a SQL database, I did the following:

sqlite3 predictions.db

(copy/pasted the command string output from write_predictions_csv)

.mode csv

.import predictions_data.csv predictions

Only batters with a minimum of 30 at bats were included in the data
'''
