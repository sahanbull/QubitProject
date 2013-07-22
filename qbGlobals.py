
import numpy as np

################### global variables #######################

oriFileName = 'data/read';

filFileName = 'data/write/fil_comb_results.csv';

finalReaderFile = 'data/write/finalReaderFile.csv';

newSampFileName = '/seededfeedback.clean.txt';

# record simple only dataset
dataSetFileName = 'data/write/dataSet'

# record the None of the above observations dataset
noneSetFileName = 'data/write/noneDataSet'



# to store required attributes
att = 'data/attributes';

# keeps the class references <class ref: ref index>
classDict = {};

clsDictFileName = '{0}/classDict.csv'.format(att);


classUIRef = {};

classUIRefFileName = '{0}/classUIRef.csv'.format(att);


wordRefDict = {};

wordRefDictFileName = '{0}/wordRefDict'.format(att);


wordIDFDict = {};

wordIDFDictFileName = '{0}/wordIDFDict'.format(att);


## datasets for analytics

# where to record worker scorecards
scoreFileName = 'data/relAnalytics/worker_scorecard.csv'


## lists and data items for visual analytics

topicHist = {}; # to store the topic ditribution

workTopics = {}; # to store the topic distribution per worker

workDict = {}

## full concordence topics

fullConFeedbacks = [];

weights = np.ndarray([]);
