
################### global variables #######################

oriFileName = 'data\\read';

filFileName = 'data\\write\\fil_comb_results.csv';

# record simple only dataset
dataSetFileName = 'data\\write\\dataSet'

# where to record worker scorecards
scoreFileName = 'data\\relAnalytics\\worker_scorecard.csv'

# to store required attributes
att = 'data\\attributes';

# keeps the class references <class ref: ref index>
classDict = {};

clsDictFileName = '{0}\\classDict.csv'.format(att);


classUIRef = {};

classUIRefFileName = '{0}\\classUIRef.csv'.format(att);


wordRefDict = {};

wordRefDictFileName = '{0}\\wordRefDict'.format(att);


wordIDFDict = {};

wordIDFDictFileName = '{0}\\wordIDFDict'.format(att);


## lists and data items for visual analytics

topicHist = {}; # to store the topic ditribution

workTopics = {}; # to store the topic distribution per worker