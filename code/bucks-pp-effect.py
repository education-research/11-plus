"""
This script compares the 11-plus test scores of children eligible for Pupil Premium funding to those non-eligible.
Data provided by Buckinghamshire Council and The Buckinghamshire Grammar Schools for 2017 and 2018 test.
In total, over 10,000 samples.

This prints a lot of summary stats to STDOUT (sorry!) and creates a rather impressive violin plot showing the
gap between PP eligible True|False candidates.

"""

indir = 'data/bucksCC_FOI/'

import numpy as np
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

# All data includes out of county candidates which need removing for two reasons
# 1) These candidates are not captured by the PP data.
# 2) These candidates are not representative.
print('Loading PP eligible scores and removing out of county records')
# Load the four data files, make initial count, drop out of county and print numbers.
pp17 = pd.read_csv(indir + 'PP-2017.csv')
n = len(pp17)
pp17 = pp17.loc[(pp17.Home == 'Buckinghamshire')]
print('2017 PP eligible:', len(pp17), 'records remain from', n)

pp18 = pd.read_csv(indir + 'PP-2018.csv')
n = len(pp18)
pp18 = pp18.loc[(pp18.Home == 'Buckinghamshire')]
print('2018 PP eligible:', len(pp18), 'records remain from', n)

all17 = pd.read_csv(indir + '2017_ethnicity_validate.csv', usecols=['LA', 'STTS'])
n = len(all17)
all17 = all17.loc[(all17.LA == 'Buckinghamshire')]
print('2017 all in-county candidates:', len(all17), 'records remain from', n)

all18 = pd.read_csv(indir + '2018_ethnicity_validate.csv', usecols=['LA', 'STTS'])
n = len(all18)
all18 = all18.loc[(all18.LA == 'Buckinghamshire')]
print('2018 all in-county candidates:', len(all18), 'records remain from', n)

# More trouble than it's worth to put this into two iteration loops
pp17 = pp17.drop(columns=['Home'])
pp18 = pp18.drop(columns=['Home'])
all17 = all17.drop(columns=['LA'])
all18 = all18.drop(columns=['LA'])

# give cols the same names
all17.columns = ['Score']
all18.columns = ['Score']

# The 'all' dataframes now contain the scores for both PP and non-PP.
# Sort by score and then add column marking them all as non-PP
all17 = all17.sort_values(by=['Score'], ignore_index=True)
all18 = all18.sort_values(by=['Score'], ignore_index=True)

all17['SES'] = 'Non-PP'
all18['SES'] = 'Non-PP'

# Next iterate over both pp dataframes and reset an SES value for each to 'PP' in the all dataframes.


for index, row in pp17.iterrows():
    # find first match row with the score AND SES == 'non-PP' then update it to SES == 'PP'
    idx = all17.loc[((all17.SES == 'Non-PP') & (all17.Score == row['Score']))].index[0]
    all17.iloc[idx] = [row['Score'], 'PP']

for index, row in pp18.iterrows():
    # find first match row with the score AND SES == 'non-PP' then update it to SES == 'PP'
    idx = all18.loc[((all18.SES == 'Non-PP') & (all18.Score == row['Score']))].index[0]
    all18.iloc[idx] = [row['Score'], 'PP']


"""
# comment out manual checks ... 
print('2017 length of all minus pp is', len(all17) - len(pp17))
print(len(all17.loc[(all17.SES == 'Non-PP')]), 'non-PP still in the dataframe')
print('2018 length of all minus pp is', len(all18) - len(pp18))
print(len(all18.loc[(all18.SES == 'Non-PP')]), 'non-PP still in the dataframe')
"""

def printstats(y):
    """
    :param y: two-digit year as a STRING
    :return: none - just formats the summary stats
    """
    w = 12
    p = 8
    print(f'Year\t\t\tValue\tStatistic')
    print('=========================================================')
    print(f'20{y}\t{nds:{w}}\tNon-PP sample size')
    print(f'20{y}\t{pps:{w}}\tPP sample size')
    print(f'20{y}\t{mun:{w}.{p}}\tNon-PP mean score')
    print(f'20{y}\t{mud:{w}.{p}}\tPP mean score')
    print(f'20{y}\t{std:{w}.{p}}\tOverall standard deviation')
    print(f'20{y}\t{(mun - mud)/std:{w}.{p}}\tEffect size')
    print(f'20{y}\t{ppn:{w}.{p}}\tProportion of Non-PP passing')
    print(f'20{y}\t{ppd:{w}.{p}}\tProportion of PP passing')


