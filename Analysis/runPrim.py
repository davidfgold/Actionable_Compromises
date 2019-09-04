import prim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from os import rename
import glob as gb

# set solution number
solution_num = '1713'
utility = 'Cary'
metric = 'C_all'

# load objectives and establish regional criteria
perturbed = pd.read_csv('../Data/satisficing_' + str(solution_num) + '_prim.csv')

DVs = pd.read_csv('../Data/all_perturbations' + solution_num +'.csv')

if utility == "Durham":
	util_DVs = DVs[['D_RT', 'D_TT', 'D_Cont', 'D_Ins', 'D_JLA']]
elif utility == "Raleigh":
	util_DVs = DVs[['R_RT', 'R_TT', 'R_Cont', 'R_Ins', 'R_JLA']]
else:
	util_DVs = DVs[['C_RT', 'C_Cont', 'C_Ins', 'C_JLA']]

p = prim.Prim(util_DVs, perturbed[metric], threshold=819, threshold_type=">")
box = p.find_box()
print box

box.show_tradeoff()
plt.show()
