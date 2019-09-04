######################################################################
'''
Name: figure_7a.py
By: D. Gold
Created: 4/8/18

Generate figure 7a from Gold et al., 2019 (In review)

This script will plot parallel coordinate plots of the robustness of each objective
Each axis represents a utility, each line a solution.
Robustness is defined as the % states of the world where the given objective meets
prespecified satisficing criteria.
'''
###################################################################### 

import numpy as np
import os
import pandas as pd
from pandas.tools.plotting import parallel_coordinates
import matplotlib.pyplot as plt
import seaborn



# solution 1713 is portfolio S in the Paper, solution 1939 is portfolio B

solutions = [1713, 1939]

colors = [['#4daf4a', '#b2df8a'], ['#984ea3', '#cab2d6']]
# create figure, 4 subplots
fig, ((ax1, ax2, ax3), (ax5, ax6, ax7)) = plt.subplots(2, 3, figsize = (8,3))

axes = [[ax1, ax2, ax3], [ax5, ax6, ax7]]

for j, solution in enumerate(solutions):
	print j
	titles = ['Durham', 'Raleigh', 'Cary']

	Odata = pd.read_csv('../Data/OriginalSatisficing_plot.csv')
	Osolution = Odata.loc[Odata['Sample']==solution] 

	Osolution['Name'] = 'Original'

	Psolution = pd.read_csv('../Data/satisficing_' + str(solution) + '.csv', header=1, names=['Sample', \
		'D_all', 'D_Rel', 'D_RF', 'D_WCC', 'O_all', 'O_Rel', 'O_RF', 'O_WCC', 'R_all', 'R_Rel', \
		 'R_RF', 'R_WCC', 'C_all', 'C_Rel', 'C_RF', 'C_WCC'])

	Psolution['Name'] = 'Perturbed'

	objs = [['D_Rel', 'D_RF', 'D_WCC','D_all','Name'], ['R_Rel', 'R_RF', 'R_WCC', 'R_all', 'Name'], \
	['C_Rel', 'C_RF', 'C_WCC', 'C_all','Name']]

	x_axis_titles = ['Rel', 'RF','WCC', 'All']

	# plot 2 parallel coordinate plots
	for i,f in enumerate(titles):
	 	current_axis = axes[j][i]
	 	Oplot_data = Osolution[objs[i]]
	 	Pplot_data = Psolution[objs[i]]
		parallel_coordinates(Pplot_data,'Name', color= colors[j][1], \
			linewidth=3, alpha=.9, ax=current_axis)
		parallel_coordinates(Oplot_data,'Name', color= colors[j][0], \
			linewidth=3, alpha=.8, ax=current_axis)
		current_axis.set_ylim([0,1000])
		current_axis.set_xticklabels([])
		if j == 0:
			current_axis.set_title(titles[i], fontsize = 12)
		if j > 0:
			current_axis.set_xticklabels(x_axis_titles)
			if i ==1:
				current_axis.set_xlabel('Criteria', fontsize = 12)
		if i == 0:
			current_axis.set_yticks([0, 250, 500, 750, 1000])
			current_axis.set_yticklabels(['0', '25', '50', '75', '100'], fontsize=8)
		else:
			current_axis.set_yticklabels([])
		current_axis.legend(loc='lower right',ncol=1, fontsize=10)
		if i !=3:
			current_axis.legend_.remove()

# figure was edited in adobe illustrator
# to improve labeling aesthetics
plt.savefig('Figure_7a.svg', bbox_inches='tight')