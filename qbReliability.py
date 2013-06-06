####################### import pacakages #####################

import tokenize
import cStringIO
from collections import Counter
import csv

import qbGlobals as qbGbl

######################## Do realiability Analysis ###############

## this function sets up a dicitonary feedbacks with its observation refs
def genObsDict(filData):
	obsDict = {};
	for row in filData:
		if row[2] in obsDict:
			obsDict[row[2]].extend([row[0]]);
		else:
			obsDict[row[2]] = [row[0]];

	return obsDict 

## this funciton generates the dictionary of workers for scoring
def genWorkDict(filData):
	workDict = {};
	for row in filData:
		# print '{0} || {1}'.format(row[0],row[2])
		if row[1] not in workDict:
			workDict[row[1]] = 0;

	return workDict 

## this function does the scoring and returns the dictionary with the scores
def scoreWorkers(obsDict,workDict,filData):

	# to store the number of worker occurences in the dataset for normalization
	workCount = [];

	# foreach feedback in list
	for uObs in obsDict:

		colClass = []; # to store the class occurences in each observation
		# foreach obseravation with same feedback, different workers
		for obs in obsDict[uObs]:
			# build a collection
			colClass.extend(filData[int(obs)-1][3]);
		# count the class frequency among different workers for the feedback
		uniClass = dict(Counter(colClass));

		
		# create word scorecard  >>  

		# foreach dictionary entry, 
		for obs in uniClass:
			# normalize for number of workers
			uniClass[obs] = float(uniClass[obs])/float(len(obsDict[uObs]));
		
		## start scoring for workers by observation	>>

		# foreach obseravation with same feedback, different workers
		for obs in obsDict[uObs]:
			tempScore = 0.0; # to accumilate score
			for cls in filData[int(obs)-1][3]:
				tempScore += uniClass[int(cls)];
			
			workCount.append(filData[int(obs)-1][1]) # add the items to the list

			# normalize for the number of classes they have chosen
			l = float(len(filData[int(obs)-1][3]))
			workDict[filData[int(obs)-1][1]] += tempScore/l;
	
	# count the word occurences
	workCount = dict(Counter(workCount));

	# normalize for number of jobs per user
	for worker in workDict:
		workDict[worker]/=float(workCount[worker]);

	return workDict

## this function write the worker trust scorecard to the csv file in the HDD
def writeScorecard(file,scoreCard):

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# foreach row in the filtered dataset
	for row in scoreCard:
		realFile.writerow( [row, scoreCard[row]]); # write to file
