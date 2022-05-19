import numpy as np
    
def computeObjectiveFunction(resultSet = None,lambda_ = None): 
    K = len(resultSet)
    distances = NaN * np.ones((K,1))
    for k in np.arange(1,K+1).reshape(-1):
        currentObject = resultSet(k)
        otherObjects = resultSet(setdiff(np.arange(1,K+1),k))
        __,distances[k] = kNearestNeighbors(vertcat(otherObjects.features),currentObject.features,1)
    
    F = (1 - lambda_) * mean(vertcat(resultSet.score)) + lambda_ * np.amin(distances)
    return F
    
    return F