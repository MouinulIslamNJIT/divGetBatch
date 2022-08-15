import pandas as pd
import numpy as np
import math
from scipy.spatial import distance
import scipy



class BallTree_node:

    def __init__(self, data,height=0,nodeId=0):
        self.data = np.asarray(data)

        # data should be two-dimensional
        assert self.data.shape[1] == 2

        self.loc = data.mean(0)
        self.radius = np.sqrt(np.max(np.sum((self.data - self.loc) ** 2, 1)))

        self.left = None
        self.right = None
        self.points = []
        self.height = 0
        self.id = 0

        self.left = None
        self.right = None
        self.points = []
        self.height = height
        self.id = nodeId
        self.parent = None



    def __str__(self):
        return "(x=" + str(self.x) + ",y=" + str(self.y) + ")"


class BallTree:
    """Simple Ball tree class"""

    # class initialization function
    def __init__(self, data,h):
        self.data = np.asarray(data)

        h = h + 1

        self.h = h
        self.nodeIdList = []
        for i in range(2 ** h):
            self.nodeIdList.append(0)
        self.documentMap = {}
        self.eps = 0.001
        for e in data:
            self.documentMap[tuple(e)] = np.zeros(self.h + 1, dtype=int)

        self.indexMap = {}
        index = 0
        for e in data:
            self.indexMap[tuple(e)] = index
            index = index + 1





        self.root = self.__buildTree(data, 0)


    def __buildTree(self, data,  father=None, height=0):
        #print(len(data))
        if height == self.h:
            return None

        self.nodeIdList[height] = self.nodeIdList[height] + 1


        if len(data) > 1:
            # sort on the dimension with the largest spread
            n = BallTree_node(data)
            n.points = data
            n.height = height
            n.id = self.nodeIdList[height]
            n.parent = father

            largest_dim = np.argmax(data.max(0) - data.min(0))
            i_sort = np.argsort(data[:, largest_dim])
            data[:] = data[i_sort, :]

            # find split point
            N = data.shape[0]
            half_N = int(N / 2)
            split_point = 0.5 * (data[half_N, largest_dim]
                                 + data[half_N - 1, largest_dim])

            for d in data:
                self.documentMap[tuple(d)][height] = self.nodeIdList[height]
                np.append(n.points,d)


            # recursively create subnodes
            n.left = self.__buildTree(data[half_N:],n, n.height + 1)
            n.right = self.__buildTree(data[:half_N], n, n.height + 1)
            return n
        return None



    def traverse(self, node):
        members = []
        if node:
            members += self.traverse(node.left)
            members.append(node)
            members += self.traverse(node.right)
        return members

    def createLevelMatrix(self, nodes, height):
        nodeId = []
        height = height + 1
        for i in range(0, len(nodes)):
            nodeId.append(-1)
            levelMatrix = np.empty(
                shape=(height + 1, 2 ** height + 1), dtype=BallTree_node)
        for i in range(0, len(nodes)):
            levelMatrix[nodes[i].height][nodes[i].id] = nodes[i]

        return levelMatrix

    def createDistanceMatrix(self, levelMatrix, height):
        dismatrix = np.empty(
            shape=(height + 1, 2 ** height + 1,
                   2 ** height + 1),
            dtype=tuple)
        for l in range(1, height + 1):
            for i in range(1, 2 ** l + 1):
                for j in range(1, 2 ** l + 1):
                    if levelMatrix[l][i] == None or levelMatrix[l][j] == None:
                        return dismatrix
                    dismatrix[l, i, j] = self.min_max_distance(levelMatrix[l][i].points, levelMatrix[l][j].points)
                    # print(l,i,j,dismatrix[l,i,j])
        return dismatrix

    def min_max_distance(self, cluster1, cluster2):
        # start = timeit.default_timer()
        if len(cluster1) == 0 or len(cluster2) == 0:
            return 0, 0
        Z = distance.cdist(cluster1, cluster2, 'euclidean')
        # print(Z.min()**2,Z.max()**2)
        # stop = timeit.default_timer()
        # print('Time for mmr: ', stop - start)

        return Z.min() ** 2, Z.max() ** 2

        mindis = float('inf')
        maxdis = -1
        for i in cluster1:
            for j in cluster2:
                dis = distance_euclidean(i, j)
                if mindis > dis:
                    mindis = dis
                    item = (i, j)
                if maxdis < dis:
                    maxdis = dis
        return mindis, maxdis
