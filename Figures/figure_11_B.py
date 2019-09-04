######################################################################
'''
Name: figure_11_S.py
By: D. Gold
Created: 4/30/18
 
This script will plot factor maps for portfolio B
'''
###################################################################### 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from logisticRegressionTools import set_thresholds
from logisticRegressionTools import fitAllLogit
from logisticRegressionTools import plotCombinedFactorMaps
import sys

# set solution number
solution_num = '1939'

# load DVs, Normalize and add intercepts
DV_names = ['D_RT', 'R_RT', 'C_RT', 'D_TT', 'O_TT', 'R_TT', 'D_Cont', 'O_Cont', \
	'R_Cont', 'C_Cont', 'D_Ins', 'O_Ins', 'R_Ins', 'C_Ins', 'D_JLA', 'R_JLA', 'O_JLA', 'C_JLA']
DVs = pd.read_csv('../Regression_input/DVs/DV_' + solution_num +'_all.csv', names=DV_names)

# Isolate Cary JLA
C_JLA = DVs['C_JLA'] 

OriginalDVs = pd.read_csv('../Parameter_ranges/' + solution_num + 'OriginalDVs.csv', names=[\
	'D_RT', 'R_RT', 'C_RT', 'D_TT', 'O_TT', 'R_TT', 'D_Cont', 'O_Cont', \
	'R_Cont', 'C_Cont', 'D_Ins', 'O_Ins', 'R_Ins', 'C_Ins', 'D_JLA', 'R_JLA', 'O_JLA', 'C_JLA'])

# normalize DV values
DVparamBounds =np.genfromtxt('../Parameter_ranges/' + solution_num + 'DV_Ranges.csv', delimiter=',')
for i, col in enumerate(DVs.columns):
        DVs[col] = (DVs[col] - DVparamBounds[i,0])/(DVparamBounds[i,1] - DVparamBounds[i,0])
        OriginalDVs[col] = (OriginalDVs[col] - DVparamBounds[i,0])/(DVparamBounds[i,1] - DVparamBounds[i,0])


# load DU factors, normalize
DU_factor_names = ['Inflow_scale', 'Evap_scale', 'Elast_scale', 'Reductions_scale', 'Reductions_lag', \
	'Peaking_Scale', 'Demand_grow_scale', 'Demand_std', 'Falls_sup', 'JL_sup', 'Cary_cap', \
	'Trans_cap', 'Trans_cost', 'Ins_prem']

DU_factors = pd.read_csv('../Regression_input/DU_repeated.csv', names=DU_factor_names)


# Fix cary JLA
C_JLA = C_JLA * DU_factors['JL_sup']
C_JLA = (C_JLA - C_JLA.min())/(C_JLA.max() - C_JLA.min())

# normalize
DUparamBounds =np.genfromtxt('../Parameter_ranges/DU_factor_ranges.csv', delimiter=',')

for i, col in enumerate(DU_factors.columns):
        DU_factors[col] = (DU_factors[col] - DUparamBounds[i,0])/(DUparamBounds[i,1] - DUparamBounds[i,0])

# add intercept column
DU_factors['intercept'] = np.ones(np.shape(DVs)[0])

LHBase = np.ones([1,len(DU_factor_names)])*.5
DU_base = pd.DataFrame(data=LHBase, columns=DU_factor_names)

# load objectives and establish regional criteria
obj_names = ['D_Rel', 'D_RF', 'D_AC', 'D_WCC', 'O_Rel', 'O_RF', 'O_AC', 'O_WCC', 'R_Rel', 'R_RF', 'R_AC', \
	'R_WCC', 'C_Rel', 'C_RF', 'C_AC', 'C_WCC']

objs = pd.read_csv('../Regression_input/obj/obj_' + solution_num + '_all.csv', names=obj_names)

# set robustness criteria
All_robustness, Durham_all, Durham_Rel, Durham_RF, Durham_WCC, Raleigh_all, Raleigh_Rel, \
	Raleigh_RF, Raleigh_WCC, Cary_all, Cary_Rel, Cary_RF, Cary_WCC = set_thresholds(objs)

# Durham
fig = plt.figure()
sns.set()
levels = np.linspace(0,1.00, 201)

ax = fig.add_subplot(1,1,1)

DUPredictors1 = ['intercept', 'Demand_grow_scale']
DVPredictors = [ 'D_RT']
DUPredictors2 = ['Inflow_scale']

combinedPredictors = pd.concat([DU_factors[DUPredictors1], DVs[DVPredictors], DU_factors[DUPredictors2]], axis=1)
result = fitAllLogit(objs, Durham_all, combinedPredictors)
plotCombinedFactorMaps(ax, result, 'Durham', 'Demand Growth Scaling Factor', 'Restriction Trigger (ROF)',
	 [0, .5, 1], ['0.5', '1.0', '2.0'], [0, .2, .4, .6, .8, 1], \
	 ['0', '0.02', '0.04', '0.06', '0.08', '0.10'], [], [], DUPredictors2, DU_base, levels)

plt.savefig(solution_num+'/Durham_all.png', bbox_inches='tight')

# Raleigh
fig = plt.figure()
sns.set()
levels = np.linspace(0,1.00, 201)

ax = fig.add_subplot(1,1,1)
DUPredictors1 = ['intercept', 'Demand_grow_scale']
DVPredictors = [ 'R_Cont']
DUPredictors2 = ['Falls_sup', 'Inflow_scale', 'Trans_cost']
combinedPredictors = pd.concat([DU_factors[DUPredictors1], DVs[DVPredictors], DU_factors[DUPredictors2]], axis=1)
result = fitAllLogit(objs, Raleigh_all, combinedPredictors)
plotCombinedFactorMaps(ax, result, 'Raleigh', 'Demand Growth Scaling Factor', 'Falls Lake Supply Allocation',
	 [0, .5, 1], ['0.5', '1.0', '2.0'], [0, .25, .5, .75, 1], \
	 ['0.8', '0.9', '1.0', '1.1', '1.2'], [],[], DUPredictors2, DU_base, levels)

plt.savefig(solution_num+'/Raleigh_all.png', bbox_inches='tight')


# Cary
fig = plt.figure()
sns.set()
levels = np.linspace(0,1.00, 201)

ax = fig.add_subplot(1,1,1)
DUPredictors1 = ['intercept', 'Demand_grow_scale']
combinedPredictors = pd.concat([DU_factors[DUPredictors1], C_JLA], axis=1)
result = fitAllLogit(objs, Cary_all, combinedPredictors)
plotCombinedFactorMaps(ax, result, 'Cary', 'Demand Growth Scaling Factor', 'Cary JLA (%)',
	 [0, .5, 1], ['0.5', '1.0', '2.0'], [0, .25, .5, .75, 1], \
	 ['30', '32.5', '35', '37.5', '40'], [], [], [], [], levels)

plt.savefig(solution_num+'/Cary_all.png', bbox_inches='tight')