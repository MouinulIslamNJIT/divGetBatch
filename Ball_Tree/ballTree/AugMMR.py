from Utils import similarity
from distance import min_max_distance
import numpy as np


def CalculateBound(ballTree,level,arity,q,lambda_score,S,simmap,indexMap,candNodes,levelMatrix,dismatrix):
    lastItem = None
    if len(S) != 0:
        lastItem = S[-1]

    lbMMRList = []
    ubMMRList = []


    for node in candNodes:

        if lastItem is not None:
            #########cluster to iTree distance##########
            
          
            recordId = ballTree.documentMap[tuple(lastItem)][level]
            
            
            mincdis, maxcdis = dismatrix[level][recordId][node.id]

            # ######### item to iTree distance ############
            # recordId = indexMap[tuple(lastItem)]
            # mincdis, maxcdis = iTree.dismatrixitem[level][recordId][node.id]

            sim_current_max = 1 / (1 + mincdis)
            sim_current_min = 1 / (1 + maxcdis)

            if sim_current_max < simmap[(node.id,level)][1]:
                sim_current_max = simmap[(node.id,level)][1]
            if sim_current_min > simmap[(node.id,level)][0]:
                sim_current_min = simmap[(node.id,level)][0]
            simmap[(node.id, level)] = (sim_current_min,sim_current_max)

        mindis,maxdis = min_max_distance([q], node.points)

        relmax = 1 / (1 + mindis)
        relmin = 1 / (1 + maxdis)

        lbMMR = 0
        ubMMR = 0
        if lastItem is None:
            lbMMR = lambda_score * relmin
            ubMMR = lambda_score * relmax
        else:
            lbMMR = lambda_score * relmin - (1 - lambda_score) * simmap[(node.id,level)][1]
            ubMMR = lambda_score * relmax - (1 - lambda_score) * simmap[(node.id,level)][0]


        lbMMRList.append(lbMMR)
        ubMMRList.append(ubMMR)


    return  (lbMMRList,ubMMRList)



def skipNodes(lbMMRList,ubMMRList,candNodes):
    maxofMin = max(lbMMRList)
    remainCluster = []
    i = 0

    for it in ubMMRList:
        if it >= maxofMin:

            if (candNodes[i].left == None or candNodes[i].right == None):
                remainCluster.append(candNodes[i])
            else:
                remainCluster.append(candNodes[i].right)
                remainCluster.append(candNodes[i].left)
        i = i + 1
    candNodes = remainCluster
    return candNodes


def DivGetBatch(ballTree,L,arity,q,lambda_score,S,simmap,indexMap,levelMatrix,dismatrix):
    candNodes = [ballTree.root.left,ballTree.root.right]

    for level in range(1,L+1):
        lbMMRList, ubMMRList = CalculateBound(ballTree,level,arity,q,lambda_score,S,simmap,indexMap,candNodes,levelMatrix,dismatrix) #calculateBound(iTree,C,indexMap,iTreeArray,l)
        candNodes = skipNodes(lbMMRList,ubMMRList,candNodes)
    candR = []

    for node in candNodes:
        candR.extend(node.points)

    # result = []
    # [result.append(x) for x in candR if x not in result]
    #
    # if len(candR) != len(result):
    #     print("diff")
    print("number of returned items by DivGetBatch: ", len(candR))
    return candR



def AugMMR(ballTree,L,arity,q,lambda_score,k,indexMap):
    nodes = ballTree.traverse(ballTree.root)

    levelMatrix = ballTree.createLevelMatrix(nodes, L + 1)
    dismatrix = ballTree.createDistanceMatrix(levelMatrix, L + 1)

    S = []
    simmap = {}

    for level in range(1, L+1):
        for nodeId in range(1, arity ** level + 1):
            node = levelMatrix[level][nodeId]
            simmap[(node.id, level)] = (1000000, -100000)



    for i in range (k):
        mmr = -100000000
        candR = DivGetBatch(ballTree,L,arity,q,lambda_score,S,simmap,indexMap,levelMatrix,dismatrix)

        for item in S:
            if np.where(candR == item) == True:
                candR.remove(item)


        nextBest = None

        for d in candR:
            sim = 0
            for s in S:
                if similarity(d, s) == 0:
                    continue
                sim_current = similarity(d, s)
                if sim_current > sim:
                    sim = sim_current
                else:
                    continue

            rel = similarity(q, d)
            mmr_current = lambda_score * rel - (1 - lambda_score) * sim

            if mmr_current > mmr:
                mmr = mmr_current
                nextBest = d
            else:
                continue

        S.append(nextBest)
    print(S)
    return S




