
####################### import pacakages #####################

import numpy;
import pandas as pd;
import pylab as P
import scipy
import re
import sklearn.cross_validation as cv
import sklearn

import random

import qbPreprocess as qbPre
import qbReliability as qbRel
import qbGlobals as qbGbl
import qbPrepare as qbPrepare

import test

########################## Main functions ########################

def filterData():
	filData = []; # to store the filtered dataset
	count = 0; # to keep the counter

	# read original file and load the relevant data
	# list all the csv log files with records
	paths = qbPre.listFiles(qbGbl.oriFileName);

	# foreach csv file in the paths
	for path in paths:
		filterSet = qbPre.filterFile(path,count); # filter data 
		filData.extend(filterSet[0]); # add to the filtered dataset in RAM
		count = filterSet[1]; # update count

	# write filtered data to a different file in the HDD 
	qbPre.writeFilCSV(qbGbl.filFileName,filData);

def doReliabilityScoring():
	# load the filtered dataset
	filData = qbPre.importFilCSV(qbGbl.filFileName,True);

	qbGbl.classUIRef = qbRel.readclsUIRef(qbGbl.classUIRefFileName);

	## generate observation list
	obsDict = qbRel.genObsDict(filData);
	
	## generate worker list 
	workDict = qbRel.genWorkDict(filData); 

	scoreCard = qbRel.scoreWorkers(obsDict,workDict,filData);

	return scoreCard

def generateNewData():
	# run to generate the global full concordence set
	notNeeded = doReliabilityScoring();
	qbRel.generateSample(qbGbl.fullConFeedbacks,3143,'{0}{1}'.format(qbGbl.oriFileName,qbGbl.newSampFileName),27000)


def doObsComplexityScoring():
	# load the filtered dataset
	filData = qbPre.importFilCSV(qbGbl.filFileName,True);

	## generate observation list
	obsDict = qbRel.genObsDict(filData);
	
	obsComplexity = qbRel.scoreObsComplex(obsDict,filData);

	return obsComplexity;

