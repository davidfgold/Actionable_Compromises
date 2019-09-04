import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

# create figure
fig = plt.figure(figsize=(14,6)) # create the figure
ax = fig.add_subplot(1, 1, 1)    # make axes to plot on

# load data
data = pd.read_csv('../Data/Trindade_et_al_solution_robustness.csv')
utils = ['OWASA', 'Raleigh', 'Cary', 'Durham']

# Color will be minimum robustness across utilities
# scale by .7 to make colorbar readable
regional=data[utils].min(axis=1)/.7
data['regional'] = regional
data = data.sort_values(by='regional')

regional_plot = data['regional'].values

objectives = data[utils].values

# set colormap
cmap = matplotlib.cm.get_cmap("RdYlBu")

# Plot all solutions
for i in range(len(objectives[:,0])):
    ys = (objectives[i,:])
    xs = range(len(ys))
    ax.plot(xs, ys, c=cmap(regional_plot[i]), alpha=.8, linewidth=4)


ax.set_ylabel("% Satisficing \nPreference $\longrightarrow$", size= 18)
ax.set_ylim([0,1])
ax.set_yticklabels(['0', '20', '40', '60', '80', '100'])
ax.set_xticks([0,1,2,3])
ax.set_xticklabels([utils[i] for i in range(0, len(utils))], fontsize=18)
ax.set_xlim([0,3])

#Colorbar
sm = matplotlib.cm.ScalarMappable(cmap=cmap)
sm.set_array([0, .55])
cbar = fig.colorbar(sm, ticks=[0, .3, .55])
cbar.ax.set_yticklabels(['0%', '30%', '55%'])

# figure was edited in adobe illustrator to
# improve labeling aesthetics
plt.savefig('figure_5.svg', bbox_inches='tight')

