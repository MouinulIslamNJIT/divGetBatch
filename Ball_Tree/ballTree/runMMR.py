
#from Utils.IndexTree import BuildIndex
from balltree import BallTree
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
    #X = yelp_data(sampleSize)/100
    X= makeBlobs_data(sampleSize)*100
    #X = np.array([[-5, -6], [1, 2], [6, 2], [3, 4], [5, 6],[5.5,5.8], [-2, -4], [-7, 10], [8, -7]])



    # import pandas as pd
    # df = pd.read_csv('2M2FMakeBlobs.csv')
    # df = df.iloc[:sampleSize]
    # X = df.to_numpy()





    #height = 6
    ballTree = BallTree(X,numberofLevel)




    
    xin = X.tolist()
    #iTree,indexMap = BuildIndex(xin,arity,numberofLevel,False)
    
    indexMap = ballTree.indexMap

    q = [200, 500]
    lambda_score = 0.8

    Xmmr = X.tolist()
    start = timeit.default_timer()

    mmrResult = MMR(lambda_score, q, Xmmr, k)

    #print("mmr", mmrResult)
    stop = timeit.default_timer()
    mmr_time = stop - start
    print('Time for mmr: ', mmr_time)


    start = timeit.default_timer()

    augmmrResult = AugMMR(ballTree,numberofLevel,arity,q,lambda_score,k,indexMap)
    #print("aug", augmmrResult)

    stop = timeit.default_timer()
    augmmr_time = stop - start
    print('Time for aug-mmr: ', augmmr_time)

    checkResult(augmmrResult, mmrResult)


