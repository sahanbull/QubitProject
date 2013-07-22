######################## import pacakages #######################

import tokenize
import cStringIO
from collections import Counter
import csv
import numpy
import scipy.stats
import matplotlib as mpl
import random
import pandas as pd
import time

import qbGlobals as qbGbl
import qbPreprocess as qbPre

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
	perfectCount = []; # to count  the number of times worker hits 1.0
	workStats = []; # to store the user statistics at the end :)
	workTopics = {}; # to store the topic distribution per worker

	topicCount = []; # to store the topic ditribution

	# foreach feedback in list
	for uObs in obsDict:

		colClass = []; # to store the class occurences in each observation

		# foreach obseravation with same feedback, different workers
		for obs in obsDict[uObs]:
			# build a collection
			colClass.extend(filData[int(obs)][3]);

			# update userwise topic count
			if filData[int(obs)][1] not in workTopics:
				workTopics[filData[int(obs)][1]] = colClass;
			else:
				workTopics[filData[int(obs)][1]].extend(colClass);

		# add the topics to the topic count list
		topicCount.extend(colClass);	

		# count the class frequency among different workers for the feedback
		uniClass = dict(Counter(colClass));
		
		# create word scorecard  >>  

		# foreach dictionary entry, 
		for obs in uniClass:
			# normalize for number of workers
			uniClass[obs] = float(uniClass[obs])/float(len(obsDict[uObs]));
		
		# sum up concordence score and normalise over number of obeservations
		# observation concordence score	
		obsScore = sum(uniClass.values())/float(len(uniClass));

		# print obsScore

		#print uniClass
		maxVal = uniClass[max(uniClass, key = uniClass.get)];
		#print maxVal
		minVal = uniClass[min(uniClass, key = uniClass.get)];
		#print minVal

		## start scoring for workers by observation	>>
		tempMaxCount = [];
		tempMinCount = [];
		tempPerfectCount = [];

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
			if obsScore == 1.0: # if perfect 1.0, 
				tempPerfectCount.append(filData[int(obs)][1]);
				qbGbl.fullConFeedbacks.append(filData[int(obs)][2])
				# print 'poing'
			# normalize for the number of classes they have chosen per obs
			l = float(len(filData[int(obs)][3]))
			workDict[filData[int(obs)][1]] += tempScore/l;

		tempMaxCount = set(tempMaxCount);
		maxCount.extend(tempMaxCount);

		tempMinCount = set(tempMinCount);
		minCount.extend(tempMinCount);

		#print tempPerfectCount
		tempPerfectCount = set(tempPerfectCount);
		#print tempPerfectCount
		perfectCount.extend(tempPerfectCount);

	# take headcounts of workers for max scoring and min scoring
	maxCount = dict(Counter(maxCount));
	minCount = dict(Counter(minCount));

	# count the total worker occurences
	workCount = dict(Counter(workCount));

	perfectCount = dict(Counter(perfectCount));
	
	# print perfectCount
	# print workTopics

	# foreach worker,
	for worker in workDict:
		## COMPUTE THE WORKER WISE LIST COMPUTATIONS
		# topic distribution per user
		wrkTpcCount = Counter(workTopics[worker]);
		# print wrkTpcCount;
		tempTpc = {};
		# change labels to the UI ref order
		for topic in wrkTpcCount:
			tempTpc[qbGbl.classUIRef[topic]] = wrkTpcCount[topic];

		workTopics[worker] = list(Counter(tempTpc).elements());


		## COMPUTE THE USER COLLECTIVE STATISTICS
		# normalize for number of jobs per user
		f = float(workCount[worker]);

		if worker in perfectCount:
			perfectness = float(perfectCount[worker]);
			perfectness /= float(maxCount[worker]);
		else: 
			perfectness = 0.0;	

		temp = [worker,workCount[worker],workDict[worker]/f,perfectness]; # normalise score per jobs
	
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
		
		temp.append(scipy.stats.tmean(workTopics[worker])); # mean of class selection
		temp.append(scipy.stats.mode(workTopics[worker])[0][0]); # mode of class selection
		temp.append(scipy.stats.mode(workTopics[worker])[1][0]/len(workTopics[worker])); # mode freaquency
		temp.append(scipy.stats.cmedian(workTopics[worker])); # median of class selection

		# update worker statistics
		workStats.append(temp);

	# count the occurences
	topicCount = Counter(topicCount);

	# change labels to the UI ref order
	for topic in topicCount:
		qbGbl.topicHist[qbGbl.classUIRef[topic]] = topicCount[topic];

	qbGbl.topicHist = list(Counter(qbGbl.topicHist).elements())
	# qbGbl.topicHist COMPLETE
	# print qbGbl.topicHist COMPLETE

	qbGbl.workTopics = workTopics;
	#print qbGbl.workTopics COMPLETE

	# print len(obsDict)

	qbGbl.fullConFeedbacks = set(qbGbl.fullConFeedbacks)

	return workStats

