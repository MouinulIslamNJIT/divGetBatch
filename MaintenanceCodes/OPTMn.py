import gurobipy as gp
from gurobipy import *
from gurobipy import tuplelist
import gurobipy as gp
from gurobipy import *
from gurobipy import tuplelist
import itertools
import random
import math
import numpy
from MaintenanceCodes.distance_final import min_distance, max_distance,min_max_distance, min_disElement, max_disElement
from MaintenanceCodes.clustering_final import Clustering
import random
import timeit
from sklearn.datasets.samples_generator import make_blobs
import pandas as pd
from numpy import asarray
from numpy import savetxt
from Utils.Utils import maintenanceMakeBlob
from Utils.Utils import getMaintenanceData


def euclideanDist(x, y):
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    return distance


def OPTMn():

    numberofCluster = 50

    numberofLevel = 1


    ################################
    #makeblobs data

    center_box = (1, 10000)


    #X,Y = make_blobs(n_samples=10000, centers=500, center_box=center_box, cluster_std=0.6, random_state=1)

    #data = asarray(X)

    # save to csv file
    #savetxt('makeblobs.csv', data, delimiter=',')


    # makeblobs insert
    #10

    #X,Y = make_blobs(n_samples=10, centers=10, center_box=center_box, cluster_std=0.6, random_state=1)

    #data = asarray(X)

    # save to csv file
    #savetxt('makeblobs-10.csv', data, delimiter=',')


    #100

    #X,Y = make_blobs(n_samples=100, centers=10, center_box=center_box, cluster_std=0.6, random_state=1)

    #data = asarray(X)

    # save to csv file
    #savetxt('makeblobs-100.csv', data, delimiter=',')


    #1000
    #X,Y = make_blobs(n_samples=1000, centers=10, center_box=center_box, cluster_std=0.6, random_state=1)

    #data = asarray(X)

    # save to csv file
    #savetxt('makeblobs-1000.csv', data, delimiter=',')



    ################################


    #random dataset


    #mylist = [(random.randint(1, 10000), (random.randint(1, 10000))) for k in range(10000)]

    #print(mylist)

    #data = asarray(mylist)

    # save to csv file
    #savetxt('randomData10k.csv', data, delimiter=',')



    ## 100 random insert

    #
    # insert100 = [(random.randint(1, 1000), (random.randint(1, 1000))) for k in range(100)]


    #
    # data = asarray(insert100)
    # ##save to csv file
    # savetxt('random100.csv', data, delimiter=',')
    #


    ## 1000 random insert
    #
    #insert1000 = [(random.randint(5000, 10000), (random.randint(5000, 10000))) for k in range(1000)]
    #
    #data = asarray(insert1000)
    #save to csv file
    #savetxt('random1000.csv', data, delimiter=',')

    ## 10000 random insert
    #
    # insert10000 = [(random.randint(1, 10000), (random.randint(1, 10000))) for k in range(10000)]
    #
    #
    # data = asarray(insert10000)
    # #save to csv file
    # savetxt('random10000.csv', data, delimiter=',')

    #########################################################
    # read dataset

    path = r'Dataset\MaintenanceDataset\randomData10k.csv'
    df = getMaintenanceData(path)


    X = df.iloc[:,:].values

    #print(X)


    #df = pd.read_csv("makeblobs.csv", header= None)

    #X = df.iloc[:,:].values



    ############ read new data to insert

    #10
    path = r'Dataset\MaintenanceDataset\random10ML.csv'
    df2 = getMaintenanceData(path)


    S = df2.iloc[:, :].values

    #100
    #df2 = pd.read_csv("random100.csv", header= None)
    #S = df2.iloc[:, :].values


    #1000
    #df2 = pd.read_csv("random1000.csv", header= None)
    #S = df2.iloc[:, :].values


    #################
    #10
    #df2 = pd.read_csv("makeblobs-10.csv", header= None)
    #S = df2.iloc[:, :].values

    #100
    #df2 = pd.read_csv("makeblobs-100.csv", header= None)
    #S = df2.iloc[:, :].values
    #print(S)


    #1000
    #df2 = pd.read_csv("makeblobs-10.csv", header= None)
    #S = df2.iloc[:, :].values
    #print(S)


    #print(S)

    ###############################################



    cluster = Clustering(X, numberofCluster, numberofLevel)
    cluster.buildTree(cluster.root)
    cluster.createLevelMatrix(cluster.root)
    simMatrixNode = cluster.createDistanceMatrix(numberofCluster, numberofLevel)
    nodescentroids = cluster.createNodesCentroids(numberofCluster, numberofLevel)
    #print(nodescentroids)


    start = timeit.default_timer()

    Nodes = cluster.createNodes(numberofCluster, numberofLevel)

    ww, hh = numberofCluster, numberofCluster
    minSimMatrix = [[0 for x in range(ww)] for y in range(hh)]
    maxSimMatrix = [[0 for x in range(ww)] for y in range(hh)]


    for i in range (numberofCluster):
        for j in range(numberofCluster):
            minSimMatrix[i][j] = simMatrixNode[1][i+1][j+1][0]
            maxSimMatrix[i][j] = simMatrixNode[1][i+1][j+1][1]


    #print(minSimMatrix)
    #print(maxSimMatrix)

    #########################################
    #S = [(1,0),(1,2),(4,4),(4,2.5),(5,8),(5,10),(3,10),(9.5,5), (9,7), (9,8), (9,9), (9,10), (10,10),
    #     (18,18), (18,19.5), (18,20), (19,21), (20,21), (19,19), (22,22)]
    #S = [(1, 0), (4, 2.5), (9, 5.5)]

    #S = [(1,0),(1,2),(4,4),(4,2.5),(5,8),(5,10),(3,10),(9.5,5), (9,7), (9,8)]

    #S = [(1, 0), (4, 2.5), (9, 5.5), (5,10),(20,21)]   # 5 insert
    #S = [(1,0),(1,2),(4,4),(4,2.5),(5,8),(5,10),(3,10),(9.5,5), (9,7), (9,8)]   # 10 insert


    ######################################

    #experiment

    #S = [(10,10),(150,150)]
    #S = [(1,4),(90,90), (300,300)]
    #S = [(1,4),(90,90), (300,300), (500,500), (800,800)]   # 5 insert experiment
    #S = [(1,4),(90,90), (300,300), (500,500), (800,800), (1000,1000), (1500, 1500), (2000, 2000), (3000,3000), (4000,4000)] # 10 insert

    #S = [(1,4),(4,4),(70,70),(90,90), (150,150),(300,300), (500,500), (800,800), (1000,1000), (1200, 1200),(1500, 1500), (2000, 2000), (3000,3000), (3800,3800),(4000,4000)] # 15 insert


    #S = [(1,4),(4,4),(70,70),(90,90), (150,150),(165,175),(300,300), (490,490),(500,500), (800,800),(950,950), (1000,1000), (1200, 1200),(1500, 1500),(1800,2000), (2000, 2000), (3000,3000), (3800,3800),(4000,4000), (4400, 4200)] # 20 insert

    #S = [(1,4),(90,90), (300,300), (500,500), (800,800), (1000,1000), (1500, 1500), (2000, 2000), (3000,3000), (4000,4000)] # 10 insert


    #S =[(1,0),(1.01,0.01),(4,2.5),(10,5)]

    C = numberofCluster
    N =len(S)
    #N = 5
    #N = 10
    #N = 15
    #N = 20


    w, h = C, N
    mindislist = [[0 for a in range(w)] for b in range(h)]


    def mindis(S, Nodes):
        for item in range(N):
            for key in Nodes.keys():
                min = 1000000000000000000000
                for value in Nodes[key]:
                    d = euclideanDist(S[item], value)**2
                    if min > d:
                        min = d
                mindislist[item][int(key)-1] = min

        return mindislist


    mindis(S, Nodes)

    maxdislist = [[0 for c in range(w)] for d in range(h)]


    def maxdis(S, Nodes):
        for item in range(N):
            for key in Nodes.keys():
                max = -1
                for value in Nodes[key]:
                    d = euclideanDist(S[item], value)**2
                    if max < d:
                        max = d
                maxdislist[item][int(key-1)] = max

        return maxdislist


    maxdis(S, Nodes)



    def cmp(a, b):
        x = 1
        y = 0
        if a > b:
            return x
        if a <= b:
            return y


    w2, l2, r2 = C, C, N

    minT = [[[0 for x2 in range(w2)] for y2 in range(l2)] for u2 in range(r2)]

    for i in range(N):
        for j in range(C):
            for p in range(C):
                if (j != p):
                    minT[i][j][p] = cmp(minSimMatrix[j][p], mindislist[i][p])



    #print(minT)


    maxT = [[[0 for x3 in range(w2)] for y3 in range(l2)] for u3 in range(r2)]

    for i in range(N):
        for j in range(C):
            for p in range(C):
                if (j != p):
                    maxT[i][j][p] = cmp(maxdislist[i][p], maxSimMatrix[j][p])


    # total = [[[0 for x3 in range(w2)] for y3 in range(l2)] for u3 in range(r2)]
    # for i in range(N):
    #     for j in range(C):
    #         for p in range(C):
    #             total[i][j][p] = minT[i][j][p] + maxT[i][j][p]
    #
    #
    # count = [[0 for x3 in range(w2)] for y3 in range(l2)]
    #
    # for i in range(N):
    #     for j in range(C):
    #         number = 0
    #         for p in range(C):
    #             if total[i][j][p] >= 1:
    #                 number = number +1
    #                 count[i][j] = number
    #
    # print("total updates for new items:",count)








    #print(maxT)
    #print("hello")

    E = [[[0 for x2 in range(w2)] for y2 in range(l2)] for u2 in range(r2)]
    D = [[0 for x2 in range(w2)] for u2 in range(r2)]
    for i in range(N):
        for j in range(C):
            for k in range(C):
                E[i][j][k] = maxT[i][j][k] + minT[i][j][k]

    for i in range(N):
        for j in range(C):
            s = 0
            for k in range(C):
                s = s + E[i][j][k]
            D[i][j] = s



    ################################################

    # Declare and initialize model
    m = gp.Model('mymodel')

    Y = m.addVars(N,C,vtype=GRB.BINARY, name="Y")

    z1 = m.addVars(C,C,vtype=GRB.CONTINUOUS,name='z1')
    x1 = m.addVars(C,C,vtype=GRB.BINARY,name='x1')

    z2 = m.addVars(C,C,vtype=GRB.CONTINUOUS,name='z2')
    x2 = m.addVars(C,C,vtype=GRB.BINARY,name='x2')

    for i in range(N):
        m.addConstr((gp.quicksum(Y[i,j] for j in range(C))) == 1)

    for j in range(C):
        for k in range(C):
                m.addConstr(gp.quicksum((Y[i, j] * minT[i][j][k] + Y[i, k] * minT[i][k][j]) for i in range(N)) == z1[j, k])

    for j in range(C):
        for k in range(C):
                m.addConstr(gp.quicksum((Y[i, j] * maxT[i][j][k] + Y[i, k] * maxT[i][k][j]) for i in range(N)) == z2[j, k])

    for i in range(C):
        for j in range(C):
            m.addGenConstrIndicator(x1[i, j], 0, z1[i, j], GRB.LESS_EQUAL, 0.1)
            m.addGenConstrIndicator(x1[i, j], 1, z1[i, j], GRB.GREATER_EQUAL, 0.1)

    for i in range(C):
        for j in range(C):
            m.addGenConstrIndicator(x2[i, j], 0, z2[i, j], GRB.LESS_EQUAL, 0.1)
            m.addGenConstrIndicator(x2[i, j], 1, z2[i, j], GRB.GREATER_EQUAL, 0.1)



    ex = gp.quicksum((x1[i,j]+x2[i,j]) for i in range(C) for j in range(C) if i < j)


    # Set objective
    m.setObjective(ex, GRB.MINIMIZE)
    m.optimize()

    #

    for v in m.getVars():
        #if v.varName.__contains__('Y') and v.x == 1.0:
        print(v.varName, v.x)

    #
    Y2 = [[0 for x3 in range(C)] for y3 in range(N)]

    for v in m.getVars():
        if v.varName.__contains__('Y'):

            #print(v.varName, v.x)
            first = v.varName.find(',')
            end = v.varName.find(']')

            i = v.varName[2:first]
            j = v.varName[first+1:end]
            i2 = int(i)
            j2 = int(j)
            Y2[i2][j2] = v.x


    #print("Y2", Y2[0][30])

    NewItems_Nodes = {}
    for i in range(N):
        for j in range(C):
            if Y2[i][j] == 1:
                NewItems_Nodes[j] = S[i]

    #print(NewItems_Nodes)



    print('Total update:', m.objVal)



    FinalNodes = {}
    for key in set().union(Nodes, NewItems_Nodes):
        if key in Nodes: FinalNodes.setdefault(key, []).extend(Nodes[key])
        if key in NewItems_Nodes: FinalNodes.setdefault(key, []).extend(NewItems_Nodes[key])

    #print(FinalNodes)
    #print(len(Nodes.values()))
    #print(len(FinalNodes.values()))

    #if FinalNodes != Nodes:
    #    print("yes")

    #
    #
    # minUpdate =  [[0 for x in range(numberofCluster+1)] for y in range(numberofCluster+1)]
    # maxUpdate =  [[0 for x in range(numberofCluster+1)] for y in range(numberofCluster+1)]
    # x = 0
    # y = 0
    #
    # nodeID = 0
    # for i in range(len(S)):
    #     for p in range(numberofCluster):
    #         if (Y2[i][p] == 1):
    #             nodeID = p
    #     for  j in range(1,numberofCluster+1):
    #         if (nodeID+1 != j):
    #             #print("nodeID", nodeID)
    #             #print("j", j)
    #             prevmin= simMatrixNode[1][nodeID+1][j][0]
    #             prevmax = simMatrixNode[1][nodeID+1][j][1]
    #             newmin = min_disElement(S[i], Nodes[j])
    #             newmax = max_disElement(S[i], Nodes[j])
    #             if (prevmin > newmin):
    #                 minUpdate[nodeID+1][j] = minUpdate[nodeID+1][j]+ 1
    #
    #             if (prevmax < newmax):
    #                 maxUpdate[nodeID+1][j] = maxUpdate[nodeID+1][j] + 1
    #                 x = i
    #                 y = j
    #
    #                 #print("x", x)
    #                 #print("y" , y)
    #
    #
    #
    #
    # total_update =  [[0 for x in range(numberofCluster+1)] for y in range(numberofCluster+1)]
    # temp =  [[0 for x in range(numberofCluster+1)] for y in range(numberofCluster+1)]
    #
    # for i in range(1, numberofCluster + 1):
    #     for j in range(1, numberofCluster + 1):
    #         if i != j:
    #             temp[i][j] = minUpdate[i][j] + maxUpdate[i][j]
    #
    #
    # #print(temp)
    #
    # for i in range(1, numberofCluster + 1):
    #     for j in range(1, numberofCluster + 1):
    #         if temp[i][j] >= 1:
    #             total_update[i][j] = 1
    #
    #
    # #print("total update matrix:",total_update)
    #
    #
    # total_update_count = 0
    #
    # for i in range(1, numberofCluster + 1):
    #     for j in range(1, numberofCluster + 1):
    #         if total_update[i][j] == 1:
    #             total_update_count = total_update_count +1
    #
    #
    #
    # print("total updates:",total_update_count)
    #







    stop = timeit.default_timer()

    print('Time for IP: ', stop - start)

