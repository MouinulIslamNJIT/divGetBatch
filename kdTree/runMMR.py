
#from Utils.IndexTree import BuildIndex
from kdtree import kdTree
import timeit
from Utils import yelp_data,makeBlobs_data,movieLens_data
from AugMMR import AugMMR
from MMR import MMR
from Utils import checkResult
import numpy as np


def runMMR(sampleSize, arity,numberofLevel,k):

    print('dataset size: ', sampleSize, 'k:', k, 'number of arity: ',
          arity, 'number of level: ', numberofLevel)

    #X = movieLens_data(sampleSize)
    #X = yelp_data(sampleSize)
    X= makeBlobs_data(sampleSize)*100
    #X = np.array([[-5, -6], [1, 2], [6, 2], [3, 4], [5, 6],[5.5,5.8], [-2, -4], [-7, 10], [8, -7]])



    X1= X[:,0]
    Y1=X[:,1]

    #height = 6
    kdt = kdTree(X1,Y1,numberofLevel)




    
    xin = X.tolist()
    #iTree,indexMap = BuildIndex(xin,arity,numberofLevel,False)
    
    indexMap = kdt.indexMap

    q = [2, 5]
    lambda_score = 0.8

    Xmmr = X.tolist()
    start = timeit.default_timer()

    mmrResult = MMR(lambda_score, q, Xmmr, k)

    #print("mmr", mmrResult)
    stop = timeit.default_timer()
    mmr_time = stop - start
    print('Time for mmr: ', mmr_time)


    start = timeit.default_timer()

    augmmrResult = AugMMR(kdt,numberofLevel,arity,q,lambda_score,k,indexMap)
    #print("aug", augmmrResult)

    stop = timeit.default_timer()
    augmmr_time = stop - start
    print('Time for aug-mmr: ', augmmr_time)

    checkResult(augmmrResult, mmrResult)


