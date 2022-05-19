import numpy as np
import numpy.matlib
    
def kNearestNeighbors(dataMatrix = None,queryMatrix = None,k = None): 
    #--------------------------------------------------------------------------
# Program to find the k - nearest neighbors (kNN) within a set of points.
# Distance metric used: Euclidean distance
    
    # Usage:
# [neighbors distances] = kNearestNeighbors(dataMatrix, queryMatrix, k);
# dataMatrix  (N x D) - N vectors with dimensionality D (within which we search for the nearest neighbors)
# queryMatrix (M x D) - M query vectors with dimensionality D
# k           (1 x 1) - Number of nearest neighbors desired
    
    # Example:
# a = [1 1; 2 2; 3 2; 4 4; 5 6];
# b = [1 1; 2 1; 6 2];
# [neighbors distances] = kNearestNeighbors(a,b,2);
    
    # Output:
# neighbors =
#      1     2
#      1     2
#      4     3
    
    # distances =
#          0    1.4142
#     1.0000    1.0000
#     2.8284    3.0000
#--------------------------------------------------------------------------
    
    neighborIds = np.zeros((queryMatrix.shape[1-1],k))
    neighborDistances = neighborIds
    numDataVectors = dataMatrix.shape[1-1]
    numQueryVectors = queryMatrix.shape[1-1]
    for i in np.arange(1,numQueryVectors+1).reshape(-1):
        dist = np.sum((np.matlib.repmat(queryMatrix(i,:),numDataVectors,1) - dataMatrix) ** 2, 2-1)
        sortval,sortpos = __builtint__.sorted(dist,'ascend')
        neighborIds[i,:] = sortpos(np.arange(1,k+1))
        neighborDistances[i,:] = np.sqrt(sortval(np.arange(1,k+1)))
    
    return neighborIds,neighborDistances