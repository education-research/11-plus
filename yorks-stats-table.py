"""
Data provided by North Yorks County Council:
https://www.whatdotheyknow.com/request/linked_data_on_11_tests#incoming-986716
Needs downloading. This script expects to find in subdirectory called 'data'.

The script compares linked results from candidates sitting the "same" test (different questions) two consecutive weeks.
The data includes both raw and age standardised test results. As expected, the reliability coefficient (correlation
between the scores on each occasion) is higher with raw results.

Version 1 used raw scores but after giving this more thought, the process of standardisation adds error to the
measurement so ...
Version 2 is rewritten to work with standardised scores.

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Qt5Agg')

rip = pd.read_excel(open('data/Response to FOI N2526 NorthYorkshire Results Raw and Standardised.xlsx', 'rb'),
                    sheet_name='Ripon Grammar School ')

erm = pd.read_excel(open('data/Response to FOI N2526 NorthYorkshire Results Raw and Standardised.xlsx', 'rb'),
                    sheet_name='Ermysteds Grammar School ')

# col names are identical so ...
scores = pd.concat([rip, erm], ignore_index=True)
del rip
del erm

# Remove the dates, raw scores and total. (Column headers are not clear!)
cols = ['1st test NVR', '1st NVR RawScore', '2nd Test NVR', '2nd NVR RawScore', '1st test VR ',
       '1st VR RawScore', '2nd test VR ', '2nd VR RawScore', 'Score']

scores.drop(cols, axis=1, inplace=True)

# Give remaining columns some sensible names
cols = ['Area', 'NonVerbal_test1', 'NonVerbal_test2', 'Verbal_test1', 'Verbal_test2']
scores.columns = cols
scores['Total_test1'] = scores.NonVerbal_test1 + scores.Verbal_test1
scores['Total_test2'] = scores.NonVerbal_test2 + scores.Verbal_test1

# Pearsons assumes normal distribution and homogenous variance so create a dataframe and capture all required data
# This needs to end up in a table so may as well build it here ...
dfa = pd.DataFrame(columns=['NonVerbal', 'Verbal', 'Total'])

for col in dfa.columns:
    for method in ['pearson', 'kendall', 'spearman']:
        # work out each correlation
        cor = scores[col + '_test1'].corr(scores[col + '_test2'], method=method)
        cor = round(cor, 4)
        # write cor to dataframe.
        print(f'update [{method}, {col}] with {cor}')
        dfa.at[method, col] = cor


for col in dfa.columns:
    # loop over statistical measures
    for stat in ['mean', 'skew', 'kurt', 'std']:
        for test in ['_test1', '_test2']:
            row = stat + test
            # print(f'row = {row}, col = {col}, stat = {stat} test = {test}')
            # This was horrendously complex to derive but is an efficient vectorised solution
            val = getattr(scores[col + test], stat)()
            val = round(val, 4)
            dfa.at[row, col] = val


dfa.to_csv('data/yorks-stats-table.py-line72.csv')
