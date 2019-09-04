######################################################################
'''
Name: figure_6c.py
By: D. Gold
Created: 10/31/17

Generate figure 6c from Gold et al., 2019 (In review)
'''
###################################################################### 
import numpy as np
import os
import pandas as pd
from pandas.tools.plotting import parallel_coordinates
import matplotlib.pyplot as plt
import seaborn as sns
 
# create figure, 4 subplots
sns.set()
fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(1, 4, figsize = (10,2))
axes = [ax1, ax2, ax3, ax4]

# load plot data df
sample_data = pd.read_csv('../Data/Decision_variables.csv')
print sample_data.head()

util_letters = ['O_', 'R_', 'C_', 'D_'] # used to extract columns for subplots
variables_wt = ['RT', 'TT', 'Cont', 'Ins', 'JLA']
variables_nt = ['RT', 'Cont', 'Ins', 'JLA']
maxes_DR = [.3, .3, .1, 5.0, .15]
maxes_C =[.3, .1, 4.0, .15]

# loop through utilities and DVs
for a, i in enumerate(util_letters):
    # Durham, OWASA or Raleigh
    if a != 2:
        original = sample_data[['Name', i+'RT', i+'TT', i+'Cont', i+'Ins', i+'JLA']]
        for j, k in enumerate(variables_wt):
            if j < 4:
                original[i+k] = original[i+k]/maxes_DR[j]
            else:
                original[i+k] = 1-((.15-original[i+k])/.1)

        print original.head()
    # Cary
    else:
        original = sample_data[['Name', i+'RT', i+'Cont', i+'Ins', i+'JLA']]
        for j, k in enumerate(variables_nt):
            if j !=3: 
                original[i+k] = original[i+k]/maxes_C[j]
            else:
                original[i+k] = 1-((.40-original[i+k])/.1)
    
    # reverse RT, TT and IT
    if a != 2:
        original[i+'TT'] = 1-original[i+'TT']

    original[i+'RT'] = 1-original[i+'RT']
    original[i+'Ins'] = 1-original[i+'Ins']

    if a == 0:
        original[i+'TT'] = 0
        original[i+'RT'] = 0
 
    if a!=2:
        min_labels = ['0.3\n' + variables_wt[0], '0.3\n' + variables_wt[1], '0.0\nCF', \
         '5\nIT',  '0.05\n' + variables_wt[4]]
        max_labels = ['0.0', '0.0', '0.1' , '1',  '0.15']
    else:
        min_labels = ['0.3\n' + variables_wt[0], '0.0\nCF', \
         '5\nIT',  '0.30\n' + variables_wt[4]]
        max_labels = ['0.0', '0.1' , '1',  '0.40']

    current_axis = axes[a]
    print original.head()

    parallel_coordinates(original,'Name', color= ['#4daf4a', '#984ea3'], \
     linewidth=3, alpha=.7, ax=current_axis)


    current_axis.set_ylim([0,1])
    current_axis.set_yticklabels([])
    current_axis.set_xticklabels(min_labels, fontsize=12)
    current_axis.get_legend().set_visible(False)

    ax1 = current_axis.twiny()

    parallel_coordinates(original,'Name', color= ['#4daf4a', '#984ea3'], \
     linewidth=3, alpha=0, ax=ax1)

    ax1.xaxis.set_ticks_position('top')
    ax1.set_ylim([0,1])
    ax1.get_legend().set_visible(False)
    ax1.set_xticklabels(max_labels, fontsize=12)

# figure was edited in adobe illustrator
# to improve labeling aesthetics
plt.savefig('Figure_6c.svg', bbox_inches='tight')
