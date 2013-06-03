######################## Preprocess data #########################

## this function filters and returns the specified fields only
def filterFile(file):

	filData = []; # stores the filtered dataset with only the relevant fields

	# opens the csv file
	csvFile = open(file,'rb');

	# reads the csv content
	realFile = csv.reader(csvFile, delimiter=',');

	x = 0; # keeps count of the iterator
	for row in realFile:
		
		# gets rid of the titles
		if x==0:
			x+=1; # conter ++
			continue;

		# 15: worker ID
		# 30: feedback content
		# 31: classified classes
		#print '{0} {1} {2} {3}'.format(x,row[15],row[30],row[31]); 
		filData.append([x,row[15],row[30],row[31]]);
		x+=1; # conter ++
		if x>20:
			break;

	# return the filtered relevant data		
	return filData;

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
#import importData

########################## Main Script ########################

## read original file and load the relevant data
OriFileName = 'data/Batch_1118256_batch_results.csv';
filData = filterFile(OriFileName);

## write relevant data to a different 
filFileName = 'data/Batch_1118256_batch_fil_results.csv';
writeFilCSV(filFileName,filData);

