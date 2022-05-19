import numpy as np
    
def pullingStrategy(dataService = None,voronoiDiagram = None,seenObjects = None,lambda_ = None,densityEstimator = None,pullingStrategyName = None,varargin = None): 
    ## Variables
    VGRADS_THR = 1e-06
    V = voronoiDiagram.vertices.coordinates
    VtoV = voronoiDiagram.topology
    centroidsFeatures = vertcat(voronoiDiagram.centroids.features)
    Vdist = voronoiDiagram.vertices.distancesFromCentroids
    S_last = dataService.getLastScore()
    Vtau = (1 - lambda_) * S_last + lambda_ * Vdist
    Vtau[isinf[V]] = NaN
    Vgrad = NaN * np.ones((V.shape[1-1],1))
    distance_to_vertex = np.zeros((V.shape[1-1],1))
    v = 0
    top2 = []
    if len(varargin) >= 1:
        gradratio = varargin[0]
    else:
        gradratio = 1
    
    # compute div score for seen objects
    seenObjects = computeDivScore(seenObjects,voronoiDiagram.centroids,lambda_)
    ## SPP core
    while 1:

        VgradS = NaN
        if 'PA-SB' == pullingStrategyName:
            __,v = np.amax(Vtau)
            if dataService.getSDepth() > 1:
                VgradS = dataService.getScore(dataService.getSDepth()) - dataService.getScore(dataService.getSDepth() - 1)
                if np.abs(VgradS) < VGRADS_THR:
                    VgradS = - VGRADS_THR
            else:
                top2,top2Score = dataService.accessByScore()
                VgradS = top2Score - dataService.getScore(1)
            nextScore = ((1 - lambda_) * VgradS) / (lambda_ * Vgrad(v)) > gradratio
        else:
            if 'PA' == pullingStrategyName:
                __,v = np.amax(Vtau)
                nextScore = ((1 - lambda_) * VgradS) / (lambda_ * Vgrad(v)) > gradratio
            else:
                if 'RR' == pullingStrategyName:
                    N_vert = V.shape[1-1]
                    if np.mod(dataService.getSumDepth(),N_vert + 1) == 0:
                        nextScore = 1
                        v = 1
                    else:
                        nextScore = 0
                        if v == N_vert:
                            v = 1
                        else:
                            v = v + 1
                else:
                    raise Exception('ERROR: invalid pulling strategy')
        if nextScore:
            if not len(top2)==0 :
                next_obj = top2
                S_last = top2Score
                top2 = []
            else:
                next_obj,S_last = dataService.accessByScore()
        else:
            next_obj,distance_to_vertex[v] = dataService.accessByDistance(V(v,:))
        # compute div score + add new object
        next_obj = computeDivScore(next_obj,voronoiDiagram.centroids,lambda_)
        if len(seenObjects) == 1:
            seenObjects = np.array([[seenObjects],[next_obj]])
        else:
            if not ismember(vertcat(next_obj.features),vertcat(seenObjects.features),'rows') :
                seenObjects = np.array([[seenObjects],[next_obj]])
        # update bound
        rho = densityEstimator.estimate(V)
        Vdepth = dataService.getVDepth(V(v,:))
        Vtau[v],Vgrad[v] = bounding_scheme(VtoV[v],V(v,:),V,distance_to_vertex(v),centroidsFeatures,S_last,lambda_,rho(v),Vdepth)
        # find best object
        bestObjectDivScore,bestObjectId = np.amax(vertcat(seenObjects.divScore))
        bestObject = seenObjects(bestObjectId)
        # exit strategy
        if bestObjectDivScore >= np.amax(Vtau):
            break

    
    return bestObject,seenObjects
    
    return bestObject,seenObjects