## this function write the worker trust scorecard to the csv file in the HDD
def writeScorecard(file,scoreCard):

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# foreach row in the filtered dataset
	for row in scoreCard:
		if row[1]<100:
			continue

		realFile.writerow(row); # write to file

## this function does the difficulty scoring for observations		
def scoreObsComplex(obsDict,filData):

	obsScore = {};
	# foreach feedback in list
	for uObs in obsDict:

		colClass = []; # to store the class occurences in each observation
		# foreach obseravation with same feedback, different workers
		for obs in obsDict[uObs]:
			# build a collection
			colClass.extend(filData[int(obs)][3]);

		uniClass = dict(Counter(colClass));
		
		# foreach dictionary entry, 
		for obs in uniClass:
			# normalize for number of workers
			uniClass[obs] = float(uniClass[obs])/float(len(obsDict[uObs]));
		
		# sum up concordence score and normalise over number of obeservation	
		score = sum(uniClass.values())/float(len(uniClass));

		obsScore[uObs] = score;
		
	return obsScore

## this function generates a random sample of observations for golden set verifications
def goldenSet(number):
	# load the filtered dataset
	filData = qbPre.readSimpleFile('data/write/fil_comb_results.csv');

	ranSample = random.sample(filData, number);

	qbPre.writeFilCSV('data/relAnalytics/goldenSet.csv',ranSample);

## pick row dataset to find the old ones
def pickRowDataset():
	newData = qbPre.readDataFrame('{0}/Batch_1123120_batch_results.csv'.format(qbGbl.oriFileName),None,0);
	data = pd.DataFrame(newData['Input.pv_id'], columns= ['pv_id'])
	
	data['global_user_id'] = newData['Input.global_user_id'];
	data['time'] = newData['Input.time'];
	data['declaration'] = newData['Input.declaration'];

	return data

## this function generates a sample mixing old and new data in given proportions
def generateSample(fulConSet,m,newFileName,n):

	# generate old data sample ================================

	oldSample = pd.DataFrame(columns=('pv_id', 'global_user_id', 'time', 'declaration'));

	# pick full information
	oldData = pickRowDataset()

	# generate and write the fully concorded for later reference to HDD
	tempFulConSet = pd.DataFrame(list(fulConSet),columns = ['declaration'])

	tempFulConSet.to_csv('data/relAnalytics/fulConSet.csv',index = False);

	# find full info of the filly concorded occurences
	for feedback in fulConSet:
		p = oldData[oldData['declaration'] == feedback];
		oldSample = oldSample.append(p[0:1],ignore_index=True)

	rows = list(oldSample.index)
	# print oldSample
	# until the population > sample size
	while len(oldSample) < m:
		# double the population by duplicating 
	 	oldSample = oldSample.append(oldSample,ignore_index=True);
	 	# shuffle the observations
	 	rows = list(oldSample.index);
		random.shuffle(rows);
		oldSample = oldSample.ix[rows]

	print oldSample.declaration
	# pick a random sample of size m
	rows = random.sample(oldSample.index,m)
	
	# random sample generated for old set
	sample = oldSample.ix[rows]

	# generate new data sample =================================
	# load the filtered dataset
	newData = qbPre.readDataFrame(newFileName,None,0);
	# pick a random sample of size
	newRows = random.sample(newData.index,n);

	newSample = newData.ix[newRows];

	# aggregate the old and new samples to gether
	sample = sample.append(newSample,ignore_index=True);
	print sample.declaration
	rows = list(sample.index);
	# shuffle them
	random.shuffle(rows);
	sample = sample.ix[rows];
	print sample.declaration
	# generate csv file :D
	sample.to_csv('data/write/newFeedbackSample2.csv',index = False);


