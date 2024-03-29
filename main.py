
####################### import pacakages #####################

import numpy;
import scipy
import re
import gensim
import sklearn.cross_validation as cv
import pandas as pd
import pylab as P
import sklearn

import matplotlib.pyplot as plt

import random

import qbPreprocess as qbPre
import qbReliability as qbRel
import qbGlobals as qbGbl
import qbPrepare as qbPrepare

import test

########################## Main functions ########################

def filterData2(cols=['HITId','HITTypeId','Title','Description','Keywords','Reward',
	'CreationTime','MaxAssignments','RequesterAnnotation','AssignmentDurationInSeconds',
	'AutoApprovalDelayInSeconds','Expiration','NumberOfSimilarHITs','LifetimeInSeconds',
	'AssignmentId','WorkerId','AssignmentStatus','AcceptTime','SubmitTime','AutoApprovalTime',
	'ApprovalTime','RejectionTime','RequesterFeedback','WorkTimeInSeconds','LifetimeApprovalRate',
	'Last30DaysApprovalRate','Last7DaysApprovalRate','Input.pv_id','Input.global_user_id',
	'Input.time','Input.declaration','Answer.Q1','Approve','Reject']):

	paths = qbPre.listFiles(qbGbl.oriFileName)
	filData = qbPre.readFiles(paths)

	filData = filData[cols];

	filData.to_csv(qbGbl.filFileName,index = False,encoding='utf-8');

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


def analyseWorkers():
	dataSet = qbRel.analyseWorkers();
	workers = list(dataSet['WorkerId'].drop_duplicates())
	
	# print dataSet
	# ax = plt.subplot(111)

	## time wise aggregate for workers## time wise aggregate for workers

	# sample = dataSet[['Time','WorkerId','AggrScore']]
	# # foreach worker..
	# for worker in workers:
	# 	tempRecords = sample[sample.WorkerId==worker]
	# 	plt.scatter(tempRecords.Time,tempRecords.AggrScore, hold='on')

	# plt.title("Aggregated Score distribution by time of Day")
	# plt.xlabel("Time of day in 24-hour")
	# plt.xlim((-0.1, 24.1))
	# plt.ylabel("Aggregated Score")
	# plt.ylim((-0.1, 1.1))
	# plt.show()

	## timewise real Score for worker

	# sample = dataSet[['Time','WorkerId','TempScore']]

	# for worker in workers:
	# 	tempRecords = sample[sample.WorkerId==worker]
	# 	plt.scatter(tempRecords.Time,tempRecords.TempScore, hold='on')


	# plt.title("Score distribution by time of Day")
	# plt.xlabel("Time of day in 24-hour")
	# plt.ylabel("Score")
	# plt.show()
				
	# ## date wise agrr

	# sample = dataSet[['Completion','WorkerId','AggrScore']]

	# for worker in workers:
	# 	tempRecords = sample[sample.WorkerId==worker]
	# 	plt.plot(tempRecords.Completion,tempRecords.AggrScore, hold='on')

	
	# plt.title("Score distribution by Completion")
	# plt.xlabel('percentage completed')
	# plt.ylabel("Aggregated Score")
	# plt.show()

	
def getReliableData(cols=['HITId','HITTypeId','Title','Description','Keywords','Reward',
	'CreationTime','MaxAssignments','RequesterAnnotation','AssignmentDurationInSeconds',
	'AutoApprovalDelayInSeconds','Expiration','NumberOfSimilarHITs','LifetimeInSeconds',
	'AssignmentId','WorkerId','AssignmentStatus','AcceptTime','SubmitTime','AutoApprovalTime',
	'ApprovalTime','RejectionTime','RequesterFeedback','WorkTimeInSeconds','LifetimeApprovalRate',
	'Last30DaysApprovalRate','Last7DaysApprovalRate','Input.pv_id','Input.global_user_id',
	'Input.time','Input.declaration','Answer.Q1','Approve','Reject']):

	dataSet = qbRel.analyseWorkers();
	badEntries = qbRel.pickBadEntries(dataSet)

	# print dataSet

	dataSet = dataSet.drop(badEntries.index)

	dataSet = dataSet[['WorkerId','Input.declaration','Answer.Q1']]
	silverSet = dataSet['Input.declaration']

	# print silverSet

	# load the fulDataset

	paths = qbPre.listFiles(qbGbl.oriFileName)
	filData = qbPre.readFiles(paths)

	filData = filData[cols];

	filData.index = (xrange(0,len(filData)))

	# remove the observations that were verified earlier as the silver set 
	dups = pd.DataFrame()
	for dec in silverSet:
		# dups = dups.append(filData[filData['Input.declaration']==dec])
		filData = filData.drop(filData[filData['Input.declaration']==dec].index)
	
	badEntries = qbRel.pickBadObs(filData)

	filData = filData.drop(badEntries.index)
	
	dataSet = dataSet.append(filData)
	dataSet = dataSet[['WorkerId','Input.declaration','Answer.Q1']]
	dataSet.index = (xrange(0,len(dataSet)))

	# print dataSet
	dataSet.to_csv(qbGbl.finalReaderFile,header=False);


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
	filData = qbPre.importFilCSV(qbGbl.finalReaderFile,False);
	
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
def classifyData(X,Y,C=[0.7]):
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
	# filData = filData[['WorkerId','Input.declaration','Answer.Q1']]
	filData = filData[['WorkerId','Input.declaration','Answer.Q1']]

	new = filData

	filename = '{0}/PerfectDataset.csv'.format(qbGbl.oriFileName)

	old = qbPre.readDataFrame(filename,None,0)

	# print new['Input.declaration'].nunique()
	# print len(old['declaration'].unique())
	filData = pd.Series(old['declaration']).drop_duplicates()
	print filData
	# tempSer = pd.Series(new['Input.declaration']).drop_duplicates()
	tempSer = new.drop_duplicates(cols=['Input.declaration'])
			
	print len (new)
	print len(tempSer)

	# print len(filData)
	# print '================='
	accuracy = []
	count=0;
	# print len(new)
	# print len(old)

	for row in filData:
		# print row
		if not (new[new['Input.declaration'] == row].empty):
			if len(new[new['Input.declaration'] == row])>1:
				print new[new['Input.declaration'] == row]
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

	print count

	P.figure();

	n, bins, patches = P.hist(accuracy,len(set(accuracy)), histtype='step',cumulative=True,normed=1)

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



