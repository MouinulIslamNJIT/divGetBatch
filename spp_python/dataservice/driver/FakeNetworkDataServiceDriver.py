
class FakeNetworkDataServiceDriver():
    #FAKENETWORKDATASERVICEDRIVER Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,accessTime = None,filesystemDataServiceDriver = None): 
        if len(varargin) == 2:
            pause('on')
            this.accessTime = accessTime
            this.filesystemDataServiceDriver = filesystemDataServiceDriver
        
        return
        
        
    def getNumFeatureVectors(this = None): 
        numFeatureVectors = this.filesystemDataServiceDriver.getNumFeatureVectors()
        return numFeatureVectors
        
        
    def accessByScore(this = None,sDepth = None,Ms = None): 
        objects,scores = this.filesystemDataServiceDriver.accessByScore(sDepth,Ms)
        pause(this.accessTime)
        return objects,scores
        
        
    def batchedAccess(this = None,vertices = None,radii = None): 
        objects,scores,numObjects = this.filesystemDataServiceDriver.batchedAccess(vertices,radii)
        pause(this.accessTime)
        return objects,scores,numObjects
        
        
    def accessByDistance(this = None,vertex = None,vDepth = None,numNearestNeighbors = None): 
        objects,scores,distancesToVertex = this.filesystemDataServiceDriver.accessByDistance(vertex,vDepth,numNearestNeighbors)
        pause(this.accessTime)
        return objects,scores,distancesToVertex
        
        
    def getFeatureVectorsDimensions(this = None): 
        featureVectorsDimensions = this.filesystemDataServiceDriver.getFeatureVectorsDimensions()
        return featureVectorsDimensions
        
        
    def reset(this = None): 
        return
        