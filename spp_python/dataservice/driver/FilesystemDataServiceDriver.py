import numpy as np

class FilesystemDataServiceDriver():
    #FILESYSTEMDATASERVICEDRIVER Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,csvPath = None,featureVectorsIds = None,scoreId = None,rankingPolicy = None,boundingRegion = None): 
        if len(varargin) >= 4:
            csvData = importdata(csvPath)
            featureVectors = csvData(:,featureVectorsIds)
            scores = csvData(:,scoreId)
            scores[np.isnan[scores]] = 0
            scores = (scores - np.amin(scores)) / (np.amax(scores) - np.amin(scores))
            discardIds = np.isnan(featureVectors(:,1))
            featureVectors = featureVectors(not discardIds ,:)
            scores = scores(not discardIds )
            if len(varargin) == 5:
                featureVectors = this.normalizeData(featureVectors,boundingRegion)
            this.syntheticDataServiceDriver = SyntheticDataServiceDriver(featureVectors,scores,rankingPolicy)
        
        return
        
        
    def getNumFeatureVectors(this = None): 
        numFeatureVectors = this.syntheticDataServiceDriver.getNumFeatureVectors
        return numFeatureVectors
        
        
    def getFeatureVectorsDimensions(this = None): 
        featureVectorsDimensions = this.syntheticDataServiceDriver.getFeatureVectorsDimensions()
        return featureVectorsDimensions
        
        
    def accessByScore(this = None,sDepth = None,Ms = None): 
        featureVectors,scores = this.syntheticDataServiceDriver.accessByScore(sDepth,Ms)
        return featureVectors,scores
        
        
    def accessByDistance(this = None,vertex = None,vDepth = None,numNearestNeighbors = None): 
        featureVector,score,distancesToVertex = this.syntheticDataServiceDriver.accessByDistance(vertex,vDepth,numNearestNeighbors)
        return featureVector,score,distancesToVertex
        
        
    def batchedAccess(this = None,vertices = None,radii = None): 
        featureVectors,scores,numObjects = this.syntheticDataServiceDriver.batchedAccess(vertices,radii)
        return featureVectors,scores,numObjects
        
        
    def reset(this = None): 
        return
        
        
    def normalizeData(this = None,featureVectors = None,boundingRegion = None): 
        numDimensions = featureVectors.shape[2-1]
        for dim in np.arange(1,numDimensions+1).reshape(-1):
            lb = np.amin(featureVectors(:,dim))
            ub = np.amax(featureVectors(:,dim))
            featureVectors[:,dim] = (featureVectors(:,dim) - lb) / (ub - lb)
        
        featureVectors = featureVectors + boundingRegion.lowerBound
        return featureVectors
        