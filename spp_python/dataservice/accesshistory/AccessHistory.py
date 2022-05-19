import numpy as np

class AccessHistory():
    #ACCESSHISTORY Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None): 
        this.TOLERANCE = 1.5 * eps
        this.accessesByDistanceHistory = struct('coordinates',[],'vDepth',[])
        this.sDepth = 0
        this.vBatched = 0
        this.lastScore = + Inf
        this.scores = []
        this.accessTimer = TimerFactory.newInstance()
        return
        
        
    def appendScores(this = None,scores = None): 
        this.scores = np.array([[this.scores],[scores]])
        this.lastScore = scores(end())
        return this
        
        
    def getScore(this = None,Ms = None): 
        numSeenScores = len(this.scores)
        if Ms > numSeenScores:
            throw(MException('AccessHistory:getScore','out of bound rank position specified'))
        
        score = this.scores(Ms)
        return score
        
        
    def getLastScore(this = None): 
        lastScore = this.lastScore
        return lastScore
        
        
    def getSDepth(this = None): 
        sDepth = this.sDepth
        return sDepth
        
        
    def getVBatched(this = None): 
        vBatched = this.vBatched
        return vBatched
        
        
    def getVDepth(this = None,vertex = None): 
        if len(varargin) == 1:
            vertex = this.accessesByDistanceHistory.coordinates
        
        vertexId = this.getVertexIdFromCoordinates(vertex)
        if not len(vertexId)==0 :
            vDepth = this.accessesByDistanceHistory.vDepth(vertexId)
        else:
            vDepth = 0
        
        return vDepth
        
        
    def incrementVBatched(this = None,increment = None): 
        this.vBatched = this.vBatched + increment
        return
        
        
    def incrementVDepth(this = None,vertices = None,increments = None): 
        verticesIds = this.getVertexIdFromCoordinates(vertices)
        if not len(verticesIds)==0 :
            this.accessesByDistanceHistory.vDepth[verticesIds] = this.accessesByDistanceHistory.vDepth(verticesIds) + increments
        else:
            this.accessesByDistanceHistory.coordinates = np.array([[this.accessesByDistanceHistory.coordinates],[vertices]])
            this.accessesByDistanceHistory.vDepth = np.array([[this.accessesByDistanceHistory.vDepth],[increments]])
        
        return
        
        
    def incrementSDepth(this = None,Ms = None): 
        this.sDepth = this.sDepth + Ms
        return
        
        
    def getAccessTimer(this = None): 
        accessTimer = this.accessTimer
        return accessTimer
        
        
    def getSumDepth(this = None): 
        sumDepth = this.sDepth + this.vBatched + sum(this.accessesByDistanceHistory.vDepth)
        return sumDepth
        
        
    def getVertexIdFromCoordinates(this = None,vertex = None): 
        if len(this.accessesByDistanceHistory.coordinates)==0:
            vertexId = []
            return vertexId
        else:
            vertexId = isfuzzymember(vertex,this.accessesByDistanceHistory.coordinates,this.TOLERANCE)
        
        if sum(vertexId) == 0:
            vertexId = []
        
        return vertexId
        