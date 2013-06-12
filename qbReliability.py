######################## import pacakages #######################

import tokenize
import cStringIO
from collections import Counter
import csv
import matplotlib as mpl

import qbGlobals as qbGbl

####################### read the reference attributes ##########

def readclsUIRef(file):

	# to store the reading dataset
	classDict= qbGbl.classDict
	classUIDict= {};

	# opens the csv file
	csvFile = open(file,'rb');

	# reads the csv content
	realFile = csv.reader(csvFile, delimiter=',');

	for row in realFile:
		try:
			classUIDict[classDict[row[0]]] = int(row[1]);
		except e:
			print 'class {0} missing in the dataset'.format(row[0]);

	return classUIDict	


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
	maxCount = []; # to store number of time worker hits maximum points
	minCount = []; # to count number of time worker hits minimum points
	workStats = [];
	# workStats = ["worker_id","no_of_jobs","score","max_score_ratio","min_score_ratio"];

	topicCount = []; # to store the topic ditribution

	# foreach feedback in list
	for uObs in obsDict:

		colClass = []; # to store the class occurences in each observation
		# foreach obseravation with same feedback, different workers
		for obs in obsDict[uObs]:
			# build a collection
			colClass.extend(filData[int(obs)][3]);

		topicCount.extend(colClass);	
		# count the class frequency among different workers for the feedback
		uniClass = dict(Counter(colClass));
		
		# create word scorecard  >>  

		# foreach dictionary entry, 
		for obs in uniClass:
			# normalize for number of workers
			uniClass[obs] = float(uniClass[obs])/float(len(obsDict[uObs]));
		
		#print uniClass
		maxVal = uniClass[max(uniClass, key = uniClass.get)];
		#print maxVal
		minVal = uniClass[min(uniClass, key = uniClass.get)];
		#print minVal
		

		## start scoring for workers by observation	>>
		tempMaxCount = [];
		tempMinCount = [];
		# foreach obseravation with same feedback, different workers
		for obs in obsDict[uObs]:
			tempScore = 0.0; # to accumilate score
			# foreach class in observation
			for cls in filData[int(obs)][3]:
				tempScore += uniClass[int(cls)];
				if uniClass[int(cls)] == maxVal:	
					tempMaxCount.append(filData[int(obs)][1]);
				elif uniClass[int(cls)] == minVal:
					tempMinCount.append(filData[int(obs)][1]);
			workCount.append(filData[int(obs)][1]) # add the worker to the list

			# normalize for the number of classes they have chosen per obs
			l = float(len(filData[int(obs)][3]))
			workDict[filData[int(obs)][1]] += tempScore/l;

		tempMaxCount = set(tempMaxCount);
		maxCount.extend(tempMaxCount);

		tempMinCount = set(tempMinCount);
		minCount.extend(tempMinCount);

	# take headcounts of workers for max scoring and min scoring
	maxCount = dict(Counter(maxCount));
	minCount = dict(Counter(minCount));

	# count the total worker occurences
	workCount = dict(Counter(workCount));

	# normalize for number of jobs per user
	for worker in workDict:
		f = float(workCount[worker]);

		temp = [worker,workCount[worker],workDict[worker]/f]; # normalise score per jobs
	
		# normalise max scores per jobs
		if worker in maxCount:
			temp.append(maxCount[worker]/f); 
		else: 
			temp.append(0.0);

		# normalise min scores per jobs
		if worker in minCount:
			temp.append(minCount[worker]/f);
		else:
			temp.append(0.0);
		
		workStats.append(temp);

	return workStats

## this function write the worker trust scorecard to the csv file in the HDD
def writeScorecard(file,scoreCard):

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# foreach row in the filtered dataset
	for row in scoreCard:
		realFile.writerow(row); # write to file
