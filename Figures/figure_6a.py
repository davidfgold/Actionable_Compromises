######################################################################
'''
Name: figure_6a.py
By: D. Gold
Created: 10/31/17

Generate figure 6a from Gold et al., 2019 (In review)
'''
###################################################################### 

import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
plt.style.use('ggplot')

# create figure
fig = plt.figure(figsize=(10,2)) # create the figure
ax = fig.add_subplot(1, 1, 1)    # make axes to plot on

# load data
data = pd.read_csv('../Data/Trindade_et_al_solution_robustness.csv')
utils = ['OWASA', 'Raleigh', 'Cary', 'Durham']

objectives = data[utils].values
colors = np.ones(objectives.shape[0])*.3
colors[-1] = 0
colors[-2] = 1

cmap_grey = matplotlib.cm.get_cmap("binary")

# Plot all solutions
for i in range(len(objectives[:,0])):
    ys = (objectives[i,:])
    xs = range(len(ys))
    if i < objectives.shape[0]-2:
    	ax.plot(xs, ys, c=cmap_grey(colors[i]), alpha=.5, linewidth=5)
    elif i < objectives.shape[0]-1:
    	ax.plot(xs, ys, c='#4daf4a', alpha=.7, linewidth=5)
    else:
        ax.plot(xs, ys, c='#984ea3', alpha=.7, linewidth=5)

ax.set_ylabel("% Satisficing \nPreference $\longrightarrow$", size= 18)
ax.set_ylim([0,1])
ax.set_yticklabels(['0', '20', '40', '60', '80', '100'])
ax.set_xticks([0,1,2,3])
ax.set_xticklabels([utils[i] for i in range(0, len(utils))], fontsize=18)
ax.set_xlim([0,3])

# figure was edited in adobe illustrator
# to improve labeling aesthetics
plt.savefig('Figure_6a.svg', bbox_inches='tight')