def filterNoneObs(type):
	filData = qbPre.readDataFrame('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),None,0);
	noneData = filData[filData.answer=='None']
	noneData.to_csv('{0}_{1}.csv'.format(qbGbl.noneSetFileName,type),index = False);


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
# types = ['100','110','111']
# # start tokenizing the stuff
# for t in types:
# 	type = t;
# 	# prepareData(type);

# # 	# qbRel.goldenSet(100);

# 	# ## carry out word scoring and related statistics
# 	# initData, dataX, dataY = preProcessData(type);
# 	print '\n'
# 	print 'Classitying data using text preProcessing specification {0}'.format(type)
# 	print '\n'
# 	filData,X,Y = preProcessData(type);

# 	# print Y
# 	# scores = cv.cross_val_score(qbPrepare.classifier,X,Y,cv=10,scoring='precision')

# 	# test.testingSVM()
# 	classifyData(X,Y,C=[0.1,0.5,0.7,1.0,1.2,2.0])
# 	print '\n'

################################ Analyse the dataset for reliability ############################################
	
analyse('{0}/Batch_1191444_batch_results.csv'.format(qbGbl.oriFileName))



# cleanExistingData('{0}/Batch_1189077_batch_results.csv'.format(qbGbl.oriFileName),'{0}/seededfeedback.clean.txt'.format(qbGbl.oriFileName))


############################## filter data and do the classification process ####################################

# filData = filterData2(cols=['SubmitTime','WorkerId','Input.declaration','Answer.Q1'])

# types = ['100','110','111']
# types = ['111']

# start tokenizing the stuff
# for t in types:
# 	type = t;
# 	# prepareData(type);

# 		# print '\n'
# 	print 'Classitying data using text preProcessing specification {0}'.format(type)
# 	print '\n'
# 	filData,X,Y = preProcessData(type);

# 	# print Y
# 	# scores = cv.cross_val_score(qbPrepare.classifier,X,Y,cv=10,scoring='precision')

# 	# test.testingSVM()


# 	# classifyData(X,Y,C=[0.1,0.5,0.7,1.0,1.2,2.0])
# 	classifyData(X,Y)
# 	print '\n'

########################## New topic detection in the observations ###########################################

# types = ['100','110','111']
# types = ['100']

# for type in types:
# 	# write only the none obs to different files
# 	# filterNoneObs(type);
# 	print type
# 	# read the file
# 	filData = qbPre.readDataFrame('{0}_{1}.csv'.format(qbGbl.noneSetFileName,type),None,0);

# 	X = qbPrepare.generateX(filData)
# 	corpus = gensim.matutils.Sparse2Corpus(X,documents_columns=False)
# 	gensim.corpora.MmCorpus.serialize('/tmp/corpus.mm', corpus)

# 	mm = gensim.corpora.MmCorpus('/tmp/corpus.mm')

	
	

# 	# for p in corp:
# 		# print p

# 	# print qbGbl.wordRefDict

# 	lda = gensim.models.ldamodel.LdaModel(mm,10,id2word=qbGbl.wordRefDict, update_every=1, chunksize=10000, passes=1, alpha=0.001,eta=0.00000001)
# 	# lda.update(mm)
# 	temp = lda.print_topics(10)
# 	print len(temp)
# 	for t in temp:
# 		print t
# 	# qbPrepare.genTopics(corpus)
	


