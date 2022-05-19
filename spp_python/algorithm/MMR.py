import numpy as np
    
def MMR(dataService = None,K = None,lambda_ = None): 
    resultSet = struct('features',cell(K,1),'score',cell(K,1),'divScore',cell(K,1))
    CPUTimer = TimerFactory.newInstance()
    # Retrieve dataset
    dataSet = []
    while 1:

        newObject = dataService.accessByScore()
        if len(newObject)==0:
            break
        dataSet = np.array([[dataSet],[newObject]])

    
    N = dataSet.shape[1-1]
    # Top-1 by score
    CPUTimer.start()
    resultSet[1] = dataSet(1)
    for k in np.arange(2,K+1).reshape(-1):
        resultSetFeatures = vertcat(resultSet.features)
        dataSetFeatures = vertcat(dataSet.features)
        __,resultSetIdxs = ismember(resultSetFeatures,dataSetFeatures,'rows')
        otherObjects = dataSet(setdiff(np.arange(1,N+1),resultSetIdxs))
        otherObjectsFeatures = vertcat(otherObjects.features)
        __,maxDist = kNearestNeighbors(resultSetFeatures,otherObjectsFeatures,1)
        score = (1 - lambda_) * vertcat(otherObjects.score) + lambda_ * maxDist
        __,idx = np.amax(score)
        resultSet[k] = otherObjects(idx)
    
    CPUTimer.stop()
    return resultSet,CPUTimer
    
    return resultSet,CPUTimer