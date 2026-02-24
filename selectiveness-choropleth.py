"""
Parents in Kent were unaware that other parts of the country don't have the 11+ !

This prompted a quick plot of the total number of school places, and grammar school places for each local
authority based on DfE data here:
https://explore-education-statistics.service.gov.uk/find-statistics/school-pupils-and-their-characteristics

This has ended up as two scripts.
This script plots a choropleth map showing where selection is most concentrated.
selectiveness3.py plots a vertical bar chart.

These two plots were then manually edited to create the composite plot.

"""

import seaborn as sns
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib
matplotlib.use('Qt5Agg')

# Load shapefile for unitary authorities.
fp = 'data/GIS/Counties_and_Unitary_Authorities_May_2023_UK_BFC_3040607888653097481/CTYUA_MAY_2023_UK_BFC.shp'
map_df = gpd.read_file(fp)
# check data type so we can see that this is not a normal dataframe, but a GEOdataframe
# map_df.head()
# That loaded all of uk. We just want England.
map_df = map_df.loc[map_df.CTYUA23CD.str.startswith('E')]

# Preview map with no data in it
# map_df.plot()
# plt.show()

cols = ['new_la_code', 'time_period', 'la_name', 'sex_of_school_description', 'phase_type_grouping',
        'type_of_establishment', 'denomination', 'admissions_policy', 'urban_rural', 'academy_flag',
        'number_of_key_stage_3_pupils_years_7_to_9', 'number_of_key_stage_4_pupils_years_10_and_11']

# load ~163k rows covering all years from 2015/16 and all school types.
df = pd.read_csv('data/spc_school_characteristics_.csv', usecols=cols)

# Filter records to select latest year and education phase "state funded secondary" (~3k remain).
df = df.loc[((df.time_period == df.time_period.max()) & (df.phase_type_grouping == 'State-funded secondary'))]

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

# Main dataframe now contains 151 counties' state funded secondary schools for a single year with four
# type of 'admissions_policy'. These types are Total, Non-selective, Selective and Unknown.
# Unknown are always non-selective (having extensively checked this before).

# check a single familiar county
check = df.loc[(df.la_name == 'Buckinghamshire')]
# Tidy up
check = check.drop(columns=['time_period', 'sex_of_school_description', 'phase_type_grouping',
                            'type_of_establishment', 'denomination', 'urban_rural', 'academy_flag',
                            'number_of_key_stage_3_pupils_years_7_to_9',
                            'number_of_key_stage_4_pupils_years_10_and_11'])

print(check.pivot_table(index='la_name', columns='admissions_policy', values='roll'))
sel = check.roll.values[1]
tot = check.roll.values[2]
print('CHECK:', sel, 'out of', tot, 'children in Bucks are in grammars. This is', sel/tot, 'of the total')

# PREP DATA for PLOTTING. THIS BIT DOES THE BAR CHART. I'm going to duplicate some code because it's easier.
# Seaborn normally prefers 'tall/long' data but this plot works by plotting both the total and then
# selective pupils on the same figure so the data needs to be transformed to a 'wide' format.
dfp = df.pivot_table(index='la_name', columns='admissions_policy', values='roll')
dfp = dfp.drop(columns=['Non-selective', 'Not applicable', 'Unknown'])
dfp = dfp.reset_index()
dfp.Selective = pd.to_numeric(dfp.Selective, errors='coerce').fillna(0).astype(np.int64)
dfp.Total = pd.to_numeric(dfp.Total, errors='coerce').fillna(0).astype(np.int64)
dfp = dfp.sort_values(['Selective', 'Total'], ascending=[False, False])
dfp['pct'] = dfp.Selective / dfp.Total

# dfp.to_csv('c:/_python/normal/data/dfp.csv', index=False)
# need to add 'new_la_code' to dfp so it can be used for the choropeth map as well as the bar chart.
# create an 'index' dataframe that just maps LA name to new code
dfi = df[['new_la_code', 'la_name']]
dfi = dfi.dropna()
dfi = dfi.drop_duplicates()
# Use this to insert a new column new_la_code as per
# https://stackoverflow.com/questions/41511730/python-function-similar-to-vlookup-excel#41511789
dfp.insert(2, 'new_la_code', dfp['la_name'].map(dfi.set_index('la_name')['new_la_code']))
# print(dfp)

"""
 _____  _      ____ _______ __  __          _____  
|  __ \| |    / __ \__   __|  \/  |   /\   |  __ \ 
| |__) | |   | |  | | | |  | \  / |  /  \  | |__) |
|  ___/| |   | |  | | | |  | |\/| | / /\ \ |  ___/ 
| |    | |___| |__| | | |  | |  | |/ ____ \| |     
|_|    |______\____/  |_|  |_|  |_/_/    \_\_|     
                                                   
This bit needs writing. Dataframe dfp has new la codes which should match the shapefile loaded above
which should allow me to plot where selective places are by proportions ... although I need to learn how!                                               

"""

merged = map_df.set_index('CTYUA23CD').join(dfp.set_index('new_la_code'))
merged['percent'] = merged.pct * 100
# set a variable that will call whatever column we want to visualise on the map
variable = 'percent'

# set the range for the choropleth
vmin, vmax = 0, 36

# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(12, 12))

# create map
merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')

# Now we can customise and add annotations
# remove the axis
ax.axis('off')

# add a title
ax.set_title('Percentage of selective school places\nin Engand by unitary authority',
             fontsize=20, fontweight='bold', color='black')

# create an annotation for the  data source
ax.annotate('Source: geoportal.statistics.gov.uk, 2024',
            xy=(0.1, .08), xycoords='figure fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=10, color='#555555')

# Create colorbar as a legend
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm)

# plt.ylabel('Percent selectivity', y=0.5, x=0.5)
plt.subplots_adjust(left=0.01, bottom=0.01, right=1, top=0.98)
plt.subplots_adjust(top=0.957, bottom=0.046, left=0.033, right=0.992, hspace=0.2, wspace=0.2)
# this will save the figure as a high-res png. you can also save as svg
fig.savefig('data/selectiveness.choropleth-300dpi.png', format='png', dpi=300)

