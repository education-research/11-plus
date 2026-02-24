"""
This started off as code behind a blog prompted by the fact that parents in Kent were unaware that other parts of
the country don't have the 11+ !
https://trak.org.uk/which-local-authority-has-most-children-in-grammar-schools-kent-or-buckinghamshire/

Version 2 of this script plotted selectiveness by local authority on a map using choropleth in the current year.
For this version I just want a longitudinal view and think the SPC covers 2014 - 2022 (but no longer at school
level.) Adapting this seems the quickest way to just give me %selection and %disadvantaged in grammars over that
period.


"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib
matplotlib.use('Qt5Agg')

cols = ['time_period', 'la_name', 'sex_of_school_description', 'phase_type_grouping',
        'type_of_establishment', 'denomination', 'admissions_policy', 'urban_rural', 'academy_flag',
        'number_of_key_stage_3_pupils_years_7_to_9', 'number_of_key_stage_4_pupils_years_10_and_11',
        'number_of_pupils_known_to_be_eligible_for_free_school_meals_performance_tables',
        'number_of_pupils_whose_first_language_is_known_or_believed_to_be_other_than_english']

# Don't have a requirement for EAL but it looked worth grabbing at the same time in case needed in future.

# load ~163k rows covering all years from 2015/16 and all school types.
df = pd.read_csv('C:/_python/test_reliability/data/spc_school_characteristics_.csv', usecols=cols)
#

# Filter records to select education phase "state funded secondary" (~3k remain).
df = df.loc[(df.phase_type_grouping == 'State-funded secondary')]

# The following filters remove double counted aggregate values.
df = df.loc[(
        (df.sex_of_school_description == 'Total') &
        (df.type_of_establishment == 'Total') &
        (df.denomination == 'Total') &
        (df.urban_rural == 'Total') &
        (df.academy_flag == 'Total')
)]

# Secondary schools often have sixth forms. To count *secondary* pupil numbers, add the KS3 & KS4 numbers
df['roll'] = df.number_of_key_stage_3_pupils_years_7_to_9 + df.number_of_key_stage_4_pupils_years_10_and_11

# Drop some unwanted cols from main df used for filtering which are now all just 'Total'
cols = ['sex_of_school_description', 'phase_type_grouping', 'type_of_establishment', 'denomination',
        'number_of_key_stage_3_pupils_years_7_to_9',
        'number_of_key_stage_4_pupils_years_10_and_11',
        'urban_rural', 'academy_flag']
df = df.drop(columns=cols)

# rename some columns sensibly!
cols = ['time_period', 'la_name', 'adm_policy', 'FSM_num', 'EAL', 'roll']
df.columns = cols

# In 201718 and 201819 DfE decided to rename 'Selective' schools 'Selective (grammar)' !
df = df.replace({'Selective (grammar)': 'Selective'})
# We now select just Total OR Selective ...
df = df.loc[(
        (df.adm_policy == 'Total') |
        (df.adm_policy == 'Selective')
)]


# Having obtained the required data now need to provide whole England summaries giving for each year
# i) % children in selective
# ii) %FSM in selectives
# iii %FSM in non-selectives
# Then plot, possibly all three on same since approx i=5%, ii=5%, iii=20% so would be ok on same y-axis

# check a single familiar county
check = df.loc[(df.la_name == 'Buckinghamshire')]
p = check.pivot_table(index='la_name', columns='adm_policy', values='roll', aggfunc='sum').T
print(p)
# Warning! Following code not robust as it depends on the data!
tot = p.iloc[1]['Buckinghamshire']
sel = p.iloc[0]['Buckinghamshire']
print('CHECK:', sel, 'out of', tot, 'children in Bucks are in grammars. This is', sel/tot, 'of the total')

# PREP DATA for PLOTTING
# Seaborn normally prefers 'tall/long' data but this plot works by plotting both the total and then
# selective pupils on the same figure so the data needs to be transformed to a 'wide' format.
dfp = df.pivot_table(index='la_name', columns='adm_policy', values='roll', aggfunc='sum')
dfp.Selective = pd.to_numeric(dfp.Selective, errors='coerce').fillna(0).astype(np.int64)
dfp.Total = pd.to_numeric(dfp.Total, errors='coerce').fillna(0).astype(np.int64)
dfp['pct'] = dfp.Selective / dfp.Total
dfp = dfp.sort_values(['Selective', 'Total'], ascending=[False, False])

dfp.to_csv('data/selectiveness-barplot.py.line93.csv')

"""

