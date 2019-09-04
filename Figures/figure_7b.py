######################################################################
'''
Name: figure_7b.py
By: D. Gold
Created: 12/8/18

Generate figure 7b from Gold et al., 2019 (In review)

this script plots cdfs of performance across perturbed portfolios
generated from 2 compromise portolios. Cdfs are plotted for 3 objectives 
and 3 utilities.

the original portfolio cdf is plotted as a dark line, perturbed portfolios
are plotted as lightly shaded lines.
'''
######################################################################

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# plotting function, to be called in loop below
def plot_cdf(util, axis, obj, sol):
	# load the data
	name = '../Data/implementation_tolerances/' + util + '_' + \
	obj + '_' + sol + '.csv'
	og_name = '../Data/implementation_tolerances/' + util +'_' \
	+ obj + '_original_' + sol + '.csv'
	data = np.loadtxt(name, delimiter=',')
	og_data = np.loadtxt(og_name, delimiter=',')

	# plotting cdf, make array from 0-999
	ranks = np.arange(0,1000)
	# ended up trimming this because 1000 was too much detail
	filtered_ranks = ranks[np.arange(0,1000,20)]

	# plot every 20th point
	for i in range(0,1024):
		col = data[np.arange(0,1000,20),i]
		# two colors, one for solution 1713, the other for 1939
		if sol=='1713':
			axis.plot(col, filtered_ranks, c='#a1d99b', linewidth=.3)
		else:
			axis.plot(col, filtered_ranks, c='#bcbddc', linewidth=.3)

	# plot the original solutions
	if sol=='1713':
		axis.plot(og_data[np.arange(0,1000,20)], filtered_ranks, c ='#005a32', linewidth=2)
	else:
		axis.plot(og_data[np.arange(0,1000,20)], filtered_ranks, c ='#4a1486', linewidth=2)
	
	# format axes and plot satisficing criteria

	# reliability
	if obj == 'rel':
		axis.plot(np.ones(1000)*.01, ranks, '--', c='black', linewidth=1)
		axis.set_xlim([0,.2])
		axis.set_xlabel('Reliability', fontsize=8)
		axis.set_xticks([0, .06666, .133333, .2])
		axis.set_xticklabels(['100%', '', '', '80%'], fontsize=6)
		axis.set_ylim([0,980]) # fix indexing
		if sol == '1713':
			axis.set_ylabel(util, fontsize=8)
			axis.set_yticks([0, 245, 490, 735, 980])
			axis.set_yticklabels(['0', '', '', '', '1.0'], fontsize=6)
		else:
			axis.set_yticks([0, 245, 490, 735, 980])
			axis.set_yticklabels([])

	# restriction frequency
	elif obj == 'rf':
		axis.plot(np.ones(1000)*.2, ranks, '--', c='black', linewidth=1)
		axis.set_xlim([0,.5])
		axis.set_xlabel('Restriction Freq.', fontsize=8)
		axis.set_xticks([0, .1666, .33333, .5])
		axis.set_xticklabels(['0%', '', '', '50%'], fontsize=6)
		axis.set_ylim([0,980]) # fix indexing
		axis.set_yticks([0, 245, 490, 735, 980])
		axis.set_yticklabels([])
	
	# worst case cost
	else:
		axis.plot(np.ones(1000)*.05, ranks, '--', c='black', linewidth=1)
		axis.set_xlim([0,.35])
		axis.set_xlabel('Worst Case Cost', fontsize=8)
		axis.set_xticks([0, .1166, .2332, .35])
		axis.set_xticklabels(['0%', '', '', '35%'], fontsize=6)
		axis.set_ylim([0,980]) # fix indexing
		axis.set_yticks([0, 245, 490, 735, 980])
		axis.set_yticklabels([])
	if util != 'Cary':
		axis.set_xticklabels([])
		axis.set_xlabel('')

	return()


# set up the figure, each axis represents a subplot
# this line creates a matplotlib plot that is empty but
# has 18 subplots
fig, ((ax1, ax2, ax3, ax10, ax11, ax12), \
	(ax4, ax5, ax6, ax13, ax14, ax15), \
	(ax7, ax8, ax9, ax16, ax17, ax18)) \
	 = plt.subplots(3, 6, figsize = (8,4))

# here I create an array to store the handel of each subplot
axes = [[ax1, ax2, ax3], [ax4, ax5, ax6], [ax7, ax8, ax9], \
 [ax10, ax11, ax12], [ax13, ax14, ax15], [ax16, ax17, ax18]]

# vector of utilities and objectives
utils = ['Durham', 'Raleigh', 'Cary']
objs = ['rel', 'rf', 'wcc']

# make the plots, loop through utilities (column) and obj (rows)
for i in range(0,3):
	for j in range(0,3):
		plot_cdf(utils[i],axes[i][j], objs[j], '1713')
		plot_cdf(utils[i], axes[i+3][j], objs[j], '1939')

# figure was edited in adobe illustrator
# to improve labeling aesthetics
plt.savefig('Figure_7b.svg', bbox_inches='tight', format='svg')






