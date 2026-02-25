"""
Inspired by Figure 1 on page 21 of, Coe et al (2008) "Evidence on the effects of selective educational system"
https://www.suttontrust.com/wp-content/uploads/2019/12/SuttonTrustFullReportFinal-1.pdf.

This shows a bivariate distribution with 0.7 correlation to illustrate the false classifications between
11+ score and attainment at 16+ (on the basis that the former should ideally predict the latter.)
... although they actually show a pass mark that selects *29%* of candidates and error is always greater
in the middle of the score range so they may have slightly exaggerated the classification error.
(See Feldt et al "Comparison of Five Methods for Estimating the Standard Error at Specific Score Levels."
https://conservancy.umn.edu/server/api/core/bitstreams/fef84c51-9d3e-4cec-9a00-e8d37fac2a18/content )
This script repeats with the correct pass mark.

"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# Set random seed so it plots the same "random" figure each time. (Comment out next line for some variety.)
np.random.seed(42)

"""
 ____ _______      __     _____  _____       _______ ______ 
|  _ \_   _\ \    / /\   |  __ \|_   _|   /\|__   __|  ____|
| |_) || |  \ \  / /  \  | |__) | | |    /  \  | |  | |__   
|  _ < | |   \ \/ / /\ \ |  _  /  | |   / /\ \ | |  |  __|  
| |_) || |_   \  / ____ \| | \ \ _| |_ / ____ \| |  | |____ 
|____/_____|   \/_/    \_\_|  \_\_____/_/    \_\_|  |______|
Create a bivariate distribution based on provided pararmeters
"""


def binorm(n, tmin, tmax, r):
    """
    :param n:       sample size
    :param tmin:    "target" min. below this values are reduced by cubic root.
    :param tmax:    "target" max. above this values are reduced by cubic root.
    :param r:       reliabiity of x to predict y - ie the target Pearson correlation coefficient
    :return: dataframe with two columns containing a bivariate distribution.
    """
    cov = np.array([[1, r], [r, 1]])
    pts = np.random.multivariate_normal([0, 0], cov, size=n)

    print('check mean values should be close to zero', pts.mean(axis=0))
    print('check covariance matrix:\n', np.cov(pts.T))
    print('check the correlation coefficient is close to wanted value:', np.corrcoef(pts.T)[0, 1])

    # put numpy array into Pandas dataframe
    dfx = pd.DataFrame(data=pts, columns=['X', 'Y'])
    # This section takes cubic root of any values beyond 2σ. Doesn't change the quantiles but makes graphs look nicer
    for c in dfx.columns:
        print('truncating', c)
        print('before min max values are', dfx[c].min(), dfx[c].max())
        dfx[c] = dfx[c].apply(lambda x: x if x > -2 else -2 + ((x + 2) ** 1/3))
        dfx[c] = dfx[c].apply(lambda x: x if x < +2 else +2 + ((x - 2) ** 1/3))
        print('after min max values are', dfx[c].min(), dfx[c].max(), '\n')
    return dfx


df = binorm(1000, -2, +2, 0.7)

"""
  _____  _____          _      ______ 
 / ____|/ ____|   /\   | |    |  ____|
| (___ | |       /  \  | |    | |__   
 \___ \| |      / /\ \ | |    |  __|  
 ____) | |____ / ____ \| |____| |____ 
|_____/ \_____/_/    \_\______|______|
Adjust the bivariate to given parameters                                      
This does not work as a function! 

for cdf in [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]:
    print(cdf)	
    plotcoe('11+ score', 'GCSE Attain8', cdf, '0.7')


"""

xmu = 100               # mean value of X           (as per 11+)
xstd = 15               # standard deviation of X   (as per 11+)
ymu = 50                # mean value of Y           (as per GCSE)
ystd = 20               # standard deviation of Y   (as per GCSE)

# create a new dataframe so we retain the unscaled normalised version
dfs = pd.DataFrame()
dfs['X'] = df['X'] * xstd + xmu
dfs['Y'] = df['Y'] * ystd + ymu


"""
 _____  _      ____ _______ 
|  __ \| |    / __ \__   __|
| |__) | |   | |  | | | |   
|  ___/| |   | |  | | | |   
| |    | |___| |__| | | |   
|_|    |______\____/  |_|   

This was original written as a function but only called once so all the hassle and none of the benefits. 
It still helps to set some variables which are used a few times before the code which was in the function. 
"""

xl = '11-plus score'
yl = 'GCSE 8 aggregate scores (final school exams at age 16)'
p = 0.75
r = 0.7

"""
:param xl:  x-axis label
:param yl:  y-axis label
:param p:   "pass rate" (quantile where we want to draw refline and calculate quantiles)
:param r:   reliability (used to create initial bivariate dataset)
:return:    nowt!
"""
xq = dfs['X'].quantile(q=p)
yq = dfs['Y'].quantile(q=p)
print('debug xq and yq are', xq, yq)
n = dfs.__len__()
tp = dfs.loc[(dfs['X'] >= xq) & (dfs['Y'] >= yq)].__len__() * 100 / n
tn = dfs.loc[(dfs['X'] <  xq) & (dfs['Y'] <  yq)].__len__() * 100 / n
fp = dfs.loc[(dfs['X'] >= xq) & (dfs['Y'] <  yq)].__len__() * 100 / n
fn = dfs.loc[(dfs['X'] <  xq) & (dfs['Y'] >= yq)].__len__() * 100 / n
tp = 'True positive\n(' + str(tp) + '%)'
tn = 'True negative\n(' + str(tn) + '%)'
fp = 'False positive\n(' + str(fp) + '%)'
fn = 'False negative\n(' + str(fn) + '%)'
# plot with seaborn
g3 = sns.jointplot(data=dfs, x='X', y='Y', color='#4CB391', marginal_ticks=True, height=10,
                   xlim=(60, 140), ylim=(0, 100))
plt.plot([60, 138.5], [0, 100], color='red', linewidth=1)
g3.refline(x=xq, y=yq, color='black', dashes=(2, 1), linewidth=0.75)
g3.figure.text(0.65, 0.75, tp, fontsize=14)
g3.figure.text(0.15, 0.15, tn, fontsize=14)
g3.figure.text(0.65, 0.15, fp, fontsize=14)
g3.figure.text(0.15, 0.75, fn, fontsize=14)
plt.xlabel(xl, fontsize=14)
plt.ylabel(yl, fontsize=14)
plt.suptitle('Predictive validity at ' + str(r) + ' correlation', y=0.1)
g3.figure.savefig('data/class_acc.py_line142.png', format='png', dpi=300)

