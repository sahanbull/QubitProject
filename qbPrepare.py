
# This module keeps all the funcions in creating X and Y matrices that are required for classification
# has methods that produces x vectors, y vector, Do TF counting etc.. 

############################## import modules #############################################

from collections import Counter;
from sklearn.feature_extraction.text import TfidfVectorizer;
from sklearn.feature_extraction.text import CountVectorizer;

from sklearn import cross_validation

from sklearn.multiclass import OneVsRestClassifier;
from sklearn.svm import SVC


import numpy; 

import qbGlobals as qbGbl;


## this function takes the feedback word vector and tramnforms it to a BOW vector according to dictionary to be 
# compatible with the SVM classification
def generateX(filData):

	# initiate transformer : tf-idf vectoriser
	# token pattern changed to define single char tokens as words.. (default : 2+ chars -> word)
	xTransformer = TfidfVectorizer(min_df=0.0,stop_words=None,token_pattern ="(?u)\\b\w+\\b"); 

	# vectorize \m/
	# print filData['declaration']
	X = xTransformer.fit_transform(filData['declaration'])
	
	# print xTransformer.get_feature_names();
	
	# save the word feature references
	qbGbl.wordRefDict = xTransformer.get_feature_names();

	return X

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

def generateY(filData):

	# initiate transformer : binary count vectoriser
	# stopword=> None to classify the None observations as negative examples
	yTransformer = CountVectorizer(min_df = 0.0, binary=True, lowercase = False)#, stop_words=[u'None']);

	# vectorize \m/
	Y = yTransformer.fit_transform(filData['answer']); 
	# print Y

	# tempY = Y.todense()
	
	# for row in tempY:
	# 	temp = []
	# 	for topic in xrange(0,row.shape[1]-1):
	# 		# if row[topic] != 0:
	# 			print 
	# # save topic labels to a reference dictionary
	# qbGbl.classDict = yTransformer.get_feature_names();

	return Y

## this function converts the dataset to fractions of train and test data :D
def segmentData(X,Y,fraction):
	XTrain, XTest, YTrain, YTest = cross_validation.train_test_split(X,Y,test_size=fraction,random_state=0)

	return XTrain, XTest, YTrain, YTest

## this function does the classification using a SVM classifier and gives generalization error
def classify(XTrain,XTest,YTrain,YTest):
	print XTrain.shape,XTest.shape,YTrain.shape,YTest.shape;
	classifier = OneVsRestClassifier(SVC(kernel='linear'));

	# print classifier
	YTrain = YTrain.todense()
	XTrain = XTrain.todense()

	print type(YTrain)
	print type(XTrain)

	classifier.fit(XTrain, YTrain)





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