########################################################################################################################
# createSampleRanges.py
__author__ = 'dfg42'
# created: 11/12/17
'''
This script will take DVs from a set of compromise solutions found through DU optimization and create ranges for LHS
sampling based on specified epsilon values for each objective.
'''
########################################################################################################################

import numpy as np
from numpy import genfromtxt


def createRanges(solution, dvs, epsilons):
	SolROF = solution[[1, 3, 4, 6, 8, 9, 10]]
	SolCont = solution[11:15]
	SolIns = solution[15:19]

	# create ROF ranges [Lower, Upper]
	# if lower bound drops below zero, set to zero
	RangeROF = np.zeros([7, 2])
	for i in range(0, 7):
		RangeROF[i, 0] = SolROF[i] - epsilons[0]
		if RangeROF[i, 0] <= 0:
			RangeROF[i, 0] = 0.001
		RangeROF[i, 1] = SolROF[i] + epsilons[0]

	# create continuity ranges [Lower, Upper]
	# if lower bound drops below zero, set to zero
	RangeCont = np.zeros([4, 2])
	for i in range(0, 4):
		RangeCont[i, 0] = SolCont[i] - epsilons[1]
		if RangeCont[i, 0] < 0:
			RangeCont[i, 0] = 0
		RangeCont[i, 1] = SolCont[i] + epsilons[1]

	# create insurance ranges [Lower, Upper]
	# if lower bound drops below 1, set to 1
	RangeIns = np.zeros([4, 2])
	for i in range(0, 4):
		RangeIns[i, 0] = SolIns[i] - epsilons[2]
		if RangeIns[i, 0] < 0:
			RangeIns[i, 0] = .1
		RangeIns[i, 1] = SolIns[i] + epsilons[2]
		if RangeIns[i, 1] > 5:
			RangeIns[i, 1] = 5

	# stack all ranges
	RangeOut = np.vstack((RangeROF, RangeCont, RangeIns))

	# print final output
	outfile = open(str(int(solution[0])) + 'ranges.txt', 'w')
	for i in range(0, 15):
		outstring = str(RangeOut[i])
		outstring = outstring[1:-1]
		outfile.write(dvs[i] + ' ' + outstring + ' ' + '\n')

	return

# load input data
Solutions = genfromtxt('../CompSols/Compromise_DVs.csv', delimiter=',',skip_header=1)
DVs = ['D_res', 'O_res', 'R_res', 'C_res', 'D_trans', 'O_trans', 'R_trans', 'D_cont', 'O_cont', 'R_cont', \
 'C_cont', 'D_ins', 'O_ins', 'R_ins', 'C_ins']
Epsilons = np.array([0.03846, 0.04, 2])
num_solutions = 14

for i in range(0, num_solutions):
	createRanges(Solutions[i], DVs, Epsilons)
