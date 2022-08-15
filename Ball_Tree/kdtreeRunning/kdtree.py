# -*- coding: utf-8 -*-
"""kdTreeTest.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q9r32scvmIqM0q1wlO1OhENWjIACz1A4
"""

import pandas as pd
import numpy as np
import math
from scipy.spatial import distance
import scipy

import math
import numpy as np

class kdTree_node:
    
    def __init__(self, x, y, split_along_x=True,height=0,nodeId=0):
        self.x = x
        self.y = y
        self.xmax = math.inf
        self.ymax = math.inf
        self.xmin = -math.inf
        self.ymin = -math.inf
        self.split_along_x = split_along_x
        self.left = None
        self.right = None
        self.points = []
        self.height = height
        self.id = nodeId
        
    def __str__(self):
        return "(x="+str(self.x)+",y="+str(self.y)+")"



class kdTree:
    def __init__(self, xs, ys,h):
        h = h+1
        i_x_sort = np.argsort(xs)
        i_y_sort = np.argsort(ys)
        self.h = h
        self.nodeIdList = []
        for i in range(2**h):
             self.nodeIdList.append(0)
        self.documentMap = {}   
        self.eps = 0.001
        for i in range(len(xs)):
            d = [xs[i],ys[i]]
            self.documentMap[tuple(d)] = np.zeros(self.h+1, dtype=int)
            
        self.indexMap = {}
        index = 0
        for e in range(0,len(xs)):
            self.indexMap[tuple([xs[e],ys[e]])] = index
            index = index + 1
        
        self.root = self.__buildTree(xs, ys, i_x_sort, i_y_sort, True,None,0)
        
        
        
    def print(self):
        self.__printSubtree(self.root)
        
    def __printSubtree(self, node):
        if node.left!=None:
            self.__printSubtree(node.left)
        print(node)
        if node.right!=None:
            self.__printSubtree(node.right)
    
    def __select(self, isorted, isecond):
        iy = np.array([]).astype(int)
        for i in isecond:
            r = (isorted==i)
            if r.any()==True:
                iy=np.append(iy,i)
        return iy
    
    def __buildTree(self, xs, ys, ix, iy, splitx=None, father=None,height=0):
        l = ix.shape[0]
        med = l//2
        
        if height == self.h:
            return None
        self.nodeIdList[height] = self.nodeIdList[height] + 1
        # Split along the xaxis
        if splitx:
            n = kdTree_node(xs[ix[med]], ys[ix[med]], True,height,self.nodeIdList[height])
            if father != None:
                
                n.xmin = father.xmin
                n.xmax = father.xmax
                n.ymin = father.ymin
                n.ymax = father.ymax
                
                if n.y <= father.y:
                    n.ymax = father.y  +  self.eps
                    
                else:
                    n.ymin = father.y +  self.eps

            for i in range(0, len(xs)):
                if xs[i] >= n.xmin and xs[i] <= n.xmax and ys[i] >= n.ymin and ys[i] <= n.ymax:
                    d = [xs[i], ys[i]]
                    self.documentMap[tuple(d)][height] = self.nodeIdList[height]
                    n.points.append(d)

            # if faterLst != None and father != None:
            #     d = [father.x, father.y]
            #     faterLst.append(d)
            #     for d in faterLst:
            #         self.documentMap[tuple(d)][height] = self.nodeIdList[height]
            #         n.points.append(d)
            

            
            if med > 0:
                sub_iy = self.__select(ix[:med],iy)
                n.left = self.__buildTree(xs, ys, ix[:med], sub_iy, False, n,n.height+1)
            if med+1<l:
                sub_iy = self.__select(ix[med+1:], iy)
                n.right = self.__buildTree(xs, ys, ix[med+1:], sub_iy, False, n,n.height+1)
            
        # This node corresponds to a split of the data along y
        else:
            n = kdTree_node(xs[iy[med]], ys[iy[med]], False,height,self.nodeIdList[height])
            if father != None:

                n.xmin = father.xmin
                n.xmax = father.xmax
                n.ymin = father.ymin
                n.ymax = father.ymax

                if n.x < father.x:
                    n.xmax = father.x +  self.eps

                else:
                    n.xmin = father.x +  self.eps


            for i in range(0, len(xs)):
                if xs[i] >= n.xmin and xs[i] <= n.xmax and ys[i] >= n.ymin and ys[i] <= n.ymax:
                    d = [xs[i], ys[i]]
                    self.documentMap[tuple(d)][height] = self.nodeIdList[height]
                    n.points.append(d)


            # if faterLst != None and father != None:
            #     d = [father.x, father.y]
            #     faterLst.append(d)
            #     for d in faterLst:
            #         self.documentMap[tuple(d)][height] = self.nodeIdList[height]
            #         n.points.append(d)


            if med > 0:
                sub_ix = self.__select(iy[:med],ix)
                n.left = self.__buildTree(xs, ys, sub_ix, iy[:med], True, n,n.height+1)
            if med+1<l:
                sub_ix = self.__select(iy[med+1:], ix)
                n.right = self.__buildTree(xs, ys, sub_ix, iy[med+1:], True, n,n.height+1)
                
       
        
        return n 
    
    def is_fully_contained(self, node, r):
        if node:
            if r['xmin'] <= node.xmin and r['xmax'] >= node.xmax and r['ymin'] <= node.ymin and r['ymax'] >= node.ymax:
                return True
        return False
    
    def is_intersect(self, node, r):
        if node:
            if r['ymin'] > node.ymax or r['ymax'] < node.ymin or r['xmin'] > node.xmax or r['xmax'] < node.xmin:
                return False
        return True
    
    def range_search(self, node, r):
       
        results = []
        if node == None:
            return results
        if node.left == None and node.right == None:
            
            if r['xmin'] <= node.x and r['xmax'] >= node.x and r['ymin'] <= node.y and r['ymax'] >= node.y:
                results.append(node)
         
        else:
            if r['xmin'] <= node.x and r['xmax'] >= node.x and r['ymin'] <= node.y and r['ymax'] >= node.y:
                results.append(node)
                
            if self.is_fully_contained(node.left, r):
                results += self.traverse(node.left)
            
            elif self.is_intersect(node.left, r):
                results += self.range_search(node.left, r)
            
            if self.is_fully_contained(node.right, r):
                results += self.traverse(node.right)
                
            elif self.is_intersect(node.right, r):
                results += self.range_search(node.right, r)
               
        return results

    def traverse(self, node):
        members = []
        if node:
            members += self.traverse(node.left)
            members.append(node)
            members += self.traverse(node.right)
        return members
        
        
        
    def createLevelMatrix(self,nodes,height):
        nodeId = []
        height = height +1
        for i in range(0,len(nodes)):
            nodeId.append(-1)
            levelMatrix = np.empty(
                shape=(height + 1, 2 ** height + 1), dtype=kdTree_node)
        for i in range(0,len(nodes)):
            levelMatrix[nodes[i].height][nodes[i].id] = nodes[i]
        
        return levelMatrix



    def createDistanceMatrix(self,levelMatrix,height):
        dismatrix = np.empty(
            shape=(height + 1, 2 ** height + 1,
                2 ** height + 1),
            dtype=tuple)
        for l in range(1,height+1):
            for i in range(1,2**l+1 ):
                for j in range(1,2**l+1 ):
                    if levelMatrix[l][i] == None or levelMatrix[l][j] == None:
                        return dismatrix
                    dismatrix[l, i, j] = self.min_max_distance(levelMatrix[l][i].points, levelMatrix[l][j].points)
                    #print(l,i,j,dismatrix[l,i,j])
        return dismatrix

    def min_max_distance(self,cluster1, cluster2):
        #start = timeit.default_timer()
        if len(cluster1)  == 0 or len(cluster2)  == 0:
            return 0,0
        Z =distance.cdist(cluster1, cluster2, 'euclidean')
        #print(Z.min()**2,Z.max()**2)
        #stop = timeit.default_timer()
        #print('Time for mmr: ', stop - start)

        return Z.min()**2,Z.max()**2


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
        return mindis,maxdis





def latlngToGlobalXY(coords):
    radius = 6371.0
    dlon = math.pi*(coords[0]-lonMean)/180.0
    dlat = math.pi*(coords[1]-latMean)/180.0
    x = radius*dlon*math.cos(math.pi*latMean/180.0)
    y = radius*dlat
    return x,y
 
''' 
df_s = pd.read_json('estaciones.json', orient='columns')
stations_positions = df_s[['lon','lat']].values.reshape(-1,2)
lonMean = np.average(stations_positions[:,0])
latMean = np.average(stations_positions[:,1])
locs_bici = np.apply_along_axis(latlngToGlobalXY, 1, stations_positions)
X = locs_bici[:,0]
Y = locs_bici[:,1]
'''



#height = 4
#kdt = kdTree(X,Y,height)

#nodes = kdt.traverse(kdt.root)

#nodes







