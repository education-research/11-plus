"""
Version 1 works but has a lot of duplicated code for year 2017 and 2018.
Version 2 will put all that into a function. DOES NOT WORK. NO TIME TO DEBUG!
Version 3 Back to duplicated monolithic code because I have a writing deadline which is more important than
coding perfection!
Version 4 Good article here:
https://schoolsweek.co.uk/why-we-need-to-stop-talking-about-disadvantage-and-what-we-should-talk-about-instead/
Pupil-Premium entitlement was encoded as "[non-]disadvantage" when first written. The plots use these values for
the legend. Rather than rewrite all the code, the values are renamed. The text based results are just printed
to stdout but these are just renamed for the tables used in the paper.
Version 5 Noticed that standard deviation of PP-eligible "treatment" group is less than the full cohort so Glass's
delta would give a larger effect size. Unlikely to make much difference because the PP group are only about 1/8
of total. As part of final submission of the paper would like to automatically generate "Table 7" and consider
adding Glass's delta. At the risk of breaking everything, might fix the encoding of PP-eligible.

Version 6. Just changed wording on plots from "PP-Eligible" to "FSM6" which is the NPD attribute name.
Version 7. Uploaded data to github so script can load from there. Minor tweak to plot aesthetics.
"""

# import numpy as np
import pandas as pd
# import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
# from time import sleep
matplotlib.use('Qt5Agg')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['STIXGeneral'],
    'mathtext.fontset': 'stix',       # math symbols from STIX
    'mathtext.default': 'regular',    # make ALL math use the regular font
})

outdir = 'Bias_effect_size/output/'

# All data includes out of county candidates which need removing for two reasons
# 1) These applicants are mostly missing from the PP data.
# 2) These applicants are not representative. (In county children are automatically enrolled.)
print('Loading data and removing out of county records')

# Load the FSM6 data files, make initial count, drop out of county and print numbers.
fsm17 = pd.read_csv('https://github.com/education-research/11-plus/blob/main/data/Bucks-FSM6-2017.csv?raw=true')

# Make a note of how many, filter out the few out of county, print how many remain
n = len(fsm17)
fsm17 = fsm17.loc[(fsm17.Home == 'Buckinghamshire')]
print('2017: Out of a total', n, 'PP-eligible candidates,', len(fsm17), 'are "in county"')

# ... same again for 2018
fsm18 = pd.read_csv('https://github.com/education-research/11-plus/blob/main/data/Bucks-FSM6-2018.csv?raw=true')
n = len(fsm18)
fsm18 = fsm18.loc[(fsm18.Home == 'Buckinghamshire')]
print('2018: Out of a total', n, 'PP-eligible candidates,', len(fsm18), 'are "in county"')

# The grammar schools publish test data in PDF format, contrary to s.11 of The Re-use of Public Sector Information
# Regulations 2015! Results are published with various different candidate info but the ethnicity data was easiest to
# parse and convert from PDF to CSV.
csv17 = 'https://github.com/education-research/11-plus/blob/main/data/Bucks-2017_ethnicity.csv?raw=true'
csv18 = 'https://github.com/education-research/11-plus/blob/main/data/Bucks-2018_ethnicity.csv?raw=true'

all17 = pd.read_csv(csv17, usecols=['LA', 'STTS'])
n = len(all17)
all17 = all17.loc[(all17.LA == 'Buckinghamshire')]
print('2017:', n,'candidates in total. After removing "out of county" ones,', len(all17), 'records remaining')

all18 = pd.read_csv(csv18, usecols=['LA', 'STTS'])
n = len(all18)
all18 = all18.loc[(all18.LA == 'Buckinghamshire')]
print('2018:', n,'candidates in total. After removing "out of county" ones,', len(all18), 'records remaining')

# Now have two dataframes for each year containing only "in county" candidates' scores.
# One contains all candidates' scores, the other just FSM6.
fsm17 = fsm17.drop(columns=['Home'])
fsm18 = fsm18.drop(columns=['Home'])
all17 = all17.drop(columns=['LA'])
all18 = all18.drop(columns=['LA'])

# give cols the same names
all17.columns = ['Score']
all18.columns = ['Score']

all17 = all17.sort_values(by=['Score'], ignore_index=True)
all18 = all18.sort_values(by=['Score'], ignore_index=True)

# Create new columns in the 'all' dataframes intially setting PP eligibility to False
all17 = all17.assign(FSM6=False)
all18 = all18.assign(FSM6=False)

# Iterate over the "PP" dataframes then find a matching score in the "all" dataframe which is still False and reset
# PP_eligibility to True. I know iterrows gets bad press for performance. I'm not counting those milliseconds!

for index, row in fsm17.iterrows():
    idx = all17.loc[((all17.FSM6 == False) & (all17.Score == row['Score']))].index[0]
    all17.iloc[idx] = [row['Score'], True]

