from pyclustering.utils import euclidean_distance_square
from clustering_final import Clustering
from distance import min_distance, max_distance
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import timeit
from Node import Node
import pandas as pd
#from sklearn.preprocessing import normalize

from GMM import GMM
from AugGMM import InitialTwoRecords, AugGMM
from Utils import checkResult

def runGMM(numberofSample, numberofCluster, numberofLevel, Kvalue):
    f = open('MMRoutput.txt', 'a')
    print('dataset size: ', numberofSample, 'k:', Kvalue, 'number of cluster: ',
          numberofCluster, 'number of level: ', numberofLevel, file=f)
    print('dataset size: ', numberofSample, 'k:', Kvalue, 'number of cluster: ',
          numberofCluster, 'number of level: ', numberofLevel)

    X, Y = make_blobs(n_samples=numberofSample, centers=500, cluster_std=0.10, random_state=0)

    #dataset=pd.read_csv('business.csv' , nrows=numberofSample)
    #dataset=pd.read_csv('ratings.csv' , nrows=numberofSample)

    #X = dataset.iloc[:, [2,3]].values
    #X = dataset.iloc[:, [6,7,8]].values

    #normalized_X = normalize(X, axis=0, norm='l2')*1000000
    #normalized_X = normalize(X, axis=0, norm='l2')*1000

    #X = normalized_X

    indexMap = {}
    index = 0
    for e in X:
        indexMap[tuple(e)] = index
        index = index + 1

    start = timeit.default_timer()
    cluster = Clustering(X.tolist(), numberofCluster, numberofLevel)
    cluster.buildTree(cluster.root)
    cluster.createLevelMatrix(cluster.root)
    cluster.createDistanceMatrix(numberofCluster, numberofLevel)
    cluster.createDistanceMatrixforelements(numberofCluster, numberofLevel)

    record1,record2  = InitialTwoRecords(cluster)

    stop = timeit.default_timer()

    print('Time for indexing: ', stop - start)

    Xgmm = X.tolist()
    start = timeit.default_timer()

    augGmmResult = AugGMMXXX(cluster, Xgmm, Kvalue, indexMap,record1,record2)
    #print("aug", augGmmResult)

    stop = timeit.default_timer()

    auggmm_time = stop - start

    auggmm_final = auggmm_time

    print('Time for aug-gmm: ', auggmm_final, file=f)
    print('Time for aug-gmm: ', auggmm_final)



    Xgmm = X.tolist()
    start = timeit.default_timer()

    gmmResult = GMM(Xgmm, Kvalue,record1,record2)
    #print("gmm", gmmResult)
    # GMM(Xgmm, Kvalue)
    stop = timeit.default_timer()

    gmm_time = stop - start
    gmm_final = gmm_time

    print('Time for gmm: ',gmm_final , file=f)
    print('Time for gmm: ', gmm_final)


    print("gmm/auggmm = ", gmm_final/auggmm_final)

    checkResult(augGmmResult, gmmResult)

def main():

    runGMM(1000, 20, 1, 20)

main()