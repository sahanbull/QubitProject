
# This module keeps all the funcions in creating X and Y matrices that are required for classification
# has methods that produces x vectors, y vector, Do TF counting etc.. 

############################## import modules #############################################

from collections import Counter;
import numpy;

import qbGlobals as qbGbl;


## this function takes the feedback word vector and tramnforms it to a BOW vector according to dictionary to be 
# compatible with the SVM classification
# def generateX(filData):

# 	obs = len(filData);
# 	dim = len(qbGbl.wordIDFDict)
	
# 	# print obs;
# 	# print dim
# 	X = numpy.zeros([obs,dim]);

# 	# foreach row in the dataset,
# 	for row in filData:
# 		# get the tf values of each word in the string
# 		tfidf = dict(Counter(row[1]));

# 		# foreach word in the row,
# 		for word in tfidf:
# 			# multiply by IDF for the word
# 			tfidf[word] = tfidf[word]*qbGbl.wordIDFDict[word];

# 			# place it in correct matrix observation
# 			# X(obs ref,word ref)
# 			X[int(row[0]),word] = tfidf[word];
		
# 	return X;	

def generateX(filData):
	print (filData);

## this funciton generates the y vector for each class and produces a matrix with Ys
# def generateY(filData):
# 	obs = len(filData);
# 	# print qbGbl.classDict
# 	cls = len(qbGbl.classDict)-1;
# 	# generate zero matrix
# 	Y = numpy.zeros([obs,cls]);

# 	# foreach observation in dataset
# 	for row in filData:
# 		# foreach topic entry in observation,
# 		for entry in row[2]:
# 			# if the topic is present,
# 			if entry in xrange(0,cls):
# 				# mark that matrix location as 1
# 				Y[int(row[0]),entry] = 1;
	
# 	return Y