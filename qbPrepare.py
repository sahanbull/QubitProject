
# This module keeps all the funcions in creating X and Y matrices that are required for classification
# has methods that produces x vectors, y vector, Do TF counting etc.. 

############################## import modules #############################################

from collections import Counter;
from sklearn.feature_extraction.text import TfidfVectorizer;
from sklearn.preprocessing import LabelBinarizer

from sklearn import cross_validation
from sklearn import metrics
from sklearn.cross_validation import KFold

from sklearn.multiclass import OneVsRestClassifier;
from sklearn.svm import LinearSVC;

import numpy as np;
import time

import qbGlobals as qbGbl;
import qbPreprocess as qbPre;


# initiate transformer : tf-idf vectoriser
# token pattern changed to define single char tokens as words.. (default :m 2+ chars -> word)
xTransformer = TfidfVectorizer(min_df=0.0,token_pattern =u'(?u)\\b\\w+\\b',ngram_range=(1,1), stop_words='english');

yTransformer = LabelBinarizer()


## this function takes the feedback word vector and tramnforms it to a BOW vector according to dictionary to be 
# compatible with the SVM classification
def generateX(filData):

	# vectorize \m/
	# print filData['declaration']


	X = xTransformer.fit_transform(filData['declaration'])
	
	qbGbl.wordRefDict = {}

	count = 0;
	for word in xTransformer.get_feature_names():
		qbGbl.wordRefDict[count]=word;
		count += 1;	
	# print qbGbl.wordRefDict
	
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

def kFoldGenerator(num,folds):
	kf = KFold(num, n_folds=folds, indices=True)
	
	return kf

def generateY(filData):

	# initiate transformer : binary count vectoriser
	# stopword=> None to classify the None observations as negative examples
	# yTransformer = CountVectorizer(min_df = 0.0, binary=True, lowercase = False)#, stop_words=[u'None']);

	# vectorize \m/
	# Y = yTransformer.fit_transform(filData['answer']); 
	# print Y

	newY = [];
	for answer in filData['answer']:
		temp = qbPre.convClasses(answer,'|');
		newY.append(temp);

	Y = yTransformer.fit_transform(newY)

	qbGbl.classDict = yTransformer.classes_;

	# tempY = Y.todense()
	
	# for row in tempY:
	# 	temp = []
	# 	for topic in xrange(0,row.shape[1]-1):
	# 		# if row[topic] != 0:
	# 			print 
	# # save topic labels to a reference dictionary

	return Y

## this function converts the dataset to fractions of train and test data :D
def segmentData(X,Y,fraction):
	XTrain, XTest, YTrain, YTest = cross_validation.train_test_split(X,Y,test_size=fraction,random_state=0)

	return XTrain, XTest, YTrain, YTest

## this function does the classification using a SVM classifier and gives generalization error
def classify(XTrain,XTest,YTrain,YTest,c,cv=False):
	# print XTrain.shape,XTest.shape,YTrain.shape,YTest.shape;
	

	# print classifier
	# YTrain = YTrain.todense()
	# XTrain = XTrain.todense()

	# print type(XTrain)
	# print type(YTrain)
	start_time = time.time()
	# print XTrain.shape

	classifier = OneVsRestClassifier(LinearSVC(penalty='L1',loss='L2',C=c,dual=False,multi_class='ovr'))#,verbose=1));

	classifier.fit(XTrain, YTrain)

	predicted = classifier.predict(XTest)

	
	# if not a cross-validation instance, need to print results
	if not cv:
		qbGbl.weights = classifier.coef_

		# print report
		print metrics.classification_report(YTest, predicted,target_names=yTransformer.classes_)

		# ##  Collective Statistics
		print 'accuracy score of the classifier: {0}'.format(1.0-metrics.hamming_loss(YTest,predicted))
		print 'value of the C\t\t\t: {0}'.format(c)

		print 'Time taken to classify\t\t: {0} seconds'.format(time.time()-start_time);

		# print 'precision score of the classifier: {0}'.format(metrics.precision_score(YTest,predicted))
		# print 'recall score the classifier: {0}'.format(metrics.recall_score(YTest,predicted))
		# print 'F1 score of the classifier: {0}'.format(metrics.f1_score(YTest,predicted))

	return float(1.0-metrics.hamming_loss(YTest,predicted))

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


def genTopics(corpus):
	lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=10, update_every=1, chunksize=10000, passes=1)