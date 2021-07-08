import itertools
import random
import math
import numpy
from MaintenanceCodes.distance_final2 import min_distance, max_distance,min_max_distance
from MaintenanceCodes.clustering_final2 import Clustering
import random
import timeit
import pandas as pd
import numpy as np
from numpy import asarray
from numpy import savetxt
import scipy.spatial.distance
from Utils.Utils import maintenanceMakeBlob
from Utils.Utils import getMaintenanceData


#def euclideanDist(x, y):
#    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
#    return distance


#df = pd.read_csv("randomData10k.csv", header= None)

#X = df.iloc[:,:].values


#df = pd.read_csv("makeblobs-1M.csv", header= None)

#df = pd.read_csv("randomData1M.csv", header= None)
#df = pd.read_csv("randomData10k.csv", header= None)


def delete():
    path = r'Dataset\MaintenanceDataset\randomData10k.csv'
    df = getMaintenanceData(path)


    #df = pd.read_csv("makeblobs.csv", header= None)

    X = df.iloc[:,:].values

    # delete 10 items from random data


    numberofCluster =50


    # 10 delete
    #S10 =[]
    #for i in range(5):
    #    index = random.randint(0, len(X)-1)
    #    S10.append(X[index])

    #S10 = []
    #index = list(np.random.choice(np.arange(0,len(X)), 10, replace=False))
    #for i in index:
    #    S10.append(X[i])

    #data = asarray(S10)
    # #save to csv file
    #savetxt('test-10.csv', data, delimiter=',')






    path = r'Dataset\MaintenanceDataset\test-10.csv'
    df2 = getMaintenanceData(path)


    S = df2.iloc[:, :].values
    #print(S)


    #for element in S:
    #    if element in X:
    #        print("yes")




    #print(X[0])
    #print(S)
    numberofLevel = 1

    cluster = Clustering(X, numberofCluster, numberofLevel)
    cluster.buildTree(cluster.root)

    Sids = {}

    for i in S:
        id = cluster.documentMap[tuple(i)][numberofLevel]
        Sids[tuple(i)] = id

    cluster.createLevelMatrix(cluster.root)
    simMatrixNode = cluster.createDistanceMatrix(numberofCluster, numberofLevel)
    Nodes = cluster.createNodes(numberofCluster, numberofLevel)




    print("simMatrixNode created")


    start = timeit.default_timer()


    #New_Nodes = Nodes

    keys = []
    for key, l in Nodes.items():
        for elements in l:
            for item in S:
                if np.array_equal(item,elements):
                    #print("l",l)
                    index = np.where(l == item)[0][0]
                    #print("len l ", len_l)
                    l = np.delete(l,index,0)
        Nodes[key] = l
                    #print("l after delete", l)


    print("item deleted")
    #print(Nodes)
    #for key, l in Nodes.items():
    #    if key not in keys:
    #        New_Nodes[key] = l


    #if New_Nodes.values() != Nodes.values():
    #    print("yes")

    #print(sum(len(v) for v in Nodes.values()))
    #print(sum(len(v) for v in New_Nodes.values()))


    # update simmatrixnode

    for item in S:
        j = Sids[tuple(item)]
        for p in range(1 , numberofCluster+1):
            if j != p:
                for elem in simMatrixNode[1][j][p][2]:
                    if item[0] == elem[0]  and item[1] == elem[1]:

                        simMatrixNode[1, j, p] = min_max_distance(Nodes[j], Nodes[p])



    print("simMatrixNode updated")
    #for each cluster pair, find the 4 items that are responsible for min max similarity distance
    # between those nodes
    # we do this for all pair of nodes
    #after that we only check if deleted item is coming from step 1 or not



    #print(newSimMatrixNode)


    stop = timeit.default_timer()
    #print(Nodes.items())
    print('Time: ', stop - start)

'''
key_item = []
for i in S:
    for k, v in Nodes.items():
        for item in v:
            if i == item:
                key_item.append((k,item))

#print(key_item)






for l in range(1, numberofLevel + 1):
    for i in range(1, numberofCluster ** l + 1):
        for j in range(1, numberofCluster ** l + 1):
            if newSimMatrixNode[l][i][j] != simMatrixNode[l][i][j]:
                print("yes")
                
'''