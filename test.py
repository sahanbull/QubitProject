import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer;
from sklearn.feature_extraction.text import CountVectorizer;

from sklearn.multiclass import OneVsRestClassifier;
from sklearn.svm import SVC

def testingSVM():
     X_train = np.array(["new york is a hell of a town","new york was originally dutch","the big apple is great","new york is also called the big apple","nyc is nice","people abbreviate new york city as nyc","the capital of great britain is london","london is in the uk","london is in england","london is in great britain","it rains a lot in london","london hosts the british museum","new york is great and so is london","i like london better than new york"])

     Y_train = [[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[1,1],[1,1]]
     # Y_train = [[0],[0],[0],[0],[0],[0],[1],[1],[1],[1],[1],[1],[0,1],[0,1]]

     X_test = np.array(['nice day in nyc','welcome to london','hello welcome to new york enjoy it here and london too'])

     tf = TfidfVectorizer()
     X = tf.fit_transform(X_train)
     print X
     print tf.get_feature_names()
     Y = np.array(Y_train)
     print Y
     clf = OneVsRestClassifier(SVC(kernel = 'linear'));

     clf.fit(X,Y)

     print X_test.shape
     newX = tf.transform(X_test)

     predicted = clf.predict(newX)
     print 'iooo'
     print predicted