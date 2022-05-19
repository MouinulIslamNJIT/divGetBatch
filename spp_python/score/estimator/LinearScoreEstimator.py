import numpy as np
from ScoreEstimator import ScoreEstimator

class LinearScoreEstimator(ScoreEstimator):
    #LINEARSCOREESTIMATOR Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None): 
        return
        
        
    def train(this = None,scoreSamples = None): 
        rankPosition = scoreSamples(:,np.arange(1,end() - 1+1))
        scores = scoreSamples(:,end())
        linearRegressor = polyfitn(rankPosition,scores,1)
        this.parameters = np.transpose(linearRegressor.Coefficients)
        return
        
        
    def computeScore(this = None,rankPosition = None): 
        numObjects = rankPosition.shape[1-1]
        rankPosition = np.array([rankPosition,np.ones((numObjects,1))])
        scores = rankPosition * this.parameters
        return scores
        
        
    def setParameters(this = None,parameters = None): 
        if parameters.shape[2-1] > 1:
            parameters = np.transpose(parameters)
        
        this.parameters = parameters
        return
        