for index, row in fsm18.iterrows():
    idx = all18.loc[((all18.FSM6 == False) & (all18.Score == row['Score']))].index[0]
    all18.iloc[idx] = [row['Score'], True]


"""
# optional checks ... 
print('2017 length of all minus pp is', len(all17) - len(fsm17))
print(len(all17.loc[(all17.FSM6 == False)]), 'False in the dataframe')
print('2018 length of all minus pp is', len(all18) - len(fsm18))
print(len(all18.loc[(all18.FSM6 == False)]), 'False in the dataframe')
"""

all17['Year'] = '2017\n(CEM)'
all18['Year'] = '2018\n(GLA)'

# Version 5 will create a dataframe for the stats and iterate over both years using globals().
stats = pd.DataFrame(columns=['all17', 'all18'])

for y in ['all17', 'all18']:
    print('Updating', y)  # Fairly meaningless feedback!
    # Total candidates and numbers in the control and treatment groups for each year.
    stats.at['n=', y] = globals()[y].__len__()
    stats.at['non_FSM6', y] = globals()[y].loc[(globals()[y].FSM6 == False)].__len__()
    stats.at['FSM6', y] = globals()[y].loc[(globals()[y].FSM6 == True)].__len__()

    # %PP entitled each year
    stats.at['FSM6_pct', y] = stats[y]['FSM6'] / stats[y]['n=']
    # Cohort/control/treatment mean and standard deviations (grouped by category)
    stats.at['cohort_mean', y] = globals()[y]['Score'].mean()
    stats.at['cohort_std', y] = globals()[y]['Score'].std()

    stats.at['non_FSM6_mean', y] = globals()[y].loc[(globals()[y].FSM6 == False)]['Score'].mean()
    stats.at['non_FSM6_std', y] = globals()[y].loc[(globals()[y].FSM6 == False)]['Score'].std()

    stats.at['FSM6_mean', y] = globals()[y].loc[(globals()[y].FSM6 == True)]['Score'].mean()
    stats.at['FSM6_std', y] = globals()[y].loc[(globals()[y].FSM6 == True)]['Score'].std()

    # Cohen's & Glass's delta
    stats.at['Cohen_d', y] = (stats[y]['FSM6_mean'] -stats[y]['non_FSM6_mean']) / stats[y]['cohort_std']
    stats.at['Glass_d', y] = (stats[y]['FSM6_mean'] -stats[y]['non_FSM6_mean']) / stats[y]['non_FSM6_std']

    # Cohort/control/treatment pass rates
    stats.at['cohort_pass_rate', y] = len(globals()[y].loc[(globals()[y].Score >= 121)]) / len(globals()[y])
    stats.at['FSM6_pass_rate', y] = (len(globals()[y].loc[((globals()[y].Score >= 121) &
                                                         (globals()[y].FSM6 == True))]) /
                                   stats.at['FSM6', y])
    stats.at['non_FSM6_pass_rate', y] = (len(globals()[y].loc[((globals()[y].Score >= 121) &
                                                             (globals()[y].FSM6 == False))]) /
                                       stats.at['non_FSM6', y])


# rename the columns then output the stats as csv with full precision.
stats.columns = ['2017', '2018']
stats.to_csv('output/bucks-v7-table-line152.csv')


"""
 _____  _      ____ _______ 
|  __ \| |    / __ \__   __|
| |__) | |   | |  | | | |   
|  ___/| |   | |  | | | |   
| |    | |___| |__| | | |   
|_|    |______\____/  |_|   

Mr Tweedy: "Those chickens are up to something. They're organised. I know it."
Mrs Tweedy: "They're chickens, you dolt! Apart from you, they're the most stupid creatures on this planet. 
THEY DON'T PLOT!"
"""

# Seaborn assign the first hue to the first value it finds first. Sort the 2017 FSM6 to start with False
all17 = all17.sort_values(by=['FSM6'], ascending=True, ignore_index=True)
# df = pd.concat([all17, all18])

fig, axs = plt.subplots(nrows=2, sharex=False, figsize=(12, 5), dpi=100)
sns.violinplot(all17, x='Score', y='Year', hue='FSM6', split=True, inner=None, ax=axs[0])
sns.violinplot(all18, x='Score', y='Year', hue='FSM6', split=True, inner=None,  ax=axs[1])

axs[1].legend().remove()
axs[0].legend(ncol=1, title='FSM6', loc='upper left', fontsize=8)

axs[0].set_ylabel('', labelpad=1, fontsize=1)
axs[1].set_ylabel('', labelpad=1, fontsize=1)
axs[0].set_xlabel('', labelpad=1, fontsize=1)

plt.subplots_adjust(top=0.97, bottom=0.114, left=0.053, right=0.988, hspace=0.195, wspace=0.2)
axs[0].axvline(x=121, color='blue', linestyle='dotted', linewidth=1)
axs[1].axvline(x=121, color='blue', linestyle='dotted', linewidth=1)

fig.savefig(outdir + 'bucks6.py-line192.png', dpi=300)


