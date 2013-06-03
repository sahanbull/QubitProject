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

	x=0; # keeps local count of the iterator >> replaced by boolean flag
	for row in realFile:
		
		# gets rid of the titles
		if x==0:
			x+=1; # count ++
			continue;

		# 15: worker ID
		# 30: feedback content
		# 31: classified classes
		#print '{0} {1} {2} {3}'.format(x,row[15],row[30],row[31]); 
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
def importFilCSV():
	pass		

######################## Import real data #######################



## this function loads the filtered file to the RAM for processing
def loadFile():
	pass



####################### import pacakages #####################

import csv
import glob

#import importData

########################## Main Script ########################

filData = []; # to store the filtered dataset
count = 1; # to keep the counter

# read original file and load the relevant data
OriFileName = 'data\\read';
# list all the csv log files with records
paths = listFiles(OriFileName);

# foreach csv file in the paths
for path in paths:
	filterSet = filterFile(path,count); # filter data 
	filData.extend(filterSet[0]); # add to the filtered dataset in RAM
	count = filterSet[1]; # update count

# write filtered data to a different file in the HDD 
filFileName = 'data/write/fil_comb_results.csv';
writeFilCSV(filFileName,filData);

