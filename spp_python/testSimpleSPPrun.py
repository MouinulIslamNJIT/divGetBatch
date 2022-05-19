import numpy as np
import matplotlib.pyplot as plt
    
def testSimpleSPPrun(): 
    K = 2
    gradratio = 1
    N = 4
    lambda_ = 0.75
    seed = 1
    rng(seed)
    S_MAX = 1
    # bounding region
    boundingRegion = struct('upperBound',0.5,'lowerBound',- 0.5)
    # generate data set
    featureVectors = np.array([[- 0.4,- 0.4],[- 0.2,0.4],[0.45,0.2],[0.3,- 0.3]])
    scores = np.array([1,0.9,0.8,0.7])
    scatter(featureVectors(:,1),featureVectors(:,2))
    plt.ylim(np.array([- 0.5,0.5]))
    plt.xlim(np.array([- 0.5,0.5]))
    # create data service
    dataService = DataService(SyntheticDataServiceDriver(featureVectors,scores,'descend'))
    # density
    densityEstimator = DensityEstimatorFactory.newInstance('uniform',dataService,boundingRegion)
    # retrieval method
    retrievalMethod = RetrievalMethodFactory.newInstance('PA-SB',gradratio)
    # SPP
    resultSet,__ = SPP(dataService,lambda_,K,boundingRegion,retrievalMethod,densityEstimator)
    return resultSet
    
    return resultSet