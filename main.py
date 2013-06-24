
####################### import pacakages #####################

import numpy;

import qbPreprocess as qbPre
import qbReliability as qbRel
import qbGlobals as qbGbl
import qbPrepare as qbPrepare

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
	qbRel.generateSample(qbGbl.fullConFeedbacks,5000,'{0}{1}'.format(qbGbl.oriFileName,qbGbl.newSampFileName),40000)

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
	 print filData
	filData = qbPre.prepareData(filData,type);

	# write filtered data to a different file in the HDD 
	qbPre.writeFilCSV('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),filData);

## this function reads preProcessed Data and vectorise it
def preProcessData(type):
	# load the cleaned dataset
	filData = qbPre.readFile('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),type);

	X = qbPrepare.generateX(filData);
	Y = []#qbPrepare.generateY(filData);
	
	return [filData,X,Y] 


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

# start tokenizing the stuff
type = '100';
prepareData(type);

# qbRel.goldenSet(100);

## carry out word scoring and related statistics
initData, dataX, dataY = preProcessData(type);
