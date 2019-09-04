######################################################################
'''
Name: figure_8.py
By: D. Gold
Created: 6/4/18
 
This script will plot guages of logistic regression results.
Gauges are post processed and combined in adobe illustrator
to make final figures.
'''
###################################################################### 

import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
import numpy as np
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
from logisticRegressionTools import set_thresholds
from logisticRegressionTools import fitLogit
from createDVLabels import createDVLabels
import math
#from PIL import Image
from mpl_toolkits.axes_grid1 import make_axes_locatable


def dial(regression_output,ax, DVTitle, arrow_index):
    # Create bins to plot (equally sized)
    size_of_groups=np.ones(len(regression_output)*2)
     
    # Create a pieplot, half white, half colored by logistic regression results
    white_half = np.ones(len(regression_output))*.5
    color_half = (.81-regression_output)/.81
    color_pallet = np.concatenate([color_half, white_half])

    cs=cm.Purples(color_pallet)
    pie_wedge_collection = plt.pie(size_of_groups, colors=cs)

    i=0
    for pie_wedge in pie_wedge_collection[0]:
        pie_wedge.set_edgecolor(cm.Purples(color_pallet[i]))
        i=i+1
    #ax.set_title(DVTitle) 
    # add a circle at the center
    my_circle=plt.Circle( (0,0), 0.3, color='white')
    #p=plt.gcf()
    ax.add_artist(my_circle)

    # create the arrow, pointing at specified index
    arrow_angle = (arrow_index/float(len(regression_output)))*3.14159
    arrow_x = 0.2*math.cos(arrow_angle)
    arrow_y = 0.2*math.sin(arrow_angle)
    ax.arrow(0,0,-arrow_x,arrow_y, width=.02, head_width=.05, \
        head_length=.1, fc='k', ec='k')

# set solution number
solution_num = '1713'
fig_name = 'Ddonut1939.svg'

# load DVs, Normalize and add intercepts
DV_names = ['D_RT', 'R_RT', 'C_RT', 'D_TT', 'O_TT', 'R_TT', 'D_Cont', 'O_Cont', \
    'R_Cont', 'C_Cont', 'D_Ins', 'O_Ins', 'R_Ins', 'C_Ins', 'D_JLA', 'R_JLA', 'O_JLA', 'C_JLA']
#DVs = pd.read_csv('../Regression_input/DVs/DV_' + solution_num +'_all.csv', names=DV_names)
DVs = pd.read_csv('../Regression_input/DVs/DV_' + solution_num +'_all.csv', names=DV_names)

OriginalDVs = pd.read_csv('../Parameter_ranges/' + solution_num + 'OriginalDVs.csv', names=[\
    'D_RT', 'R_RT', 'C_RT', 'D_TT', 'O_TT', 'R_TT', 'D_Cont', 'O_Cont', \
    'R_Cont', 'C_Cont', 'D_Ins', 'O_Ins', 'R_Ins', 'C_Ins', 'D_JLA', 'R_JLA', 'O_JLA', 'C_JLA'])

# normalize DV values
DVparamBounds =np.genfromtxt('../Parameter_ranges/' + solution_num + 'DV_Ranges.csv', delimiter=',')
for i, col in enumerate(DVs.columns):
        DVs[col] = (DVs[col] - DVparamBounds[i,0])/(DVparamBounds[i,1] - DVparamBounds[i,0])
        OriginalDVs[col] = (OriginalDVs[col] - DVparamBounds[i,0])/(DVparamBounds[i,1] - DVparamBounds[i,0])

# add intercept column
DVs['intercept'] = np.ones(np.shape(DVs)[0])

# load objectives and establish regional criteria
obj_names = ['D_Rel', 'D_RF', 'D_AC', 'D_WCC', 'O_Rel', 'O_RF', 'O_AC', 'O_WCC', 'R_Rel', 'R_RF', 'R_AC', \
    'R_WCC', 'C_Rel', 'C_RF', 'C_AC', 'C_WCC']

#objs = pd.read_csv('../Regression_input/obj/obj_' + solution_num + '_all.csv', names=obj_names)
objs = pd.read_csv('../Regression_input/obj/obj_' + solution_num + '_all.csv', names=obj_names)

# set robustness criteria
All_robustness, Durham_all, Durham_Rel, Durham_RF, Durham_WCC, Raleigh_all, Raleigh_Rel, \
    Raleigh_RF, Raleigh_WCC, Cary_all, Cary_Rel, Cary_RF, Cary_WCC = set_thresholds(objs)


# set up plot labels for DVs
DurPlotLabelsTop, DurPlotLabelsBottom, RalPlotLabelsTop, RalPlotLabelsBottom, \
 CarPlotLabelsTop, CarPlotLabelsBottom = createDVLabels(DVparamBounds)

# list of decision variables for each utility to plot
utilDVs = [['D_RT', 'D_TT', 'D_Cont', 'D_Ins', 'D_JLA'], \
['R_RT', 'R_TT', 'R_Cont', 'R_Ins', 'R_JLA'], \
 ['C_RT', 'C_Cont', 'C_Ins', 'C_JLA']]


# ranges for prediction, reverse is for DVs where lower means more use (ie ROF trigger)
DVrange = np.linspace(0.0, 1.0, 1001)
DVrange_reverse = np.linspace(1.0, 0, 1001)

DRCcriteria = [Durham_Rel, Raleigh_Rel, Cary_Rel]
plotTitles = ['Durham \n', 'Raleigh \n', 'Cary \n']
DVTitles = ['Restriction \nTrigger', 'Transfer \nTrigger', 'Contingency \nFund', \
'Insurance \nTrigger', 'Jordan Lake \nAllocation']

fig = plt.figure(figsize=(14,3))

# fit the logistic regression with all DVs
predictors = list(utilDVs[2])
predictors.append('intercept')
result = fitLogit(objs, DRCcriteria[2], DVs, predictors)
print result.summary()


predicted_probs = np.zeros([1001,len(utilDVs[1])])
originalUtilDVs = OriginalDVs[utilDVs[1]]

DV_arrow = [[500, 50, 500, 500, 500], [500, 500, 500, 500, 500], [500, 400, 250, 500]]

for j in range(0, len(utilDVs[0])):
    #print utilDVs[i][0]
    grid = np.ones([1001,len(predictors)])
    for k in range(0, len(utilDVs[0])):
        grid[:,k] = grid[:,k]*OriginalDVs[utilDVs[0][k]].values
    grid[:,j] = DVrange
    z = result.predict(grid)
    predicted_probs[:,j] = z
    ax = fig.add_subplot(1,len(utilDVs[2]),j+1)
    dial(predicted_probs[:,j], ax, DVTitles[j], DV_arrow[0][j])

plt.show()
plt.savefig(fig_name, bbox_inches='tight') 
