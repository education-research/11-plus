"""
The latest House of Commons library reseach briefing is here:
https://commonslibrary.parliament.uk/research-briefings/sn07070/
I asked nicely and they gave me the data behind the two graphs in section 5.1. :-)
The "percentage of maintained secondary school pupils taught in grammar schools" agrees with my figures but is
marginally higher than Allen's figures for "national share of pupils" which I assume includes children in private
education. Allen (2016):
https://ffteducationdatalab.org.uk/2016/09/there-is-not-yet-a-proven-route-to-help-disadvantaged-pupils-into-grammar-schools/

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.lines as mlines

matplotlib.use('Qt5Agg')

df = pd.read_csv('data/parliament-data.csv')
# Latest research paper says the pre-1967 data relates to both England and Wales (although there isn't a noticeable
# step change. Wales population is relatively small). Include just the England data.

df = df.loc[(df['scope'] == 'England')]
df = df.drop(columns=['scope'])  # no longer needed so tidy up.

# The percentage of children in grammars is very precisely but verbosely defined. For coding lets be more pithy.
df.columns = ['year', 'schools', 'percentage']

plt.rcParams["axes.labelsize"] = 14
fig, ax1 = plt.subplots(figsize=(16, 8), dpi=100)
lp1 = sns.lineplot(data=df, x='year', y='percentage', ax=ax1, color='blue', linewidth=2)
# clone the axis
ax2 = ax1.twinx()
lp2 = sns.lineplot(data=df, x='year', y='schools', ax=ax2, color='green', linewidth=2)

fig.suptitle('Percentage of maintained secondary school pupils taught in grammar schools and the number of schools',
             fontsize=16, fontweight='bold')

ax1.tick_params(axis='y', colors='blue')
ax1.yaxis.label.set_color('blue')
ax1.set(ylabel='Percentage of children in grammars')

ax2.tick_params(axis='y', colors='green')
ax2.yaxis.label.set_color('green')
ax2.set(ylabel='Number of grammar schools')
ax1.set(xlabel='year')

blue = mlines.Line2D([], [], color='blue', label='% pupils in grammar schools')
green = mlines.Line2D([], [], color='green', label='Number of grammar schools')
plt.legend(handles=[blue, green], fontsize='large', fancybox=True, shadow=True, loc='upper right')
plt.subplots_adjust(top=0.94, bottom=0.073, left=0.039, right=0.95, hspace=0.2, wspace=0.2)
# NB .figure.text() is positioned relative to final window so adjust it first (line above) before adding text.
source = 'Data source:\nHouse of Commons Library'
lp1.figure.text(0.05, 0.1, source, fontsize=14)

fig.savefig('data/parliament-figures.py.png', dpi=300)

