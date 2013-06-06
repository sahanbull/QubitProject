
####################### import pacakages #####################

import csv
import glob

import qbGlobals as qbGbl

######################## Preprocess data #########################

## this function returns all the file paths with .csv extension in the directory
def listFiles(path):
	path = '{0}\\*.csv'.format(path);
	paths = glob.glob(path)
	return paths

## this function filters and returns the specified fields only
def filterFile(file,count):

	filData = []; # stores the filtered dataset with only the relevant fields

	# opens the csv file
	csvFile = open(file,'rb');

	# reads the csv content
	realFile = csv.reader(csvFile, delimiter=',');

	x = True; # keeps local count of the iterator >> replaced by boolean flag
	#foreach row in the csv file
	for row in realFile:
		
		# gets rid of the titles
		if x:
			x = False; # skip topic checked
			continue;

		# 15: worker ID
		# 30: feedback content
		# 31: classified classes
		filData.append([count,row[15],row[30],row[31]]);
		count+=1; # counter ++

	# return the filtered relevant data		
	return [filData,count];

## this function writes the filtered dataset to a new file for operational convinience
def writeFilCSV(file,filData):

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# foreach row in the filtered dataset
	for row in filData:
		realFile.writerow(row); # write to file

## this function conversts the string of classification to useable list
def convClasses(field,split):
	temp = field.split(split);
	return temp;

## this function conversts the string of classification to integer refs in the classDict
def conv2ClsDict(field):
	newField = [];
	for tmpCls in field:
		newField.append(qbGbl.classDict[tmpCls]);

	return newField

## this function generates the dictionary of classes and their indexes
def genClassDict(field,index):
	for tmpCls in field:
		if tmpCls not in qbGbl.classDict:
			qbGbl.classDict[tmpCls] = index;
			index+=1; 
	return index

## this funciton imports the specified data set given in the string
def importFilCSV(file):

	# to store the reading dataset
	filData = [];

	# opens the csv file
	csvFile = open(file,'rb');

	# reads the csv content
	realFile = csv.reader(csvFile, delimiter=',');
	
	index = 1;
	for row in realFile:
		# segment multiple classes
		row[3]=convClasses(row[3],'|');
		index = genClassDict(row[3],index);

		row[3] = conv2ClsDict(row[3])
		# 0: ref ID
		# 1: worker ID
		# 2: feedback content
		# 3: classified classes
		filData.append(row);
	
	return filData