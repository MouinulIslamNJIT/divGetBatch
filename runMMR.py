

from pyclustering.utils import euclidean_distance_square
from IndexTree import Clustering
from Utils import get_object_size
#from normalization import normalized_X
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import timeit
from Node import Node
import pandas as pd
from sklearn.preprocessing import normalize

from AugMMR import AugMMR
from MMR import MMR
from Utils import checkResult


def run(numberofSample, arity,numberofLevel,Kvalue):
    numberofCluster = arity^numberofLevel
    f = open('MMRoutput.txt', 'a')
    print('dataset size: ', numberofSample, 'k:', Kvalue, 'number of cluster: ',
          numberofCluster, 'number of level: ', numberofLevel, file=f)
    print('dataset size: ', numberofSample, 'k:', Kvalue, 'number of cluster: ',
          numberofCluster, 'number of level: ', numberofLevel)

    X, Y = make_blobs(n_samples=numberofSample, centers=10, cluster_std=0.010, random_state=0)


    #dataset=pd.read_csv('business.csv' , nrows=numberofSample)
    # dataset=pd.read_csv('ratings.csv' , nrows=numberofSample)

    # X = dataset.iloc[:, [2,3]].values
    #X = dataset.iloc[:, [6,7,8]].values

    # normalized_X = normalize(X, axis=0, norm='l2')*1000000
    #normalized_X = normalize(X, axis=0, norm='l2')*1000

    #X = normalized_X

    indexMap = {}
    index = 0
    for e in X:
        indexMap[tuple(e)] = index
        index = index + 1

    start = timeit.default_timer()
    iTree = Clustering(X.tolist(), arity, numberofLevel)
    iTree.buildTree(iTree.root)
    iTree.createLevelMatrix(iTree.root)
    iTree.createDistanceMatrix(arity, numberofLevel)
    #iTree.createDistanceMatrixforelements(arity, numberofLevel)

    #iTree.cleanUp(iTree.root)
    #print(get_object_size(iTree))

    q = [2,5]
    lambda_score = 0.8




    stop = timeit.default_timer()
    print('Time for indexing: ', stop - start)

    Xmmr = X.tolist()
    start = timeit.default_timer()

    mmrResult = MMR(lambda_score, q, Xmmr, Kvalue)

    print("mmr", mmrResult)
    # GMM(Xgmm, Kvalue)
    stop = timeit.default_timer()

    gmm_time = stop - start

    print('Time for mmr: ',gmm_time , file=f)
    print('Time for mmr: ', gmm_time)


    start = timeit.default_timer()

    augmmrResult = AugMMR(iTree,numberofLevel,arity,q,lambda_score,Kvalue,indexMap)
    print("aug", augmmrResult)

    stop = timeit.default_timer()

    auggmm_time = stop - start

    auggmm_final = auggmm_time

    print('Time for aug-mmr: ',auggmm_final , file=f)
    print('Time for aug-mmr: ', auggmm_final)


    checkResult(augmmrResult, mmrResult)

def main():

    run(5000,9, 2 ,20)

main()
