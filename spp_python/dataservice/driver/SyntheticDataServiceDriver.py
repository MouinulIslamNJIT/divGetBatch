import numpy as np
import numpy.matlib

class SyntheticDataServiceDriver():
    #SYNTETHICDATASERVICEDRIVER Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,featureVectors = None,scores = None,rankingPolicy = None): 
        if len(varargin) <= 2:
            rankingPolicy = 'descend'
        
        if len(varargin) >= 2:
            featureVectors,scores = this.orderByQueryRelevance(featureVectors,scores,rankingPolicy)
            this.featureVectorsDimensions = featureVectors.shape[2-1]
            this.featureVectors = featureVectors
            this.scores = scores
            this.numFeatureVectors = featureVectors.shape[1-1]
            this.tree = kdtree_build(this.featureVectors)
        
        return
        
        
    def getNumFeatureVectors(this = None): 
        numFeatureVectors = this.numFeatureVectors
        return numFeatureVectors
        
        
    def getFeatureVectorsDimensions(this = None): 
        featureVectorsDimensions = this.featureVectorsDimensions
        return featureVectorsDimensions
        
        
    def accessByScore(this = None,sDepth = None,Ms = None): 
        if sDepth >= this.numFeatureVectors:
            featureVectors = []
            scores = []
            return featureVectors,scores
        
        if sDepth + Ms <= this.numFeatureVectors:
            featureVectors = this.featureVectors(np.arange(sDepth + 1,sDepth + Ms+1),:)
            scores = this.scores(np.arange(sDepth + 1,sDepth + Ms+1))
        else:
            featureVectors = this.featureVectors(np.arange(sDepth + 1,end()+1),:)
            scores = this.scores(np.arange(sDepth + 1,end()+1))
        
        return featureVectors,scores
        
        
    def accessByDistance(this = None,vertex = None,vDepth = None,numNearestNeighbors = None): 
        neighborsIds = kdtree_k_nearest_neighbors(this.tree,vertex,vDepth + numNearestNeighbors)
        neighborsIds = flipud(neighborsIds)
        featureVector = this.featureVectors(neighborsIds(end()),:)
        score = this.scores(neighborsIds(end()))
        distancesToVertex = np.sqrt(sum((featureVector - vertex) ** 2))
        return featureVector,score,distancesToVertex
        
        
    def batchedAccess(this = None,vertices = None,radii = None): 
        numVertices = vertices.shape[1-1]
        numObjects = NaN * np.ones((numVertices,1))
        featureVectorsIds = []
        for vertexId in np.arange(1,numVertices+1).reshape(-1):
            distancesToVertex = np.sqrt(np.sum((this.featureVectors - np.matlib.repmat(vertices(vertexId,:),this.featureVectors.shape[1-1],1)) ** 2, 2-1))
            neighborsIds = np.transpose(find(distancesToVertex < radii(vertexId)))
            numObjects[vertexId] = len(neighborsIds)
            featureVectorsIds = np.array([featureVectorsIds,neighborsIds])
        
        featureVectorsIds = unique(featureVectorsIds)
        featureVectors = this.featureVectors(featureVectorsIds,:)
        scores = this.scores(featureVectorsIds,:)
        return featureVectors,scores,numObjects
        
        
    def reset(this = None): 
        return
        
        
    def orderByQueryRelevance(this = None,featureVectors = None,scores = None,rankingPolicy = None): 
        scores,scoresIds = __builtint__.sorted(scores,rankingPolicy)
        featureVectors = featureVectors(scoresIds,:)
        if str(rankingPolicy) == str('ascend'):
            scores = 1 - scores
        
        return featureVectors,scores
        