## this funciton tokenizes the words
def prepareData(type):
	# load the filtered dataset
	filData = qbPre.importFilCSV(qbGbl.filFileName,False);
	
	filData = qbPre.prepareData(filData,type);
	filData = pd.DataFrame(filData,columns=['index','declaration','answer'])
	del filData['index']
	
	noneRecs = filData[filData.declaration == ''].index
	filData = filData.drop(noneRecs)

	# generate csv file :D
	filData.to_csv('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),index = False);
	

	# write filtered data to a different file in the HDD 
	# qbPre.writeFilCSV('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),filData);

## this function reads preProcessed Data and vectorise it
def preProcessData(type):
	# load the cleaned dataset
	# filData = qbPre.readFile('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),type);

	filData = qbPre.readDataFrame('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),None,0);
	filData = filData.drop_duplicates(cols=['declaration']) # drop all the duplicates
	sample = filData[filData['answer'].str.contains('None')] # pick all the observaions as None of above
	filData = filData.drop(sample.index) # drop them as well

	rows = list(filData.index);
	random.shuffle(rows);
	# print rows
	filData = filData.ix[rows]

	# print oldSample.declaration
	# filData = qbPre.readFile('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),type);
	# print filData

	# m = int(round(len(filData)*1.0))
	# print m
	# rows = random.sample(filData.index,m)
	
	# # random sample generated for old set
	# filData = filData.ix[rows]
	# print 'Number of observations: {0}'.format(len(filData))

	X = qbPrepare.generateX(filData);

	Y = qbPrepare.generateY(filData);

	return [filData,X,Y] 

## this function takes X and Y and does everything necessary to classify them
def classifyData(X,Y,C=[1.0]):
	XTrain, XTest, YTrain, YTest = qbPrepare.segmentData(X,Y,0.4);

	kfolds = qbPrepare.kFoldGenerator(XTrain.shape[0],5)

	valScore = [];

	for c in C:

		score = [];

		for train,test in kfolds:
			xTrainCV = XTrain[train]
			yTrainCV = YTrain[train]
			
			xTestCV = XTrain[test]
			yTestCV = YTrain[test]

			# print xTrainCV.shape,yTrainCV.shape,xTestCV.shape,yTestCV.shape

			score.append(qbPrepare.classify(XTrain,XTest,YTrain,YTest,c,cv=True))

		print 'cross validation accuracy with C= {0}: {1}'.format(c,numpy.mean(score))	
	
		valScore.append(numpy.mean(score))
	
	print '\n'

	finalC = C[numpy.argmax(valScore)]

	qbPrepare.classify(XTrain,XTest,YTrain,YTest,finalC);

def analyse(filename):

	# filData = qbPre.readDataFrame(filename,None,0);
	# filData = filData[['WorkerId','Input.declaration','Answer.Q1']]

	# new = filData

	# filename = '{0}'.format(qbGbl.filFileName) 
	# # filData = pd.DataFrame(columns=['index','worker','declaration','answer'])
	# filData = qbPre.readDataFrame(filename,None,None);
	# filData.columns = ['index','worker','declaration','answer'];

	# del filData['index']

	# old = filData

	# oldDecs = []
	
	# for row in new['Input.declaration']:
	# 	if (old[old['declaration'] == row].empty):
	# 		continue;
	# 	else:
	# 		oldDecs.append(numpy.array(old[old['declaration'] == row])[1])

	# oldDecs = pd.DataFrame(oldDecs,columns=['worker','declaration','answer'])
	
	# oldDecs.to_csv('{0}/PerfectDataset.csv'.format(qbGbl.oriFileName),index = False);
	
	## ===============================================================================
	filData = qbPre.readDataFrame(filename,None,0);
	filData = filData[['WorkerId','Input.declaration','Answer.Q1']]

	new = filData

	filename = '{0}/PerfectDataset.csv'.format(qbGbl.oriFileName)

	old = qbPre.readDataFrame(filename,None,0)

	# print new['Input.declaration'].nunique()
	# print len(old['declaration'].unique())
	filData = pd.Series(old['declaration'].unique())
	# print len(filData)
	# print '================='
	accuracy = []
	count=0;
	for row in filData:
		# print row
		if not (new[new['Input.declaration'] == row].empty):
			count += len(new[new['Input.declaration'] == row])
			tempOld = qbPre.convClasses(list(old[old['declaration'] == row]['answer'])[0],'|')
			# print tempOld
			tempNew = qbPre.convClasses(list(new[new['Input.declaration'] == row]['Answer.Q1'])[0],'|')
			# print tempNew
			tempScore = 0.0;
			for topic in tempNew:
				if topic in tempOld:
					tempScore += 1.0;

			tempScore /= float(len(tempNew))
			accuracy.append(tempScore)
	
	print scipy.stats.tmean(accuracy) 

	P.figure();

	n, bins, patches = P.hist(accuracy,len(set(accuracy)), histtype='bar',cumulative=False)

	P.title("Score distribution")
	P.xlabel("score")
	P.ylabel("Frequency")
	P.show()


## this function takes an existing labelled dataset and a generated dataset and removed the labelled observations
def cleanExistingData(filename1,filename2):

	labelled = qbPre.readDataFrame(filename1,None,0)
	labelled = labelled['Input.declaration']
	print labelled
	
	unlabelled = qbPre.readDataFrame(filename2,None,0);

	unlabelled = unlabelled.drop_duplicates(cols=['declaration'])

	# print unlabelled[unlabelled['declaration']==labelled]
	for row in labelled:
		unlabelled = unlabelled.drop(unlabelled[unlabelled['declaration']==row].index)
		# if not unlabelled[unlabelled['declaration']==row].empty:
		# 	unlabelled.drop
		# if not (unlabelled[unlabelled['Input.declaration'] == row].empty):
	
	print unlabelled

	# unlabelled.to_csv('{0}/newData.csv'.format(qbGbl.oriFileName),index = False);


	# # test = pd.DataFrame.to_records(labelled,index=False)
	# count = 0
	# # print test.pv_id
	# for row in labelled.values:
	# 	print '=================================='
	# 	count += 1
	# 	if len(unlabelled[unlabelled['pv_id']==row[0]]) > 1:
	# 		# pass
	# 		print unlabelled[unlabelled['pv_id']==row[0]]
	# 	# print (len(unlabelled[unlabelled['pv_id'] == row[0] and unlabelled['global_user_id'] == row[1]])) #>1:
	# 		# print 'IOOOO'
		
	# print count
	# # write = 'data/write/cleanedDataset.csv';

########################## Main Script ########################

## filter the data from the main dataset and write the only relevant files to new file
# filterData()	

## carry out reliabilty scoring and then write results to a CSV file
# scoreCard = doReliabilityScoring();
# qbRel.writeScorecard(qbGbl.scoreFileName,scoreCard);

## carry out reliabilty scoring and then write results to a CSV file
# obsComplexity = doObsComplexityScoring();
# qbRel.writeScorecard(qbGbl.scoreFileName,scoreCard);

# generateNewData()
types = ['100','110','111']
# start tokenizing the stuff
for t in types:
	type = t;
	# prepareData(type);

	# qbRel.goldenSet(100);

	# ## carry out word scoring and related statistics
	# initData, dataX, dataY = preProcessData(type);
	print '\n'
	print 'Classitying data using text preProcessing specification {0}'.format(type)
	print '\n'
	filData,X,Y = preProcessData(type);

	# print Y
	# scores = cv.cross_val_score(qbPrepare.classifier,X,Y,cv=10,scoring='precision')

	# test.testingSVM()
	classifyData(X,Y,C=[0.1,0.5,0.7,1.0,1.2,2.0])
	print '\n'

# analyse('{0}/Batch_1189077_batch_results.csv'.format(qbGbl.oriFileName))

# cleanExistingData('{0}/Batch_1189077_batch_results.csv'.format(qbGbl.oriFileName),'{0}/seededfeedback.clean.txt'.format(qbGbl.oriFileName))