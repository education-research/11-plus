"""
The Sunday Times newspaper annually publishes its "Parent Power league tables".
The "Top 400 state schools" was downloaded on 11/12/2024.
Further work was then done to link these data to the DfE prior cohort KS2 SAT tests and Attainment8 final exam results
The final cleaned up data file read into this is:
ParentPowerCLEAN+GIAS.csv
This still has 400 records but contains 39 non-English schools and 3 more which are missing the DfE data so the first
step is to filter these out.

This script then plots the data, works out correlations, etc.
OUTPUTS
There is a single joint plot written at line 55 (yeah line numbers keep changing!)
Three individual joint plots come out near line 86. These can then be concatenated into a single plot.
Some linear regression analysis writes residuals info to data/pp_residuals.csv

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Qt5Agg')

pp = pd.read_csv('data/ParentPowerCLEAN+GIAS.csv')

# Drop some unwanted columns
cols = ['Rank', 'School', 'Type', 'A-level(%A*)', 'A-level(% A*/A)', 'A-level(%A*/B)', 'A-level_rank',
        'GCSE_rank', 'FINAL URL ']
pp = pp.drop(columns=cols)

# Give the columns nicer names!
cols = ['Town', 'Times_rating', 'School_Name', 'KS2score', 'Attain8']
pp.columns = cols

# Had earlier issues with too many Queen Eliabeths!
# tmp = pp.loc[pp['School_Name'].str.contains('lizabet')]
# print(tmp[['Times_rating','KS2score', 'Attain8']].corr())

# remove 36 non-English and 3 with missing DfE data (values == 0)
print('Starting with', pp.__len__(), 'records')
pp = pp.loc[(pp.School_Name != 'not an English school')]
print('Removed non-English schools', pp.__len__(), 'records remaining')
pp = pp.loc[(pp.KS2score != 0)]
print('Removed schools missing DfE data', pp.__len__(), 'records remaining')

# create some summary stats for a table in the paper.
print(pp[['Times_rating', 'KS2score', 'Attain8']].describe())
pp[['Times_rating', 'KS2score', 'Attain8']].describe().to_csv('data/ppstats.csv')


def ppplot(x, y, xl, yl):
    """
    Seaborn jointplot adds marginal distributions but can't plot in an array so need to do each separately
    :param x:   x!
    :param y:   y!
    :param xl:  x label
    :param yl:  y label
    :return:
    """
    sns.jointplot(pp, x=x, y=y, kind='reg', height=8, ratio=6)
    plt.xlabel(xl)
    plt.ylabel(yl)
    cor = pp[x].corr(pp[y])
    cor = round(cor, 4)
    cor = ' (ρ=' + str(cor) + ')'
    xpos = (pp[x].max() - pp[x].min()) * 0.7 + pp[x].min()
    ypos = (pp[y].max() - pp[y].min()) * 0.1 + pp[y].min()
    plt.text(xpos, ypos, cor, fontsize=12)
    title = yl + ' ~ ' + xl
    plt.suptitle(title, y=0.98,  fontsize=14, fontweight='bold')
    # NB to frig this to keep the scatter plot 1:1 square ratio AND have a title need to increase left and
    # and top margins by the same amounts!
    # plt.subplots_adjust(left=0.083, bottom=0.073, right=0.981, top=0.981, wspace=0.2, hspace=0.2)
    plt.subplots_adjust(right=0.96, top=0.96)
    plt.savefig('data/ParentPowerPlot-v2.py-line86' + xl + yl + '.png', dpi=300)


# NB the jointplot is a figure-level function meaning the only way to create a "single" plot with all three
# graphs is to do them one at a time then use paintbrush to stitch them together
ppplot('KS2score', 'Attain8',   'DfE KS2 score',    'DfE Attainment 8')
ppplot('KS2score', 'Times_rating', 'DfE KS2 score',    'Times attainment rating')
ppplot('Attain8', 'Times_rating',  'DfE Attainment 8', 'Times attainment rating')

"""
 _____  ______ _____ _____  ______  _____ _____ _____ ____  _   _ 
|  __ \|  ____/ ____|  __ \|  ____|/ ____/ ____|_   _/ __ \| \ | |
| |__) | |__ | |  __| |__) | |__  | (___| (___   | || |  | |  \| |
|  _  /|  __|| | |_ |  _  /|  __|  \___ \\___ \  | || |  | | . ` |
| | \ \| |___| |__| | | \ \| |____ ____) |___) |_| || |__| | |\  |
|_|  \_\______\_____|_|  \_\______|_____/_____/|_____\____/|_| \_|

Calculate correlation and regression values.  

"""

# print correlation matrix.
corr = pp[['Times_rating','KS2score', 'Attain8']].corr()
print(corr)
corr.to_csv('data/corr2.csv')

# Check the residuals from Times_rating ~ Attain8
lm = smf.ols(formula='Times_rating ~ Attain8', data=pp).fit()
print(lm.summary())
# add another column with predicted PP_rating based on DfE Attain8.
pp['Times_predA8'] = pp.Attain8 * lm.params.iloc[1] + lm.params.iloc[0]
# Calculate residuals. (NB postive values should be where Times' figure is higher than might be expected.)
pp['Times_predA8_resid'] = pp.Times_rating - pp.Times_predA8


# Check the residuals from Attain8 ~ KS2score
lm = smf.ols(formula='Attain8 ~ KS2score', data=pp).fit()
print(lm.summary())
# add another column with predicted PP_rating based on DfE Attain8.
pp['A8_predKS2'] = pp.KS2score * lm.params.iloc[1] + lm.params.iloc[0]
# Calculate residuals. (NB postive values should be where Times' figure is higher than might be expected.)
pp['A8_predKS2_resid'] = pp.Attain8 - pp.A8_predKS2


# Check the residuals from Times ~ KS2score
lm = smf.ols(formula='Times_rating ~ KS2score', data=pp).fit()
print(lm.summary())
# add another column with predicted PP_rating based on DfE Attain8.
pp['Times_predKS2'] = pp.KS2score * lm.params.iloc[1] + lm.params.iloc[0]
# Calculate residuals. (NB postive values should be where Times' figure is higher than might be expected.)
pp['Times_predKS2_resid'] = pp.Attain8 - pp.Times_predKS2

# Calculate the absolute values of the outlier so we can sort.
pp['abs'] = abs(pp.Times_predA8_resid)

pp = pp.sort_values(by='abs', ascending=False)

pp.to_csv('data/ParentPowerPlot.py_line133_residuals.csv')

