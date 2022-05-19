import numpy as np
from DensityEstimator import DensityEstimator

class DensityUniformEstimator(DensityEstimator):
    #DENSITYUNIFORMESTIMATOR Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,uniformDensity = None): 
        if len(varargin) == 1:
            this.uniformDensity = uniformDensity
        
        return
        
        
    def train(this = None,__ = None,__ = None): 
        throw(MException('DensityUniformEstimator:train','operation not supported'))
        return
        
        
    def estimate(this = None,point = None): 
        numPoints = point.shape[1-1]
        estimatedDensity = this.uniformDensity * np.ones((numPoints,1))
        return estimatedDensity
        