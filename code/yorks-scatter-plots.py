"""
Data provided by North Yorks County Council:
https://www.whatdotheyknow.com/request/linked_data_on_11_tests#incoming-986716
This script expects to find this in a subdirectory called 'data'.

Works out the occasion reliability for tests taken a week apart and plots "before and after"

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Qt5Agg')

rip = pd.read_excel(open('data/Response to FOI N2526 NorthYorkshire Results Raw and Standardised.xlsx', 'rb'),
                    sheet_name='Ripon Grammar School ')

erm = pd.read_excel(open('data/Response to FOI N2526 NorthYorkshire Results Raw and Standardised.xlsx', 'rb'),
                    sheet_name='Ermysteds Grammar School ')

# col names are identical so ...
scores = pd.concat([rip, erm], ignore_index=True)
del rip
del erm

# Remove the dates, raw scores and total. (Column headers are not clear!)
cols = ['1st test NVR', '2nd Test NVR', '1st test VR ', '2nd test VR ',  'Score']
scores.drop(cols, axis=1, inplace=True)

# Give remaining columns some sensible names
cols = ['Area', 'NVR_1_Raw', 'NVR_1_SAS', 'NVR_2_Raw', 'NVR_2_SAS', 'VR_1_Raw', 'VR_1_SAS', 'VR_2_Raw', 'VR_2_SAS']
scores.columns = cols

scores['Tot_1_Raw'] = scores.NVR_1_Raw + scores.VR_1_Raw
scores['Tot_1_SAS'] = scores.NVR_1_SAS + scores.VR_1_SAS
scores['Tot_2_Raw'] = scores.NVR_2_Raw + scores.VR_2_Raw
scores['Tot_2_SAS'] = scores.NVR_2_SAS + scores.VR_2_SAS


"""
 _____  _      ____ _______ _____ 
|  __ \| |    / __ \__   __/ ____|
| |__) | |   | |  | | | | | (___  
|  ___/| |   | |  | | | |  \___ \ 
| |    | |___| |__| | | |  ____) |
|_|    |______\____/  |_| |_____/ 
                                  
"""

def plotyorks(x, y, t):
    """
    :param x: string containing the x-value in scores.
    :param y: string containing the y-value in scores.
    :param t: string what to call the version written to file.
    :return:
    jointplot with KDE margins look good but not a figure level function so have to create three individual plots
    then use image editing software to join them together.
    """
    mx = pd.concat([scores[x], scores[y]], ignore_index=True).max()
    mn = pd.concat([scores[x], scores[y]], ignore_index=True).min()
    f = sns.jointplot(scores, x=x, y=y, hue='Area')
    plt.legend(ncol=1, loc='upper left', fontsize=8)
    plt.xlim(mn -2, mx + 2)
    plt.ylim(mn -2, mx + 2)
    c = scores[x].corr(scores[y])
    c = round(c, 4)
    c = t + '\nρ=' + str(c)
    f.ax_joint.text(mx * 0.9, mn * 1.05, c)
    f.savefig('data/yorks-scatter.py_line77_' + t + '.png', format='png', dpi=300)
    del f, mx


plotyorks('NVR_1_Raw', 'NVR_2_Raw', 'Non-Verbal Raw')
plotyorks('VR_1_Raw', 'VR_2_Raw', 'Verbal Raw')
plotyorks('Tot_1_Raw', 'Tot_2_Raw', 'Total Raw')
plotyorks('NVR_1_SAS', 'NVR_2_SAS', 'Non-Verbal SAS')
plotyorks('VR_1_SAS', 'VR_2_SAS', 'Verbal SAS')
plotyorks('Tot_1_SAS', 'Tot_2_SAS', 'Total SAS')


