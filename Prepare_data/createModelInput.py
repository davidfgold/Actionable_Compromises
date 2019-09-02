########################################################################################################################
# createModelInput.py
__author__ = 'dfg42'
# created: 11/15/17
# updated: 1/19/18
'''
This script will create input for the water resources model by taking perturbed sample values and combining them with
unchanged DVs from the original solutions
'''
########################################################################################################################

import numpy as np
from numpy import genfromtxt
from numpy import savetxt


def combine(originalFileName, solution, solutionRow, lhsSampleFileName):
	original = genfromtxt(originalFileName, delimiter=',', skip_header=1)
	LHS = genfromtxt(lhsSampleFileName, delimiter=',')
	outFile = np.zeros([1008, 32])
	perturbedIndex = range(0, 1008)

	#  add unchanged values to file
	outFile[:, 0] = perturbedIndex
	unchangedIndex = [2, 5, 7, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
	for i in range(0, 16):
		outFile[:, unchangedIndex[i]] = original[solutionRow, unchangedIndex[i]]

	#  add changed values to file
	changedIndex = [1, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
	for i in range(0, 15):
		columnValue = np.ones([1008, 1])*LHS[:, i]
		outFile[:, changedIndex[i]] = columnValue[:][0]

	# print perturbations to one file for WCU reevaluation
	savetxt('Solution_' + str(solution) + "/all_perturbations" + str(solution) + ".csv", outFile, delimiter=",", fmt='%f')

	# print
	for i in range(0, 1008):
		miniOut = outFile[i, :]
		savetxt('Solution_' + str(solution) + "/sample_" + str(i) + ".csv", miniOut[None], delimiter=',', fmt='%f')

	return

compSols = [598, 629, 1077, 1079, 1427, 1494, 1599, 1709, 1713, 1864, 1939, 2074, 2191, 2841]
originalFile = '../CompSols/Compromise_DVs.csv'

j = 0
for i in compSols:
	LHSSampleFile = 'LHSSamples/Solution' + str(i) + '_Samples.csv'
	combine(originalFile, i, j, LHSSampleFile)
	j+=1
