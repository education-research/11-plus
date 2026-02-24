"""
Using data from Lincs Consortium which includes raw, standardised and (aggregated) age, this script works out
normal age standardised scores, plots them against the GLA SAS scores then adds a logistic function curve which
rather conclusively proves there is no substance to the claimed proprietary maths.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Qt5Agg')
plt.rcParams['font.family'] = 'Times New Roman'  # Works for labels but does not in raw strings.
# modified the matplotlibrc file to use serif font family ... but it doesn't work!

# Start with the data as disclosed by FOI
lincs = pd.read_csv('data/Lincolnshire_results_2019_Sent_2024-noPW.csv')
lincs['WOB'] = pd.to_datetime(lincs['WOB'], format='%Y-%m-%d')
# Following two lines could be one but using a mask means it's possible to view the series to see if it looks ok.
mask = (lincs['WOB'] >= '2008-09-01') & (lincs['WOB'] <= '2009-08-31')
lincs = lincs.loc[mask]
# Create days older than the youngest in the df:
lincs['daysold'] = (lincs.WOB.min() - lincs['WOB']).dt.days + 365
# candidates ages in days now range from 1 to 365 but in multiples of 7 (+1)

# The next section of code interpolates exact date of birth based on location. (The muppets sorted before aggregate!)
# The method is so complex I didn't understand how it worked five minutes after writing it. (Essentially keeps
# incrementing the DOB until enough of that day have been created, appending to an array which becomes a df column.)
# Go look at the dataframe to see what it does!
aa = []
for d in lincs.daysold.unique():
    print('guessterpolating DOBs for daysold = ', d)

    n = len(lincs[(lincs['daysold'] == d)])
    tt = []   # list of 'triggers'
    for t in range(1, 8):
        # print(t)
        tt.append(t * n/7)


    dd = d
    i = 0
    for trigger in tt:
        print('keep adding until we reach or pass', trigger)
        while i < trigger:
            aa.append(dd)
            i += 1
        dd += 1


# correct the first ten entries which are the last day of August
for i in range(0,10):
    aa[i] = 7

# Finally, add that array as a column which has the relative age in days of all candidates.
lincs['age_days'] = aa
lincs['age_days'] = lincs['age_days'] - 6

# The age of all candidates now ranges between 1 and 365 days. :-)

# Create a new dataframe with just wanted columns. (Verbal Reasoning is prob better for studying age-weighting.)
verb = lincs[['age_days','VRTotalRawScore', 'SASVR']].copy()
verb.columns = ['age_days', 'raw', 'sas']
verb = verb.dropna()

# tidy up unused variables ...
del aa,d,dd, i, mask, n, t, trigger, tt

"""
Standardise the raw scores the standard way
"""

lm = smf.ols(formula='raw ~ age_days', data=verb).fit()
# print(lm.summary())
# print(lm.pvalues)
# print(lm.params)

print('Scores are {0:.2f} + {1:.4f} for each day older the candidate is.'
      .format(lm.params.iloc[0],lm.params.iloc[1]))

# Create raw but age-weighted scores. It's all relative because final results are rescaled (mu=100, sig=15) but
# *SUBTRACT* the coefficient for each day candidate is *OLDER*
verb['raw_aw'] = verb.raw - (verb.age_days * lm.params.iloc[1])

mu = verb['raw_aw'].mean()
sig = verb['raw_aw'].std()

# Standardise the results the standard way! (z = (x - mu)/sigma * 15 + 100)
verb['z'] = (verb['raw_aw'] - mu) / sig * 15 + 100
"""
# Confirm that worked ...
lm = smf.ols(formula='z ~ age_days', data=verb).fit()
print('age_days coefficient should be vanishingly small (viz zero with some rounding error.)', lm.params.iloc[1])
# ... and maybe have a look at the results in Excel
# verb.to_csv('data/verb.csv')
"""

"""
1) Plot the normal standardised results against GLA's
2) Add logistic curve with suitable parameters to demonstrate this is the relationship.
(The parameters weren't conjured out of thin air. See lgf.py  
"""

#verb['j'] = np.random.uniform(-.5, .5, verb.shape[0])
verb['xjit'] = verb.sas + np.random.uniform(-.5, .5, verb.shape[0])
# Check that xjit looks correct.
# sns.scatterplot(verb, x='xjit', y='sas', ax=ax1)

fig1, ax1 = plt.subplots(figsize=(15, 10))
sns.scatterplot(verb, x='xjit', y='z', ax=ax1)
ax1.set_xlim(60, 150)
ax1.set_ylim(55, 130)
ax1.axvline(x=110, color='red', linestyle='dotted', linewidth=1)
ax1.axhline(y=101, color='red', linestyle='dotted', linewidth=1)

plt.subplots_adjust(top=0.98, bottom=0.061, left=0.046, right=0.983, hspace=0.2, wspace=0.2)

a = np.arange(-10, 10, 0.1)
b = (1 / (1 + np.exp(-a))) - 0.5
xt, yt, xs, ys = 105, 95, 16, 76
plt.plot(a * xs + xt, b * ys + yt, color='red')

xlab = 'Lincolnshire Consortium Verbal Reasoning 2019 (logit transformation: Schagan (1990))'
ylab = 'Conventional age-standardision (no transformation)'
ax1.set_xlabel(xlab, fontsize=14)
ax1.set_ylabel(ylab, fontsize=14)

# plt.text(130, 57, 'f(x) = ln[x/(1-x)] (Schagan 1990)', fontsize=14)
plt.text(144, 125, r'$\mathdefault{  f(x)=\frac{1}{1+e^{-x}}         }$', fontsize=14)

fig1.savefig('data/lincs-gla-fit-fig2.png', dpi=300)

