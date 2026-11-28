"""
Final tidy up. Data is on github so can load from there. The objectives have changed over time but in this final
version we're looking for the regression coefficient for candidates' relative ages. This was initially expressed
in "marks" where σ=15 but that isn't needed for effect sizes. 11-plus results are invariably "standardised" in a
non-standard way so the benefits are marginal.

Dates are always hard work to process! Weekly DOBs are converted to "days_older" relative to the youngest.
These all end up as multiples of 7 but this marginal loss of fidelity makes no difference to linear regression.

"""

# import numpy as np
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from time import sleep
# import matplotlib
# matplotlib.use('Qt5Agg')

outdir = 'Bias_effect_size/output/'
csv = 'https://github.com/education-research/11-plus/blob/main/data/Kent_FOI_59020546.csv?raw=true'
# Load raw scores from data disclosed by FOI
kent = pd.read_csv(csv, usecols=['Week of birth', 'Raw Maths', 'Raw English', 'Raw Reasoning'])
kent.columns = ['WoB', 'Maths', 'English', 'Reasoning']
sleep(2)  # Github can get stroppy if data is requested too quickly.

# There were 12 identifiable data subjects in the data disclosed by Lincs, despite very clear instructions to
# remove these! This "anon" version is as disclosed but with these records removed.
csv = 'https://github.com/education-research/11-plus/blob/main/data/Lincs_n=4267-anon.csv?raw=true'
lincs = pd.read_csv(csv, usecols=['WOB', 'VRTotalRawScore', 'NVTotalRawScore'])
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
results = pd.DataFrame(columns=['Auth', 'Test', 'Coef', 'P>|t|', 'R-square', 'count', 'mean', 'std', 'skew', 'kurt'])

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
    # data[test] = (data[test] - data[test].mean()) / data[test].std() * 15 + 100
    # Normalise so σ=1, μ=0
    data[test] = (data[test] - data[test].mean()) / data[test].std()

    print('Check normalisation: mean =', data[test].mean(), ', std dev =', data[test].std())

    form = test + ' ~ days_older'
    lm = smf.ols(formula=form, data=data).fit()

    # build a row of data for this regression
    row = [auth, test]

    # daily coefficient in "marks"
    row.append(lm.params.iloc[1])
    # add P>|t|
    row.append(lm.pvalues.iloc[1])
    # add R^2
    row.append(lm.rsquared)
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

results.to_csv(outdir + 'lincs-kent-regression-v2.py.csv', index=False)

