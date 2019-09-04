######################################################################
'''
Name: figure_10.py
By: D. Gold
Created: 4/30/18
 
This script will plot the safe operating space for a water supply portfolio
Portfolio S was called solution 1713 and portfolio B 1939
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
fig, ((ax1, ax3, ax4)) = plt.subplots(1, 3, figsize = (15,3))
axes = [ax1, ax3, ax4]

# this is for portfolio B, change to 1713 to make portfolio S
solution_num = '1939'

# load plot data df
sample_data = pd.read_csv('../Data/Solution'+str(solution_num)+'Samples_plot.csv')

util_letters = ['D_', 'R_', 'C_'] # used to extract columns for subplots
variables_wt = ['RT', 'TT', 'Cont', 'Ins', 'JLA']
variables_nt = ['RT', 'Cont', 'Ins', 'JLA']
maxes_DR = [.3, .3, .13, 5.0,.45]
maxes_C =[.3, .13, 4.0, .45]

# loop through utilities and DVs
for a, i in enumerate(util_letters):
    Safe = sample_data[sample_data[i+'all']>sample_data.iloc[-1][i+'all']] # unchanged solutions
    Danger = sample_data[sample_data[i+'all']<sample_data.iloc[-1][i+'all']] # worse solutions
    # Durham or Raleigh
    if a < 2:
        original = sample_data.iloc[-1][[i+'RT', i+'TT', i+'Cont', i+'Ins', i+'JLA']]
        SOS = np.ones([50,5])
        nSOS = np.ones([Danger.shape[0], 5])
        background_max = np.ones([1,5])
        background_min = np.zeros([1,5])
        for j, k in enumerate(variables_wt):
            if j < 2:
                SOS[:,j] = np.linspace(Safe[i+k].max(), Safe[i+k].min(), 50)/maxes_DR[j]
                nSOS[:,j] = np.linspace(Danger[i+k].max(), Danger[i+k].min(), Danger.shape[0])/maxes_DR[j]
                original[i+k] = original[i+k]/maxes_DR[j]
            elif j == 3:
                SOS[:,j] = (np.linspace(Safe['R_'+k].max(), Safe['R_'+k].min(), 50))/maxes_DR[j]
                nSOS[:,j] = (np.linspace(Danger['R_'+k].max(), Danger['R_'+k].min(), Danger.shape[0]))/maxes_DR[j]
                original[i+k] = .5
            else:
                SOS[:,j] = np.linspace(Safe[i+k].min(), Safe[i+k].max(), 50)/maxes_DR[j]
                nSOS[:,j] = np.linspace(Danger[i+k].min(), Danger[i+k].max(), Danger.shape[0])/maxes_DR[j]
                original[i+k] = original[i+k]/maxes_DR[j]
        SOS = pd.DataFrame(SOS, columns = [i+n for n in variables_wt])
        SOS = SOS.append(original, ignore_index=True)
        nSOS = pd.DataFrame(nSOS, columns = [i+n for n in variables_wt])
        background = np.concatenate((background_min, background_max))
        background = pd.DataFrame(background, columns = [i+n for n in variables_wt])
        n=0
    
    # Cary
    else:
        original = sample_data.iloc[-1][[i+'RT', i+'Cont', i+'Ins', i+'JLA']]
        background
        SOS = np.ones([50,4])
        nSOS = np.ones([Danger.shape[0], 4])
        background_max = np.ones([1,4])
        background_min = np.zeros([1,4])

        for j, k in enumerate(variables_nt):
            if j < 1: 
                SOS[:,j] = np.linspace(Safe[i+k].max(), Safe[i+k].min(), 50)/maxes_C[j]
                nSOS[:,j] = np.linspace(Danger[i+k].max(), Danger[i+k].min(), Danger.shape[0])/maxes_C[j]
                original[i+k] = original[i+k]/maxes_C[j]
            elif j ==2:
                SOS[:,j] = np.linspace(Safe[i+k].max(), Safe[i+k].min(), 50)/maxes_C[j]
                nSOS[:,j] = np.linspace(Danger[i+k].max(), Danger[i+k].min(), Danger.shape[0])/maxes_C[j]
                original[i+k] = .5
            else:
                SOS[:,j] = np.linspace(Safe[i+k].min(), Safe[i+k].max(), 50)/maxes_C[j]
                nSOS[:,j] = np.linspace(Danger[i+k].min(), Danger[i+k].max(), Danger.shape[0])/maxes_C[j]
                original[i+k] = original[i+k]/maxes_C[j]
        SOS = pd.DataFrame(SOS, columns = [i+n for n in variables_nt])
        SOS = SOS.append(original, ignore_index=True)
        nSOS = pd.DataFrame(nSOS, columns = [i+n for n in variables_nt])
        background = np.concatenate((background_min, background_max))
        background = pd.DataFrame(background, columns = [i+n for n in variables_nt])

    SOS['Name'] = 'Safe'
    nSOS['Name'] = 'unSafe'
    background['Name'] = 'background'
    SOS.iloc[-1, SOS.columns.get_loc('Name')] = 'Original'
    
    # reverse RT, TT and IT
    SOS[i+'RT'] = 1-SOS[i+'RT']
    SOS[i+'Ins'] = 1-SOS[i+'Ins']
    if a < 2:
        SOS[i+'TT'] = 1-SOS[i+'TT']


    nSOS[i+'RT'] = 1-nSOS[i+'RT']
    nSOS[i+'Ins'] = 1-nSOS[i+'Ins']

    if a < 2:
        nSOS[i+'TT'] = 1-nSOS[i+'TT']
    

    if a<2:
        min_labels = ['0.3\n' + variables_wt[0], '0.3\n' + variables_wt[1], '0.0\nCF', \
         '5\nIT',  '0.0\n' + variables_wt[4]]
        max_labels = ['0.0', '0.0', '0.1' , '1',  '0.45']
    else:
        min_labels = ['0.3\n' + variables_wt[0], '0.0\nCF', \
         '5\nIT',  '0.0\n' + variables_wt[4]]
        max_labels = ['0.0', '0.1' , '1',  '0.45']

    current_axis = axes[a]
    parallel_coordinates(background,'Name', color= [ '#810f7c'], \
    linewidth=5, alpha=0, ax=current_axis)
    parallel_coordinates(nSOS,'Name', color= [ '#810f7c'], \
     linewidth=5, alpha=.8, ax=current_axis)

    current_axis.set_ylim([0,1])
    current_axis.set_yticklabels([])
    current_axis.set_xticklabels(min_labels, fontsize=12)
    current_axis.get_legend().set_visible(False)

    print background.head()
    
    ax1 = current_axis.twiny()
    parallel_coordinates(background,'Name', color= [ '#810f7c'], \
     linewidth=5, alpha=0, ax=ax1)
    parallel_coordinates(nSOS,'Name', color= [ '#810f7c'], \
     linewidth=5, alpha=.8, ax=ax1)
    parallel_coordinates(SOS,'Name', color= [ '#9ebcda', '#000000'], \
     linewidth=5, alpha=.8, ax=ax1)

    ax1.xaxis.set_ticks_position('top')
    ax1.set_ylim([0,1])
    ax1.get_legend().set_visible(False)
    ax1.set_xticklabels(max_labels, fontsize=12)

# the two SOS's were combined in adobe illustrator
# to improve labeling aesthetics
plt.show()
#plt.savefig(solution_num+'_SOS.svg', bbox_inches='tight')
