import numpy as np
    
def SPP(dataService = None,lambda_ = None,K = None,boundingRegion = None,retrievalMethod = None,densityEstimator = None): 
    seenObjects = []
    resultSet = struct('features',cell(K,1),'score',cell(K,1),'divScore',cell(K,1))
    totalTimer = TimerFactory.newInstance()
    # top-1 by score
    totalTimer.start()
    resultSet[1] = dataService.accessByScore()
    seenObjects = resultSet(1)
    totalTimer.stop()
    # voronoi diagram
    createVoronoiDiagram = VoronoiDiagramFactory.newInstance(dataService)
    totalTimer.start()
    for k in np.arange(2,K+1).reshape(-1):
        # build voronoi diagram
        centroids = resultSet(np.arange(1,k - 1+1))
        voronoiDiagram = createVoronoiDiagram(centroids,boundingRegion,k)
        # retrieve method
        resultSet[k],seenObjects = retrievalMethod(dataService,voronoiDiagram,seenObjects,lambda_,densityEstimator)
    
    totalTimer.stop()
    return resultSet,totalTimer
    
    return resultSet,totalTimer