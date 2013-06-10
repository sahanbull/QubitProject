
####################### import pacakages #####################

import qbPreprocess as qbPre
import qbReliability as qbRel
import qbGlobals as qbGbl

########################## Main functions ########################

def filterData():
	filData = []; # to store the filtered dataset
	count = 1; # to keep the counter

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
	filData = qbPre.importFilCSV(qbGbl.filFileName);

	# generate observation list
	obsDict = qbRel.genObsDict(filData);
	
	# generate worker list 
	workDict = qbRel.genWorkDict(filData); 

	scoreCard = qbRel.scoreWorkers(obsDict,workDict,filData)

	return scoreCard

## this funciton tokenizes the words
def prepareData(type):
	# load the filtered dataset
	filData = qbPre.importFilCSV(qbGbl.filFileName);

	filData = qbPre.prepareData(filData,type);

	# write filtered data to a different file in the HDD 
	qbPre.writeFilCSV('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),filData);

## this function reads preProcessed Data and vectorise it
def preProcessData(type):
	# load the cleaned dataset
	filData = qbPre.readFile('{0}_{1}.csv'.format(qbGbl.dataSetFileName,type),type);
	print qbGbl.wordIDFDict


########################## Main Script ########################

## filter the data from the main dataset and write the only relevant files to new file
#filterData()	

## carry out reliabilty scoring and then write results to a CSV file
# scoreCard = doReliabilityScoring();
# qbRel.writeScorecard(qbGbl.scoreFileName,scoreCard);

## start tokenizing the stuff
type = '100';
#prepareData(type);

preProcessData(type);
