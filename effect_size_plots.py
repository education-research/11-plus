"""
Results of research give the following effect sizes for different "treatments"
One year’s intense tutoring	            +2.63σ
Entitlement to Pupil Premium funding	-0.89σ
Candidates 4 months older           	+0.117σ

This script will plot a control group (assuming no skew or kurtosis and continuous rather than discrete) then
plot the other "treatments" on the same graph so they can be visually compared.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Qt5Agg')

# Parameters for the normal distribution
mean = 100
std_dev = 15

# Generate some data
x = np.linspace(40, 160, 1000)
y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)


def plott(d, lab, col, w):
    """
    ("plot" feels like it should be a reserved word so add another t)
    Print the distribution transformed by its effect size (Cohen's d) on the figure created above.
    :param d:       Effect size (control group equals zero)
    :param lab:     Label for the legend
    :param col:     Colour to use
    :param w:       Line width
    """
    # Standard deviation is 15 so need to multiply Cohen's d by this amount to show it in "marks"
    d = d * 15
    plt.plot(x + d, y, label=lab, color=col, linewidth=w)
    plt.axvline(x=d + 100, color=col, linestyle='dotted', linewidth=1)
    print('Mean score for', lab, 'is', d+100)


# Create a figure then fill it with plots.
fig, ax = plt.subplots(figsize=(16, 8), dpi=150)
plott(0, 'control', 'orange', 2)
plott(2.63, 'coached', 'blue',1)
plott(-0.89, 'low SES', 'red', 1)
plott(0.117, 'old in year', 'green', 1)

# add grey dash at the nominal 25% pass mark
plt.axvline(110, color='grey', linestyle='dashed', linewidth=1)

# tidy up some aesthetics
plt.ylim(0, )
plt.xlim(40,180)
ax.set_xlabel('11-plus scores' ,fontsize=14, fontweight='bold')
ax.set_ylabel('Probability Density' ,fontsize=14, fontweight='bold')
ax.set_yticks([])
ax.set_yticklabels([])
plt.subplots_adjust(top=0.981, bottom=0.079, left=0.025, right=0.982)
fig.legend(fontsize=16)

fig.savefig('data/effect_size_plots.py_line62.png', dpi=300)