def analyseWorkers():
	filData = qbPre.readDataFrame(qbGbl.filFileName,None,0);

	workers = filData.WorkerId.drop_duplicates();

	filename = '{0}/PerfectDataset.csv'.format(qbGbl.oriFileName)

	old = qbPre.readDataFrame(filename,None,0)

	perfectDecs = old.declaration.drop_duplicates()

	dataSet = pd.DataFrame()

	for row in perfectDecs:
		if not filData[filData['Input.declaration']==row].empty:
			if dataSet.empty:
				dataSet = filData[filData['Input.declaration']==row]
			else:
				dataSet = dataSet.append(filData[filData['Input.declaration']==row])


	dataSet.SubmitTime = pd.to_datetime(dataSet.SubmitTime)

	# dataSet = pd.DataFrame(dataSet.values,
	# 	columns=['SubmitTime','WorkerId','Input.declaration','Answer.Q1'])

	# print dataSet

	dataSet = dataSet.sort(columns=['SubmitTime'])
	# firstDate = list(dataSet.SubmitTime)[0]

	records = [];
	# print dataSet	
	workers = dataSet.WorkerId.drop_duplicates();
	


	for worker in workers:
		tempStats = {'score':0.0,'freq':0}
		tempRecords = dataSet[dataSet.WorkerId==worker]
		for row in tempRecords.itertuples():
			newRow = list(row)
			# print newRow[-2]
		 	# print old[old['declaration'] == newRow[-2]]
			tempOld = qbPre.convClasses(list(old[old['declaration'] == newRow[-2]].answer)[0],'|')
			# print tempOld
			tempNew = qbPre.convClasses(newRow[-1],'|')
			# print tempNew
			tempScore = 0.0;
			for topic in tempNew:
				if topic in tempOld:
					tempScore += 1.0;
			tempScore /= float(len(tempNew))

		 	tempStats['freq']+=1; # frequency ++
			tempStats['score']+=tempScore;
			
			aggrScore = tempStats['score']/tempStats['freq']
			tm = row[1].time()
			tm = float(tm.hour) + float(tm.minute) / 60
			# print tm

			compl = float(tempStats['freq'])/float(len(tempRecords))
			# del newRow[0]
			newRow.extend([tm,tempScore,aggrScore,compl])

			records.append(newRow)

	records = numpy.array(records);

	dataSet = pd.DataFrame(records[:,1:],
		columns = ['SubmitTime','WorkerId','Input.declaration','Answer.Q1','Time','TempScore','AggrScore','Completion'],
		index=records[:,0])

	return dataSet



	# newDataSet = pd.DataFrame(records[1:],columns=[])
	
		# print tempStats



	# counter = 0
	# for worker in workers:
	# 	if len(filData[filData.WorkerId==worker])<100:
	# 		counter += len(filData[filData.WorkerId==worker])

	# print counter
	# print filData

def pickBadEntries(frame,val=0.75):
	workStat = frame[frame.Completion==1.0]

	goodList = workStat[workStat.AggrScore > val][['WorkerId','AggrScore']]

	for worker in goodList.values:
		qbGbl.workDict[worker[0]] = worker[1]

	badList = workStat[workStat.AggrScore <= val].WorkerId
	badEntries = pd.DataFrame()
	for worker in badList:
		tempBad = frame[frame.WorkerId==worker]
		badEntries = badEntries.append(tempBad)

	# remove the duplicates depending on the majority vote

	temp = pickBadObs(frame)
	
	badEntries = badEntries.append(temp)
		
	return badEntries
	# print len(uniqueSet)
	# return badEntries










def pickBadObs(frame):

	fulBads = pd.DataFrame()
	# pick unique declarations
	uniqueSet = frame['Input.declaration'].drop_duplicates()

	# foreach declaration...
	for dec in uniqueSet:
		# all the openions for that openion
		temp = frame[frame['Input.declaration']==dec]

		# pick all the classes with frequency
		classes = list(temp['Answer.Q1'])
		norm = float(len(classes)) # total number of openions

		# count the class frequency among worker responses for the feedback
		classes = dict(Counter(classes));

		# foreach dictionary entry, 
		for obs in classes:
			# normalize for number of openions (makes it a fraction)
			classes[obs] = float(classes[obs])/norm;

		# foreach observation,
		tempScore = []
		for obs in temp.values:
			if obs[1] not in qbGbl.workDict:
				qbGbl.workDict[obs[1]] = 0.0;
			score = qbGbl.workDict[obs[1]] * classes[obs[3]]
			# print score
			tempScore.append(score)

		tempTemp = pd.Series(tempScore,index=temp.index)
		
		# remove the top scored observation as we need to leave it
		temp = temp.drop(tempTemp.idxmax())

		fulBads = fulBads.append(temp)

	return fulBads



