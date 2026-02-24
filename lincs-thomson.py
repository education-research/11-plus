"""
Thomson 1932 paper describes age weighting.
Here we use data from Lincs Consortium to recreate that.
Can we use modified box plots or violin plots to visualise Thomson's method.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import statsmodels.api as sm
matplotlib.use('Qt5Agg')

# Start with data exactly as disclosed by FOI
lincs = pd.read_csv('data/Lincolnshire_results_2019_Sent_2024-noPW.csv')

# WOB contains the *week* of birth. (See Tribunal decision
# https://caselaw.nationalarchives.gov.uk/ukftt/grc/2024/712?query=james+coombs#para_64)
# First convert this to Python date/time.

lincs['WOB'] = pd.to_datetime(lincs['WOB'], format='%Y-%m-%d')
lincs = lincs.sort_values(by='WOB', ascending=True)

# Top & tail DOBs outside the normal range of dates (01/09/2008 <= DOB <= 31/08/2009)

mask = (lincs['WOB'] >= '2008-09-01') & (lincs['WOB'] <= '2009-08-31')
lincs = lincs.loc[mask]

"""
WOB is aggregated by week. There are 52 full weeks. To recreate the Thomson method create 12 "months" which
approximately align with real calendar months (but arguably better from data analysis because they
each contain exactly 28 dates of birth.)
"""
# First create days older than the youngest in the df:
lincs['daysold'] = (lincs.iloc[-1,1] - lincs['WOB']).dt.days
# Then remove two weeks to lose the very youngest children and take the floor function of divided by 28 days
lincs['monthsold'] = (lincs['daysold'] - 14) // 28

# We still have a couple of weeks outside our modified 12 * 28 day year
mask = (lincs['monthsold'] < 12) & (lincs['monthsold'] >= 0)
# so create a copy for plotting with those weeks trimmed off.
plotdf = lincs.loc[mask]
plotdf = plotdf.sort_values(by='monthsold', ascending=True)

def monname(m):
    """
    :param m: monthsold in the range 0 - 11
    :return: a nice string
    """
    mons = ['Aug', 'Jul', 'Jun', 'May', 'Apr', 'Mar', 'Feb', 'Jan', 'Dec', 'Nov', 'Oct', 'Sep']
    return '10:' + str(m) + '\n(' + mons[m] + ')'


# print(monname(4))

"""
mdict = {0: 'Aug',1:  'Jul',2:  'Jun',3:  'May',4:  'Apr',5:  'Mar',
         6: 'Feb',7:  'Jan',8:  'Dec',9:  'Nov',10: 'Oct',11: 'Sep'}
"""
plotdf['Age at test'] = plotdf['monthsold'].apply(lambda x: monname(x))
plotdf = plotdf[plotdf['VRTotalRawScore'].notna()]

# This person answering had exact same idea as me, but handy to know *how*
# https://stackoverflow.com/questions/41529936/plot-additional-quantiles-on-seaborn-violin-plots#41538052

fig1, ax1 = plt.subplots(figsize=(14, 10))
sns.boxplot(data=plotdf, x='Age at test', y='VRTotalRawScore', showfliers=False, showbox=False, whis=[5, 95], ax=ax1)
sns.boxplot(data=plotdf, x='Age at test', y='VRTotalRawScore', showfliers=False, showbox=False, whis=[16, 84], ax=ax1)
sns.violinplot(data=plotdf, x='Age at test', y='VRTotalRawScore', ax=ax1, hue='Age at test')

x = plotdf.monthsold.unique().tolist()
x = sm.add_constant(x)

pc2iq = {5: 75, 16: 85, 50: 100, 84: 115, 95: 125}
for p in pc2iq.keys():
    print('adding regression line for percentile', p)
    # Draw regression line on the violin plot for percentile p
    # y needs to be an array of the current percentile for each month at percentile p.
    y = []
    for yy in range(0,12):
        # print(yy)
        y.append(plotdf['VRTotalRawScore'].loc[(plotdf['monthsold'] == yy)].quantile(p/100))

    result = sm.OLS(y, x).fit()
    y_pred = result.params[0] + result.params[1] * plotdf['monthsold'].unique()
    plt.plot(plotdf['Age at test'].unique(), y_pred, color='red', label='Regression Line')
    reglabel = 'SAS = ' + str(pc2iq[p])
#    ax1.text(5, y[5] +1, reglabel, fontsize=14, color='red')
    ax1.text(12.2, y_pred[11], reglabel, fontsize=14, color='red')


# Repeat the above loop but draw ONE 25% pass mark line
y = []
for yy in range(0,12):
    # print(yy)
    y.append(plotdf['VRTotalRawScore'].loc[(plotdf['monthsold'] == yy)].quantile(0.75))

result = sm.OLS(y, x).fit()
y_pred = result.params[0] + result.params[1] * plotdf['monthsold'].unique()
plt.plot(plotdf['Age at test'].unique(), y_pred, color='blue', label='Regression Line')
reglabel = 'Pct(75th)'
ax1.text(12.2, y_pred[11], reglabel, fontsize=14, color='blue')

fig1.suptitle('Thomson Age Weighting', y=0.94, fontsize=20, fontweight='bold', color='black')
plt.subplots_adjust(top=0.962, bottom=0.049,  left=0.029, right=0.93, hspace=0.2, wspace=0.2)
fig1.savefig('data/thomson-violin.py_line106.png', format='png', dpi=300)

