
# This module keeps all the funcions in creating X and Y matrices that are required for classification
# has methods that produces x vectors, y vector, Do TF counting etc.. 

############################## import modules #############################################

from collections import Counter;
import numpy;

import qbGlobals as qbGbl;


## this function takes the feedback word vector and tramnforms it to a BOW vector according to dictionary to be 
# compatible with the SVM classification
def generateX(filData):

	obs = len(filData);
	dim = len(qbGbl.wordIDFDict)
	
	print obs;
	print dim
	X = numpy.zeros([obs,dim]);

	# for row in filData:
	# 	tfidf = dict(Counter(row[1]));
	# 	for word in tfidf:
	# 		tfidf[word] = tfidf[word]*qbGbl.wordIDFDict[word];
	# 		X[int(row[0]),word] = tfidf[word];
		
	return X;	

def generateY(filData):
	obs = len(filData);
	# cls = len(qbGbl.)
	