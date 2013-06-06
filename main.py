
####################### import pacakages #####################

import qbPreprocess as qbPre
import qbReliability as qbRel
import qbGlobals as qbGbl

########################## Main Script ########################

# filData = []; # to store the filtered dataset
# count = 1; # to keep the counter

# # read original file and load the relevant data
# # list all the csv log files with records
# paths = listFiles(qbGbl.OriFileName);

# # foreach csv file in the paths
# for path in paths:
# 	filterSet = filterFile(path,count); # filter data 
# 	filData.extend(filterSet[0]); # add to the filtered dataset in RAM
# 	count = filterSet[1]; # update count

# write filtered data to a different file in the HDD 
# writeFilCSV(qbGbl.filFileName,filData);

# load the filtered dataset
filData = qbPre.importFilCSV(qbGbl.filFileName);

obsDict = qbRel.genObsDict(filData);
# print filData
#print obsDict
workDict = qbRel.genWorkDict(filData); 


