

from pyclustering.utils import euclidean_distance_square
from clustering_final import Clustering
from Utils import get_object_size
#from normalization import normalized_X
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import timeit
from Node import Node
import pandas as pd
from sklearn.preprocessing import normalize

from GMM import GMM
from Utils import checkResult,InitialTwoRecordsInGMM
from AugGMM import AugGMM

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
    iTree.createDistanceMatrixforelements(arity, numberofLevel)
    initRecords = InitialTwoRecordsInGMM(iTree)
    iTree.cleanUp(iTree.root)
    print(get_object_size(iTree))



    stop = timeit.default_timer()


    print('Time for indexing: ', stop - start)

    Xgmm = X.tolist()
    start = timeit.default_timer()

    gmmResult = GMM(Xgmm, Kvalue,initRecords)

    print("gmm", gmmResult)
    # GMM(Xgmm, Kvalue)
    stop = timeit.default_timer()

    gmm_time = stop - start
    gmm_final = gmm_time

    print('Time for gmm: ',gmm_final , file=f)
    print('Time for gmm: ', gmm_final)

    Xgmm = X.tolist()
    start = timeit.default_timer()

    augGmmResult = AugGMM(iTree,numberofLevel,arity, Xgmm, Kvalue,indexMap,initRecords)
    print("aug", augGmmResult)

    stop = timeit.default_timer()

    auggmm_time = stop - start

    auggmm_final = auggmm_time

    print('Time for aug-gmm: ',auggmm_final , file=f)
    print('Time for aug-gmm: ', auggmm_final)

    checkResult(augGmmResult, gmmResult)

def main():

    run(1000,20 , 1 ,20)

main()
