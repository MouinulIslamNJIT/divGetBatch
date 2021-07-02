from pyclustering.utils import euclidean_distance_square
from sklearn.datasets.samples_generator import make_blobs
from MaintenanceCodes.clustering_final import Clustering
import numpy as np
import timeit
import pandas as pd
from sklearn.preprocessing import normalize
import timeit
from numpy import asarray
from numpy import savetxt
import scipy.spatial.distance
import random

from Utils.Utils import maintenanceMovieLens

from Utils.Utils import getMaintenanceData


def grMn():
    numberofCluster = 50
    numberofLevel = 1

    center_box = (1, 100000)

    # 10000
    # X,Y = make_blobs(n_samples=100000, centers=10, center_box=center_box, cluster_std=0.6, random_state=1)

    # data = asarray(X)

    # save to csv file
    # savetxt('makeblobs-100k.csv', data, delimiter=',')

    # mylist = [(random.randint(1, 1000000), (random.randint(1, 1000000))) for k in range(1000000)]

    # print(mylist)

    # data = asarray(mylist)

    # save to csv file
    # savetxt('randomData1M.csv', data, delimiter=',')

    # dataset=pd.read_csv(r'Dataset\ratings\ratings.csv')
    # #df = pd.read_csv("randomData1M.csv", header= None)
    # #dataset = pd.read_csv(r'Dataset\business\business.csv', nrows=10)

    df = maintenanceMovieLens()

    X = df.iloc[:, :].values

    ############ read new data to insert

    path = r'Dataset\MaintenanceDataset\makeblobs-1000.csv'

    df2 = getMaintenanceData(path)
    S = df2.iloc[:, :].values

    cluster = Clustering(X, numberofCluster, numberofLevel)
    cluster.buildTree(cluster.root)
    cluster.createLevelMatrix(cluster.root)
    simMatrixNode = cluster.createDistanceMatrix(numberofCluster, numberofLevel)

    nodes = cluster.createNodes(numberofCluster, numberofLevel)

    nodescentroids = cluster.createNodesCentroids(numberofCluster, numberofLevel)

    print("clustering finished")

    start = timeit.default_timer()

    selectedNodes = []

    for item in S:
        mindis = 100000000000000000000
        for key, value in Clustering.centroids.items():

            dist = (item[0] - value[0]) ** 2 + (item[1] - value[1]) ** 2

            if dist < mindis:
                mindis = dist
            min_key = key
        selectedNodes.append((min_key, item))

    print("finding closest node finished")

    minUpdate = [[0 for x in range(numberofCluster + 1)] for y in range(numberofCluster + 1)]
    maxUpdate = [[0 for x in range(numberofCluster + 1)] for y in range(numberofCluster + 1)]

    totalUpdate = 0
    for j in range(1, numberofCluster + 1):
        z = scipy.spatial.distance.cdist(S, nodes[j], 'euclidean')
        for i in range(len(S)):
            nodeID = selectedNodes[i][0]
            if (nodeID != j):
                prevmin = simMatrixNode[1][nodeID][j][0]
                prevmax = simMatrixNode[1][nodeID][j][1]

                newmin = z[i][:].min() ** 2
                newmax = z[i][:].max() ** 2

                if (prevmin > newmin):
                    # update simmatrixnode

                    minUpdate[nodeID][j] = minUpdate[nodeID][j] + 1
                    totalUpdate = totalUpdate + 1
                if (prevmax < newmax):
                    # update simmatrixnode
                    maxUpdate[nodeID][j] = maxUpdate[nodeID][j] + 1
                    totalUpdate = totalUpdate + 1

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    total_update = [[0 for x in range(numberofCluster + 1)] for y in range(numberofCluster + 1)]
    temp = [[0 for x in range(numberofCluster + 1)] for y in range(numberofCluster + 1)]

    for i in range(1, numberofCluster + 1):
        for j in range(1, numberofCluster + 1):
            if minUpdate[i][j] >= 1:
                minUpdate[i][j] = 1

    for i in range(1, numberofCluster + 1):
        for j in range(1, numberofCluster + 1):
            if maxUpdate[i][j] >= 1:
                maxUpdate[i][j] = 1

    for i in range(1, numberofCluster + 1):
        for j in range(1, numberofCluster + 1):
            if i != j:
                total_update[i][j] = minUpdate[i][j] + maxUpdate[i][j]

    total_update_count = 0

    for i in range(1, numberofCluster + 1):
        for j in range(1, numberofCluster + 1):
            total_update_count = total_update_count + total_update[i][j]

    print("total updates:", total_update_count)