# **2017** Basic stats, pass rates and effect sizes
std = all17.Score.std()
mun = all17.loc[(all17.SES == 'Non-PP')].Score.mean()
mud = all17.loc[(all17.SES == 'PP')].Score.mean()
# Pass mark is "fixed" at 121. Mean and standard deviation is then contorted to the right numbers "pass"!
ppn = len(all17.loc[((all17.SES == 'Non-PP') & (all17.Score >= 121))]) / \
      len(all17.loc[(all17.SES == 'Non-PP')])
ppd = len(all17.loc[((all17.SES == 'PP') & (all17.Score >= 121))]) / \
      len(all17.loc[(all17.SES == 'PP')])
nds = len(all17) - len(pp17)
pps = len(pp17)
printstats('17')
print('\n')

# **2018** Basic stats, pass rates and effect sizes
std = all18.Score.std()
mun = all18.loc[(all18.SES == 'Non-PP')].Score.mean()
mud = all18.loc[(all18.SES == 'PP')].Score.mean()
# Pass mark is "fixed" at 121. Mean and standard deviation is then contorted to the right numbers "pass"!
ppn = len(all18.loc[((all18.SES == 'Non-PP') & (all18.Score >= 121))]) / \
      len(all18.loc[(all18.SES == 'Non-PP')])
ppd = len(all18.loc[((all18.SES == 'PP') & (all18.Score >= 121))]) / \
      len(all18.loc[(all18.SES == 'PP')])
nds = len(all18) - len(pp18)
pps = len(pp18)
printstats('18')

all17['Year'] = '2017\n(CEM)'
all18['Year'] = '2018\n(GLA)'

# plus the stats I decided later I should've included before!
print('2017 mean', all17.Score.mean())
print('2017 std dev', all17.Score.std())
print('2017 skew', all17.Score.skew())

print('2018 mean', all18.Score.mean())
print('2018 std dev', all18.Score.std())
print('2018 skew', all18.Score.skew())

# Re-encode Non-PP as False and PP as True to simplify the plot

all17 = all17.replace('Non-PP', 'False')
all17 = all17.replace('PP', 'True')
all18 = all18.replace('Non-PP', 'False')
all18 = all18.replace('PP', 'True')

all17.columns = ['Score', 'Pupil-Premium-eligible', 'Year']
all18.columns = ['Score', 'Pupil-Premium-eligible', 'Year']


"""
 _____  _      ____ _______ 
|  __ \| |    / __ \__   __|
| |__) | |   | |  | | | |   
|  ___/| |   | |  | | | |   
| |    | |___| |__| | | |   
|_|    |______\____/  |_|   
                            
"""

# sns.violin will assign the first hue it finds first. Sort 'Pupil-Premium-eligible' so it starts with False
all17 = all17.sort_values(by=['Pupil-Premium-eligible'], ascending=True, ignore_index=True)
# df = pd.concat([all17, all18])

fig, axs = plt.subplots(nrows=2, sharex=False, figsize=(12, 5), dpi=300)
sns.violinplot(all17, x='Score', y='Year', hue='Pupil-Premium-eligible', split=True, ax=axs[0])
sns.violinplot(all18, x='Score', y='Year', hue='Pupil-Premium-eligible', split=True, ax=axs[1])

axs[0].legend().remove()
axs[1].legend(ncol=1, loc='upper right', fontsize=8)

axs[0].set_ylabel('', labelpad=1, fontsize=1)
axs[1].set_ylabel('', labelpad=1, fontsize=1)
axs[0].set_xlabel('', labelpad=1, fontsize=1)

plt.subplots_adjust(left=0.05, bottom=0.11, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
axs[0].axvline(x=121, color='blue', linestyle='dotted', linewidth=1)
axs[1].axvline(x=121, color='blue', linestyle='dotted', linewidth=1)

fig.savefig('data/bucks-pp-effect.py-line184.png', dpi=450)