# PREP DATA for PLOTTING
# Seaborn normally prefers 'tall/long' data but this plot works by plotting both the total and then
# selective pupils on the same figure so the data needs to be transformed to a 'wide' format.
dfp = df.pivot_table(index='la_name', columns='adm_policy', values='roll')

dfp = dfp.drop(columns=['Non-selective', 'Not applicable', 'Unknown'])
dfp = dfp.reset_index()
dfp.Selective = pd.to_numeric(dfp.Selective, errors='coerce').fillna(0).astype(np.int64)
dfp.Total = pd.to_numeric(dfp.Total, errors='coerce').fillna(0).astype(np.int64)
dfp = dfp.sort_values(['Selective', 'Total'], ascending=[False, False])
dfp['pct'] = dfp.Selective / dfp.Total

dfp.to_csv('C:/_python/11+reliability/data/selectiveness_by_LA.csv', index=False)

"""

# Example from https://pythonbasics.org/seaborn-barplot/
f, ax = plt.subplots(figsize=(6, 45))
sns.set_color_codes('pastel')
sns.barplot(x='Total', y='la_name', data=dfp,
            label='Total pupils', color='b', edgecolor='w')
sns.set_color_codes('muted')
sns.barplot(x='Selective', y='la_name', data=dfp,
            label='Pupils in grammars', color='b', edgecolor='w')

plt.xlabel('Pupil Numbers (2023/24)')
plt.ylabel('Local Authority')

ax.legend(ncol=1, loc='lower right', fontsize=10)

# This adjusts the margins the same way the subplot configuration tool does manually. :-)
plt.subplots_adjust(left=0.35, bottom=0.05, right=1, top=1)

sns.despine(left=True, bottom=True)
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(6)

ax.legend(prop=dict(size=6))
plt.show()

f.savefig('data/selectiveness-barplot.py-line137.png', format='png', dpi=300)

# Create the same plot but only selective authorities.
dfp = dfp.loc[(dfp['Selective'] > 0)]

# Example from https://pythonbasics.org/seaborn-barplot/
f, ax = plt.subplots(figsize=(6, 11))
sns.set_color_codes('pastel')
sns.barplot(x='Total', y='la_name', data=dfp,
            label='Total pupils', color='b', edgecolor='w')
sns.set_color_codes('muted')
sns.barplot(x='Selective', y='la_name', data=dfp,
            label='Pupils in grammars', color='b', edgecolor='w')

plt.xlabel('Pupil Numbers (2023/24)')
plt.ylabel('Local Authority')

ax.legend(ncol=1, loc='lower right', fontsize=10)

# This adjusts the margins the same way the subplot configuration tool does manually. :-)
plt.subplots_adjust(top=0.991, bottom=0.035, left=0.341, right=0.963)

sns.despine(left=True, bottom=True)
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(6)

ax.legend(prop=dict(size=6))
plt.show()

f.savefig('data/selectiveness-barplot.py-line165.png', format='png', dpi=300)

print('Selective schools exist in {0} local authorities.' .format(dfp.__len__()))
print('The proportions range from {0:.2f}% to {1:.2f}%.' .format(dfp.pct.min() * 100, dfp.pct.max() * 100))

# print('a line with no line break', end='')
# print(' finish the line')

minrow = dfp.loc[(dfp['pct'] ==  dfp.pct.min())].reset_index()
maxrow = dfp.loc[(dfp['pct'] ==  dfp.pct.max())].reset_index()
minla = minrow.iloc[0,0]
maxla = maxrow.iloc[0,0]

print('The proportions range from ', end='')
print('{0:.2f}% in {1} ' .format(dfp.pct.min() * 100, minla ), end='')
print('to {0:.2f}% in {1}.' .format(dfp.pct.max() * 100, maxla ))


