"""
Data now available from both Lincs and Kent with raw scores and DOB rounded to nearest week.
Lincs data was used to investigate GLA's claimed "Proprietary Standardisation" [sic with straight face]
That involved 'deaggregating' DOBs so the graphs weren't a step function (although TBH that was more aesthetic.)

This is a tidy up/consolidation of other scripts which will create a standard function to normalise scores to
σ=15, μ=100 the results can be compared against Essex and compared against each other.

"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Qt5Agg')
plt.rcParams['font.family'] = 'Times New Roman'  # Works for labels but not in raw strings.

# Load raw scores from source data exactly as disclosed by FOI
kent = pd.read_csv('data/Kent_FOI_59020546.csv',
                   usecols=['Week of birth', 'Raw Maths', 'Raw English', 'Raw Reasoning'])
kent.columns = ['WoB', 'Maths', 'English', 'Reasoning']

# There were 12 seriously wrong age children in this data. These *should* have been excluded from the data, as
# requested to ensure anonymity! These were manually prior removed from the csv file so it can be shared.

lincs = pd.read_csv('data/Lincs_n=4267-anon.csv',
                    usecols=['WOB', 'VRTotalRawScore', 'NVTotalRawScore'])
lincs.columns = ['WoB', 'Verbal_Reasoning', 'Non_Verbal_Reasoning']

# Create days_older value based on week of birth
pd.options.mode.chained_assignment = None
kent['WoB'] = pd.to_datetime(kent['WoB'], format='%d/%m/%Y')
kent['days_older'] = (kent.WoB.min() - kent['WoB']).dt.days + 1000
kent.days_older = kent.days_older - kent.days_older.min()
# Ages now range (0, 371) days. There are nine in the last week of August. These seem ok to leave.

lincs['WoB'] = pd.to_datetime(lincs['WoB'], format='%d/%m/%Y')
lincs['days_older'] = (lincs.WoB.min() - lincs['WoB']).dt.days + 1000
lincs.days_older = lincs.days_older - lincs.days_older.min()
# Ages now range (0, 378) days. Still a few not in normal age cohort but < 2 weeks so seems ok.

# Create an empty dataframe to put results in.
results = pd.DataFrame(columns=['Auth', 'Test', 'Coef', 'P>|t|', 'count', 'mean', 'std', 'skew', 'kurt'])

"""
 _____  ______ _____ _____  ______  _____ _____ _____ ____  _   _ 
|  __ \|  ____/ ____|  __ \|  ____|/ ____/ ____|_   _/ __ \| \ | |
| |__) | |__ | |  __| |__) | |__  | (___| (___   | || |  | |  \| |
|  _  /|  __|| | |_ |  _  /|  __|  \___ \\___ \  | || |  | | . ` |
| | \ \| |___| |__| | | \ \| |____ ____) |___) |_| || |__| | |\  |
|_|  \_\______\_____|_|  \_\______|_____/_____/|_____\____/|_| \_|
                                                                  
"""

def regr(auth, data):
    """
    Takes dataframe of raw scores and adds a row of results from linear regression to the results dataframe.
    :param auth: The (quasi/)admissions authority
    :param data: Dataframe with two columns: [raw_scores, days_older]
    :return:
    """

    # Get the name of this test.
    test = data.columns[0]
    # kent has an empty row. lincs has missing values for some tests. Drop all missing values.
    data = data.dropna(subset=[test])

    # Normalise so σ=15, μ=100
    data[test] = (data[test] - data[test].mean()) / data[test].std() * 15 + 100
    print('Check normalisation: mean =', data[test].mean(), ', std dev =', data[test].std())

    form = test + ' ~ days_older'
    lm = smf.ols(formula=form, data=data).fit()

    # build a row of data for this regression
    row = [auth, test]

    # daily coefficient in "marks"
    row.append(lm.params.iloc[1])
    # add P>|t|
    row.append(lm.pvalues.iloc[1])
    # add other useful stuff
    row.append(data[test].count())
    row.append(data[test].mean())
    row.append(data[test].std())
    row.append(data[test].skew())
    row.append(data[test].kurt())

    results.loc[len(results)] = row

# Kent
for t in ['Maths', 'English', 'Reasoning']:
    regr('Kent', kent[[t, 'days_older']].copy())


# Lincs
for t in ['Verbal_Reasoning', 'Non_Verbal_Reasoning']:
    regr('Lincs', lincs[[t, 'days_older']].copy())

results.to_csv('data/lincs-kent-regression.py_line100.csv')

