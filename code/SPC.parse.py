"""
  _____ _____   _____
 / ____|  __ \ / ____|
| (___ | |__) | |
 \___ \|  ___/| |
 ____) | |    | |____
|_____/|_|     \_____|

From 2010 to 2022 DfE routinely disclosed *SCHOOL LEVEL* dataset called "Schools Pupils & Characteristics"
based on January census. From 2023 onwards this was changed to include all years dating back to 2016 but
aggregated to local authority level. The latest SPC can be found here:
https://explore-education-statistics.service.gov.uk/find-statistics/school-pupils-and-their-characteristics

The school level data is still available here:
https://github.com/jamescoombs3/SchoolsPupilsCharacteristics
The data is in CSV. The leftmost columns describe each school (like URN, phase of education ...) There were a dozen
of these in 2010. By 2022 this had grown to 30 columns. Column names and values are not consistent! (The rightmost
~200 fields have other values such as the number of boys aged 13 or proportion/count of FSM. Not needed here.)

SPC.parse.py
============
This script does the following
1) Defines a filter to select just regular state funded secondary schools.
2) Categorises each school as own admission authority [True|False]. (Community and Voluntary controlled schools'
arrangements are *normally* set by the LA (Wolfe 2013) although this isn't 100%).
3) Categorise as fully selective [True|False]. NB: There were 164 until two merged to make 163.

"""

# Pycharm thinks this import isn't needed. It is!
from tkinter.constants import FALSE
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')

# Create empty dataframe.
out = pd.DataFrame(columns=['year', 'selective', 'pct_own_aa'])

# iterate over the available years.
years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

for y in years:
    url = 'https://github.com/jamescoombs3/SchoolsPupilsCharacteristics/blob/main/SPC_' + y + '.csv?raw=true'
    # loading 30 leftmost columns is sufficient.
    df = pd.read_csv(url, usecols=range(0, 30), encoding ='ISO-8859-1', low_memory=False)

    # Change column names so they are consistent! This will only change the name if the dictionary key matches so,
    # by changing it to something different and unique, any oversights are picked up.
    df = df.rename(columns={'Type of establishment':'estab_type', 'type_of_establishment':'estab_type',
                            'TypeOfEstablishment':'estab_type', 'TypeOfEstablishment (name)':'estab_type'})
    df = df.rename(columns={'Admissions policy':'admin_policy', 'Admissions Policy':'admin_policy',
                            'admissions_policy':'admin_policy'})
    df = df.rename(columns={'Phase of education':'phase', 'Phase-type grouping':'phase',
                            'phase-type_grouping':'phase'})


    # 1) Filter just state funded mainstream secondary schools.
    if y == '2010' or y == '2011' or y == '2012' or y == '2013':
        # This filter does not include pupil referral/special schools
        df = df.loc[(df.phase == 'Secondary')]

    else:
        # This filter (also) does not include pupil referral/special schools
        df = df.loc[(df.phase == 'State-funded secondary')]

    # TEST with each year.  df.estab_type.unique()
    # This should not return any special schools because they were filtered out above.
    df['aa_flag'] = df['estab_type'].apply(lambda x: False if
    x == 'Community' or x == 'Community School' or x == 'Community school' or x == 'Voluntary controlled' or
    x == 'Voluntary Controlled School' or x == 'Voluntary controlled school'
    else True)

    df['selective'] = df['admin_policy'].apply(lambda x: True if
    x == 'Selective' or x == 'Selective (grammar)' else False)

    path = 'data/test' + y + '.csv'
    # df.to_csv(path, index=False)
    # Further sanity check.
    gs = df[df['selective']].__len__()
    tot = df.__len__()
    print('In' , y , 'there were', gs, 'grammars out of a total', tot, 'schools')

    # Work out percentage of selective schools which are own admissions authority
    tdf = df[df['selective']]
    # tdf['aa_flag'].value_counts(normalize=True).mul(100).astype(str) + '%'
    pct = tdf['aa_flag'].value_counts(normalize=True).loc[True]
    # Create a row to append to a summary table {year, selective, %own adm auth}
    out.loc[len(out)] = [y, True, pct]

    # Work out percentage of comprehensive schools which are own admissions authority. (Note the tilda '~')
    tdf = df[~df['selective']]
    # tdf['aa_flag'].value_counts(normalize=True).mul(100).astype(str) + '%'
    pct = tdf['aa_flag'].value_counts(normalize=True).loc[True]
    # Create a row to append to a summary table {year, selective, %own adm auth}
    out.loc[len(out)] = [y, False, pct]


out.to_csv('data/spc_longitudinal.csv', index=False)
# Dataframe is 'long' which is better for plotting. Converting to 'wide' is better for a table in a document.
out.pivot(columns=['selective'], index=['year'], values=['pct_own_aa']).to_csv('data/spc_pivot.csv')

# PLOT

out['Percent own admissions authority'] = out.pct_own_aa * 100
hue_order = [True, False]
fig, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=out, x='year', y='Percent own admissions authority' , hue='selective', hue_order=hue_order)

# ax1.set_ylabel('Percent own admissions authority')
ax1.set_xlabel('Year')
plt.subplots_adjust(top=0.984, bottom=0.063, left=0.034, right=0.992, hspace=0.2, wspace=0.2)

fig.savefig('data/SPC.parse.py_line_116.png', dpi=300)

