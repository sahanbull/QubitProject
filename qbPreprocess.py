######################## Preprocess data #########################

import csv
import glob

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

	x=0; # keeps local count of the iterator >> replaced by boolean flag
	#foreach row in the csv file
	for row in realFile:
		
		# gets rid of the titles
		if x==0:
			x+=1; # count ++
			continue;

		# 15: worker ID
		# 30: feedback content
		# 31: classified classes
		filData.append([count,row[15],row[30],row[31]]);
		x+=1; # local cont ++
		count+=1; # counter ++
		if x>20:
			break;

	# return the filtered relevant data		
	return [filData,x];

## this function writes the filtered dataset to a new file for operational convinience
def writeFilCSV(file,filData):

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# foreach row in the filtered dataset
	for row in filData:
		realFile.writerow(row); # write to file

## this funciton imports the specified data set given in the string
def importFilCSV(file):

	# to store the reading dataset
	filData = [];

	# opens the csv file
	csvFile = open(file,'rb');

	# reads the csv content
	realFile = csv.reader(csvFile, delimiter=',');
			
	for row in realFile:

		# 0: ref ID
		# 1: worker ID
		# 2: feedback content
		# 3: classified classes
		filData.append(row);

	return filData

## this function conversts the string of classification to useable list
def convClasses(filData,split):
	for row in filData:
		temp = row[3].split(split)
		row[3] = temp;

	return filData