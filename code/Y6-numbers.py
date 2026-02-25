
"""
This provides an *authoritative* script for finding the number of Y6 children in all schools ... but can be
modified to return other figures.

Data downloaded from:
https://explore-education-statistics.service.gov.uk/find-statistics/school-pupils-and-their-characteristics
Location may change but searching for "Schools, pupils and their characteristics" should find the latest.
There should be a "download all data" link.
The zip file contains a number of files and filenames change but the relevant one is invariably the biggest!
Data needs extracting to a suitable location.
"""

import pandas as pd

fcols = ['time_period', 'geographic_level', 'sex_of_school_description', 'phase_type_grouping',
         'type_of_establishment', 'denomination', 'admissions_policy', 'urban_rural', 'academy_flag']
# Have never seen any part time Y6 pupils but load these columns anyway.
dcols = ['full_time_female_year_group_6', 'full_time_male_year_group_6',
         'part_time_female_year_group_6', 'part_time_male_year_group_6']

spc = 'C:/docs/_datasets/_SPC/school-pupils-and-their-characteristics_2024-25/data/spc_school_characteristics.csv'
df = pd.read_csv(spc, usecols=fcols + dcols)

# Create a new column with the total Y6 on roll
df['Y6'] = 0
for c in dcols:
    df['Y6'] = df['Y6'] + df[c]

print('Initial row count', df.__len__())
print('select just National records')
df = df.loc[(df.geographic_level == 'National')]
print('Row count now', df.__len__())

# Array slice [1:] selects all but the first 'geographic_level'
for c in fcols[2:]:
    print('filter', c, 'to only include Total')
    df = df.loc[(df[c] == 'Total')]
    print('Row count now', df.__len__())


df = df.sort_values(by=['time_period'])
# keep just the relevant cols
df = df[['time_period', 'full_time_female_year_group_6', 'full_time_male_year_group_6', 'Y6']]
df.columns = ['Year', 'Y6 girls', 'Y6 boys', 'Y6 total']

print(df.to_string(index=False))
df.to_csv('data/y6-numbers.py_line48.csv', index=False)

# Plot horizontal bar using the example (which matches the % in grammars by LA) at
# https://seaborn.pydata.org/examples/part_whole_bars.html
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

# Do I need to convert Year to object?
df['Year'] = df.Year.astype(str)

# Plot the total pupils, both boys and girls but label legend as girls.
f, ax = plt.subplots(figsize=(12, 8))
sns.set_theme(style='whitegrid')
sns.set_color_codes('pastel')
sns.barplot(x='Y6 total', y='Year', data=df, label='Y6 Girls', color='b')

# Plot just boys on top of girls
sns.set_color_codes('muted')
sns.barplot(x='Y6 boys', y='Year', data=df,
            label='Y6 boys', color='b')

# Add labels etc.
url = 'https://explore-education-statistics.service.gov.uk/find-statistics/school-pupils-and-their-characteristics'
ax.set_xlabel('Source: ' + url ,fontsize=10, fontweight='bold')
ax.set_ylabel('Academic Year' ,fontsize=14, fontweight='bold')
sns.despine(left=True, bottom=True)
f.suptitle('Total Year 6 children across all school types', fontsize=14, fontweight='bold', color='black')
f.text(202425, 400000, 'Source:' + url)
plt.subplots_adjust(top=0.956, bottom=0.053, left=0.059, right=0.984,hspace=0.2, wspace=0.2)
f.savefig('data/Y6-numbers.py_line79.png', format='png', dpi=300)
