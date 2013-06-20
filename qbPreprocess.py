
####################### import pacakages #####################

import math
import csv
import glob
import re
import nltk.tokenize as nltkTok
import enchant
from enchant.checker import SpellChecker
import nltk

import qbGlobals as qbGbl

######################## Preprocess data #########################

## this function reads a simple file
def readSimpleFile(file):
	filData = []; # stores the filtered dataset with only the relevant fields

	# opens the csv file
	csvFile = open(file,'rb');

	# reads the csv content
	realFile = csv.reader(csvFile, delimiter=',');

	for row in realFile:
		filData.append(row)

	return filData

## this function returns all the file paths with .csv extension in the directory
def listFiles(path):
	path = '{0}/*.csv'.format(path);

	print path
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

## this function writes useable files with x and y only
def writeUsableCSV(file,filData):

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# foreach row in the filtered dataset
	for row in filData:
		realFile.writerow(row); # write to file

############################## build the dictionaries and manage them ######################

## this function generates the dictionary of classes and their indexes
def genClassDict(field,index):
	for tmpCls in field:
		if tmpCls not in qbGbl.classDict:
			if tmpCls == 'None':
				qbGbl.classDict[tmpCls] = 99;
			else:
				qbGbl.classDict[tmpCls] = index;
				index+=1; 
	return index

## this function writes the dictionary to the specified file
def saveClassDict(file):
	classDict = qbGbl.classDict;

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# # sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# # foreach row in the filtered dataset
	for row in classDict:
		realFile.writerow([row, classDict[row]]); # write to file

## this function reads the classes dictionary from the the file:  HAVE TO BE UPDATED>>>>>>>>>>>>>>>>>>>>>>>>>>
def readClassDict(file):
	print file

## takes the list of tokens and updates the dictionary
def updateWordRefDict(field,index):
	tempIndex = []; # to store indices intiated via this field
	for word in field:
		if word not in qbGbl.wordRefDict:
			qbGbl.wordRefDict[word] = index; # initiate word
			qbGbl.wordIDFDict[index] = 0.0; # initiate IDF for the word
			tempIndex.append(index); # to keep track of new keys for IDF count
			index+=1;  
		else:
			tempIndex.append(qbGbl.wordRefDict[word]); # to count existing keys

	wordSet = set(tempIndex); # make a unique set of words		
	# update IDF counts
	for word in wordSet:
		qbGbl.wordIDFDict[word] += 1.0;

	return [tempIndex,index]

## this function writes the dictionary of ref words to the specified file
def saveWordRefDict(file):
	wordRefDict = qbGbl.wordRefDict;

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# # sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# # foreach row in the filtered dataset
	for row in wordRefDict:
		realFile.writerow([row, wordRefDict[row]]); # write to file


## this function writes the dictionary of ref words to the specified file
def saveWordIDFDict(file):
	wordIDFDict = qbGbl.wordIDFDict;

	# opens the csv file or creates one if its not there
	csvfile = open(file, 'wb');

	# # sets properties and attributes
	realFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC);

	# # foreach row in the filtered dataset
	for row in wordIDFDict:
		realFile.writerow([row, wordIDFDict[row]]); # write to file

##########################################################################################

## This fucntion transforms the words into a list of indices
def convertFeedback(row):
	tempIndex = [];
	pass

## this function reads the preprocessed file
def readFile(file,type):
	filData = []; # stores the filtered dataset with only the relevant fields

	# opens the csv file
	csvFile = open(file,'rb');

	# reads the csv content
	realFile = csv.reader(csvFile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC);

	index = 0;
	for row in realFile:
		# segment multiple classes
		temp =convClasses(row[2],'|');
		row[2] = conv2ClsDict(temp)

		# tokenize the feedback
		tempRow = tokenStr(row[1]);
	 	bundle = updateWordRefDict(tempRow,index);

	 	row[1] = bundle[0];
	 	index = bundle[1];

		filData.append(row);

	numOfDocs = len(filData);
	
	# compute IDF for each word

	for word in qbGbl.wordIDFDict:
		tempDf = qbGbl.wordIDFDict[word];
		qbGbl.wordIDFDict[word] = math.log(numOfDocs/tempDf);

	# save the file in the dictionary in the HDD for later reference
	saveWordRefDict('{0}_{1}.csv'.format(qbGbl.wordRefDictFileName,type));
	
	# save the file in the dictionary in the HDD for later reference
	saveWordIDFDict('{0}_{1}.csv'.format(qbGbl.wordIDFDictFileName,type));

	return filData
	
## this function conversts the string of classification to useable list, >> Split it
def convClasses(field,split):
	temp = field.split(split);
	return temp;

## this function conversts the string of classification to integer refs in the classDict
def conv2ClsDict(field):
	newField = [];
	for tmpCls in field:
		newField.append(qbGbl.classDict[tmpCls]);

	return newField

## this funciton imports the specified data set given in the string
def importFilCSV(file,flag):

	# to store the reading dataset
	filData = [];

	# opens the csv file
	csvFile = open(file,'rb');

	# reads the csv content
	realFile = csv.reader(csvFile, delimiter=',');
	
	index = 0; # to uniquely index classes
	for row in realFile:
		# segment multiple classes
		temp =convClasses(row[3],'|');
		index = genClassDict(temp,index);

		if flag:
			row[3] = conv2ClsDict(temp)

		# 0: ref ID
		# 1: worker ID
		# 2: feedback content
		# 3: classified classes
		filData.append(row);

	saveClassDict(qbGbl.clsDictFileName);

	return filData

## this function tokenizes a string and returns the list of strings
def tokenStr(str):
	return nltkTok.word_tokenize(str);

	# return str.split();

## this function simplifies the text : 
#		removes all non-alpha chars
def simplify(str):
	str = re.sub(r'[^\w\s]','',str);
	return str

## this function converts all the letters to lower class 
def toLower(str):
	return str.lower();

## this function corrects all the spelling
def doSpelling(str):
	
	chkr = SpellChecker("en_GB"); # any english dictionary

	chkr.set_text(str);


	## we can do more similarity ratio checks as well :P right now pick the best match
	for err in chkr:
		str = re.sub(err.word,chkr.suggest(err.word)[0],str)

	# tempStr = tokenStr(str);
	# for word in tempStr:
	# 	if not d.check(word):
	# 		d.suggest(word);

	return str

## this function does the stemming for the words
def doStemming(str):
	myStemmer = nltk.stem.porter.PorterStemmer() # Portor's Stemmer
	tempStr = tokenStr(str);

	str = "";
	for word in tempStr:
		str += myStemmer.stem(word) + " "
	str = str.strip();

	return str

## this function standardizes the text field
def standadiseString(str,type):
	if type[1] == '1':
		str = doSpelling(str);
	if type[2] == '1':
		str = doStemming(str);
	if type[0] == '1':	 
		str = simplify(str);	

	str = toLower(str);	

	return str;

## this function prepares the data in the format specified by type
def prepareData(filData,type):
	tempfilData = [];
	for row in filData:
		# print '==='
		str = row[2];
		#str = tokenStr(str);
		str = standadiseString(str,type);
		tempfilData.append([row[0],str,row[3]]);
	
	return tempfilData