
from pyclustering.utils import euclidean_distance_square
from clustering_final import Clustering
from distance import min_distance, max_distance
#from normalization import normalized_X
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import timeit
from Node import Node
import pandas as pd
#from sklearn.preprocessing import normalize


# numberOfCluster = 40
# numberOfLevels = 1


from GMM import GMM
from Utils import checkResult


def InitialTwoRecords(cluster):
    maxdis = 0
    selectedNode1 = None
    selectedNode2 = None

    for node1 in cluster.root.children:
        for node2 in cluster.root.children:
            distmin , distmax = cluster.dismatrix[1][node1.id][node2.id]
            if maxdis < distmax:
                maxdis = distmax
                selectedNode1 = node1
                selectedNode2 = node2
    candR = selectedNode1.elements + selectedNode2.elements

    maxdis = 0

    for i in candR:
        for j in candR:
            if i != j:
                dis = euclidean_distance_square(i, j)
                if maxdis < dis:
                    maxdis = dis
                    record1 = i
                    record2 = j

    selectedNode1.elements.remove(record1)
    selectedNode2.elements.remove(record2)

    return  (record1,record2)


def AugGMM(cluster, X, K, indexMap, record1,record2):
    l = 1
    S = []
    S.append(record1)
    S.append(record2)
    X.remove(record1)
    X.remove(record2)


    minMap = {}
    for node1 in cluster.root.children:

        ##########item to cluster distance##########

        id = indexMap[tuple(record1)]
        distmin, distmax = cluster.dismatrixitem[l][id][node1.id]
        minMap[node1.id] = (distmax, distmin)

        ##########cluster to cluster distance##########

        # id = cluster.documentMap[tuple(a)][l]
        # distmin, distmax = cluster.dismatrix[l][id][node1.id]
        # minMap[node1.id] = (distmax,distmin)

    lastItem = record2

    for k in range(K - 2):
        candR = DivGetBatch(cluster, S, minMap, lastItem, indexMap)
        L = []
        maxval = 0
        maxitem = None
        for i in candR:
            min = float("inf")
            for j in S:
                dist = euclidean_distance_square(i, j)
                if min >= dist:
                    min = dist
                if min <= maxval:
                    break
            if min >= maxval:
                maxval = min
                maxitem = i
            L.append(min)


        lastItem = maxitem

        S.append(maxitem)
        X.remove(maxitem)
        id = cluster.documentMap[tuple(maxitem)][l]
        node = cluster.root.children[id - 1]
        node.elements.remove(maxitem)

    return S



def DivGetBatch(cluster,S,minMap,lastItem,indexMap):

    lBGMM,uBGMM = CalculateBound(cluster,S,minMap,lastItem,indexMap)
    candR = SkipNode(cluster,lBGMM,uBGMM)
    #print(" |candR| by DivGetBatch: ", len(candR))
    return candR


def CalculateBound(cluster,S,minMap,lastItem,indexMap):
    l = 1
    lBGMM = []
    uBGMM = []
    for node1 in cluster.root.children:
        e = lastItem

        ##########cluster to cluster distance##########
        # id = cluster.documentMap[tuple(e)][l]
        # distmin, distmax = cluster.dismatrix[l][id][node1.id]

        ######### item to cluster distance ############
        id = indexMap[tuple(e)]
        distmin, distmax = cluster.dismatrixitem[l][id][node1.id]

        minmax = minMap[node1.id][0]
        minmin = minMap[node1.id][1]
        if minmax > distmax:
            minmax = distmax

        if minmin > distmin:
            minmin = distmin

        minMap[node1.id] = (minmax, minmin)
        lBGMM.append(minmin)
        uBGMM.append(minmax)
    return  (lBGMM,uBGMM)


def SkipNode(cluster,LLmin,LLmax):
    maxofMin = max(LLmin)
    candR = []
    i = 0
    for it in LLmax:
        if it >= maxofMin:
            candR = candR + cluster.root.children[i].elements
        i = i + 1
    return candR
