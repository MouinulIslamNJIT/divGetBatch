
class DataService():
    #DATASERVICE Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,dataServiceDriver = None): 
        if len(varargin) == 1:
            this.accessHistory = AccessHistory()
            this.dataServiceDriver = dataServiceDriver
        
        return
        
        
    def getAccessHistory(this = None): 
        accessHistory = this.accessHistory
        return accessHistory
        
        
    def getObjectsDimensions(this = None): 
        objectsDimensions = this.dataServiceDriver.getFeatureVectorsDimensions()
        return objectsDimensions
        
        
    def getNumObjects(this = None): 
        numObjects = this.dataServiceDriver.getNumFeatureVectors()
        return numObjects
        
        
    def getScore(this = None,Ms = None): 
        score = this.accessHistory.getScore(Ms)
        return score
        
        
    def getSDepth(this = None): 
        sDepth = this.accessHistory.getSDepth()
        return sDepth
        
        
    def getVDepth(this = None,vertex = None): 
        if len(varargin) == 1:
            vDepth = this.accessHistory.getVDepth()
        else:
            vDepth = this.accessHistory.getVDepth(vertex)
        
        return vDepth
        
        
    def getSumDepth(this = None): 
        sumDepth = this.accessHistory.getSumDepth()
        return sumDepth
        
        
    def getLastScore(this = None): 
        lastScore = this.accessHistory.getLastScore()
        return lastScore
        
        
    def accessByScore(this = None,Ms = None): 
        if len(varargin) == 1:
            Ms = 1
        
        if Ms == 0:
            objects = []
            return objects,lastScore
        
        # get timer
        accessTimer = this.accessHistory.getAccessTimer()
        # get objects by score
        accessTimer.start()
        featureVectors,scores = this.dataServiceDriver.accessByScore(this.accessHistory.getSDepth(),Ms)
        accessTimer.stop()
        objects = this.constructObjects(featureVectors,scores)
        if len(objects)==0:
            return objects,lastScore
        
        # update history
        lastScore = scores(end())
        this.accessHistory.incrementSDepth(Ms)
        this.accessHistory.appendScores(scores)
        return objects,lastScore
        
        
    def accessByDistance(this = None,vertex = None,numNearestNeighbors = None): 
        if len(varargin) == 2:
            numNearestNeighbors = 1
        
        # get history + timer
        accessTimer = this.accessHistory.getAccessTimer()
        vDepth = this.accessHistory.getVDepth(vertex)
        # get objects by distance
        accessTimer.start()
        featureVector,score,distancesToVertex = this.dataServiceDriver.accessByDistance(vertex,vDepth,numNearestNeighbors)
        accessTimer.stop()
        object = this.constructObjects(featureVector,score)
        # update history
        this.accessHistory.incrementVDepth(vertex,1)
        return object,distancesToVertex
        
        
    def batchedAccess(this = None,vertices = None,radii = None): 
        # get timer
        accessTimer = this.accessHistory.getAccessTimer()
        # get objects by batched access
        accessTimer.start()
        featureVectors,scores,numObjects = this.dataServiceDriver.batchedAccess(vertices,radii)
        accessTimer.stop()
        objects = this.constructObjects(featureVectors,scores)
        # update history
        this.accessHistory.incrementVBatched(sum(numObjects))
        return objects,numObjects
        
        
    def resetAccessHistory(this = None): 
        this.accessHistory = AccessHistory()
        this.dataServiceDriver.reset()
        return
        
        
    def constructObjects(this = None,featureVectors = None,scores = None): 
        if len(featureVectors)==0:
            objects = []
            return objects
        
        objects = struct('features',num2cell(featureVectors,2),'score',num2cell(scores),'divScore',[])
        return objects
        