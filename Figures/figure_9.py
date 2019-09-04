######################################################################
'''
Name: figure_9.py
By: D. Gold
Created: 10/8/18

Generate figure 9 from Gold et al., 2019 (In review)

This script plots heatmaps showing the results of the delta
global sensitivity analysis
'''
######################################################################

import numpy as np
import seaborn as sns;
import pandas as pd
import matplotlib.pyplot as plt
sns.set()

fig = plt.figure(figsize=(12,8))

# Durham
delta_results =pd.read_csv('../Data/Delta_SA/Durham_1713_norm_delta_indiv.csv', header=0, index_col=0)
important_factors = ['D_RT', 'D_TT', 'D_Co', 'D_Ins', 'DS', 'IS', 'FS', 'JL' ]
delta_plot = delta_results[important_factors]
ax = fig.add_subplot(3,2,1)
sns.heatmap(delta_plot, vmax=1, vmin=0, cmap='Greens', ax=ax, cbar=False)

delta_results =pd.read_csv('../Data/Delta_SA/Durham_1939_norm_delta_indiv.csv', header=0, index_col=0)
important_factors = ['D_RT', 'D_TT', 'D_Co', 'D_Ins', 'DS', 'IS', 'FS', 'JL' ]
delta_plot = delta_results[important_factors]
ax = fig.add_subplot(3,2,2)
sns.heatmap(delta_plot, vmax=1, vmin=0, cmap='Purples', ax=ax, cbar=False)

# Raleigh
delta_results =pd.read_csv('../Data/Delta_SA/Raleigh_1713_norm_delta_indiv.csv', header=0, index_col=0)
important_factors = ['R_RT', 'R_TT', 'R_Co', 'R_Ins', 'DS', 'IS', 'FS', 'JL' ]
delta_plot = delta_results[important_factors]
ax = fig.add_subplot(3,2,3)
sns.heatmap(delta_plot, vmax=1, vmin=0, cmap='Greens', ax=ax, cbar=False)

delta_results =pd.read_csv('../Data/Delta_SA/Raleigh_1939_norm_delta_indiv.csv', header=0, index_col=0)
important_factors = ['R_RT', 'R_TT', 'R_Co', 'R_Ins', 'DS', 'IS', 'FS', 'JL' ]
delta_plot = delta_results[important_factors]
ax = fig.add_subplot(3,2,4)
sns.heatmap(delta_plot, vmax=1, vmin=0, cmap='Purples', ax=ax, cbar=False)

# Cary
delta_results =pd.read_csv('../Data/Delta_SA/Cary_1713_norm_delta_indiv.csv', header=0, index_col=0)
important_factors = ['C_RT', 'C_Co', 'C_Ins', 'DS', 'IS', 'FS', 'JL' ]
delta_plot = delta_results[important_factors]
ax = fig.add_subplot(3,2,5)
sns.heatmap(delta_plot, vmax=1, vmin=0, cmap='Greens', ax=ax, cbar=False)

delta_results =pd.read_csv('../Data/Delta_SA/Cary_1939_norm_delta_indiv.csv', header=0, index_col=0)
important_factors = ['C_RT', 'C_Co', 'C_Ins', 'DS', 'IS', 'FS', 'JL' ]
delta_plot = delta_results[important_factors]
ax = fig.add_subplot(3,2,6)
sns.heatmap(delta_plot, vmax=1, vmin=0, cmap='Purples', ax=ax, cbar=False)

plt.subplots_adjust(hspace=.3)

# figure was edited in adobe illustrator
# to improve labeling aesthetics
plt.savefig('Figure_9.svg', bbox_inches='tight')
