"""
Data is taken from Feldt, Leonard S, Manfred Steffen, and Naim C Gupta. 1985. A Comparison of Five Methods for
Estimating the Standard Error of Measurement at Specific Score Levels.
It took a lot of typing in!

Note this creates two plots because there didn't seem to be any way to add a single legend to the 3x2 plot.
The final plot is created using paintbrush to copy legend.png into feldt.png.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

df = pd.read_csv('data/feldt-data.csv')
methods = ['IRT', 'F(X^3)', 'Keats', 'CompBin', 'ANOVA']

# Create a weighted mean. Start by filling with zeros.
df['W_Mean'] = 0.1   # This forces new column to be float and avoids typeset future warning.
for test in ['V', 'L', 'SI']:
    for grade in [9, 11]:
        tempdf = df[((df['Test'] == test) & (df['Grade'] == grade))].copy()
        sumN = tempdf.N.sum()
        ar = []
        # work out the weighted mean SEM for each statistical method and append to ar
        for col in methods:
            cx = col + 'wm'
            # print(col, '->', cx)
            tempdf[cx] = tempdf[col] * tempdf['N']
            ar.append(tempdf[cx].sum() / sumN)

        # Set W_Mean for this test/grade to the mean value of ar.
        df.loc[(df['Test'] == test) & (df['Grade'] == grade), 'W_Mean'] = np.array(ar).mean()


# Start by plotting a single figure. Extract just wanted rows/columns then set x as the row index.
# cols = ['Test', 'Grade', 'x', 'N', 'IRT', 'F(X^3)', 'Keats', 'CompBin', 'ANOVA']
df = df.drop(columns=['N'])  # No longer needed now we have weighted means and deffo don't want on our plot!

rows = [9, 11]
cols = ['V', 'L', 'SI']
fig, ax = plt.subplots(figsize=(16, 8), dpi=100, nrows=2, ncols=3, sharey=True)

for r in [0, 1]:
    for c in [0, 1, 2]:
        # First create a plotting dataframe just containing the one test's results
        print('Plot rows that match Test =', cols[c] ,'and Grade =',rows[r])
        pdf = df[((df['Test'] == cols[c]) & (df['Grade'] == rows[r]))].copy()
        pdf = pdf.drop(columns=['Test', 'Grade'])
        pdf = pdf.set_index('x')
        # Next plot
        axx = sns.lineplot(data=pdf, linewidth=2, ax=ax[r,c], dashes=False)
        axx.get_legend().remove()
        # If row is 0 turn off xlabel and remove ticklabels.
        if r == 0:
            axx.set(xticklabels=[])
            axx.set_xlabel('')
        else:
            axx.tick_params(axis='x', labelrotation=90)
            axx.set_xlabel('Test: ' + cols[c], fontsize=16)
        if c == 0:
            axx.set_ylabel('Grade: ' + str(rows[r]), fontsize=16)



plt.subplots_adjust(top=0.988, bottom=0.074, left=0.034, right=0.994, hspace=0.036, wspace=0.026)
# plt.figlegend(ncol=6, fancybox=True, shadow=True, loc='lower left', bbox_to_anchor=(0.5, 0., 1, 0.1))

fig.savefig('data/feldt.png', dpi=300)

# figlegend() created a 6x6 legend although the legend is same for all six plots. Simple workaround is to create
# another single plot and then Paintbrush to use the legend from it. (Life's too short!)

fig2, ax = plt.subplots(figsize=(16, 8), dpi=300)
axx = sns.lineplot(data=pdf, linewidth=2, dashes=False)
plt.figlegend(ncol=6, fancybox=True, shadow=True, loc='lower left')
plt.figlegend(ncol=1, fancybox=True, shadow=True)

fig2.savefig('data/legend.png', dpi=600)
