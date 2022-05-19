import numpy as np
from DensitySampler import DensitySampler

class DensitySampler2D(DensitySampler):
    #BOUNDINGREGIONSAMPLER2D Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,dataService = None): 
        if len(dataService)==0:
            dataService = 0
        
        # TODO TODO TODO MATLAB2PYTHON: this@DensitySampler(dataService);
        return
        
        
    def computeArea(this = None,radius = None): 
        area = radius ** 2 * pi
        return area
        
        
    def computeNumProbingLocations(this = None,numQuadrants = None): 
        numProbingLocations = (numQuadrants + 1) ** 2
        return numProbingLocations
        
        
    def computeInitialDensityRadius(this = None,numProbingLocations = None,areaPercentage = None): 
        radius = np.sqrt(areaPercentage / (numProbingLocations * pi))
        return radius
        
        
    def sample(this = None,boundingRegion = None,radius = None,numQuadrants = None): 
        lowerBound = boundingRegion.lowerBound
        upperBound = boundingRegion.upperBound
        step = (upperBound - lowerBound) / numQuadrants
        X,Y = np.meshgrid(np.array([np.arange(lowerBound,upperBound+step,step)]),np.transpose(np.array([np.arange(lowerBound,upperBound+step,step)])))
        probingLocations = np.array([X,Y])
        numProbingLocations = probingLocations.shape[1-1]
        probingLocationsIds = np.arange(1,numProbingLocations+1)
        estimatedDensity = NaN * np.ones((numProbingLocations,1))
        while not len(probingLocationsIds)==0 :
    
            __,numObjects = this.dataService.batchedAccess(probingLocations(probingLocationsIds,:),radius * np.ones((len(probingLocationsIds),1)))
            area = this.computeArea(radius)
            estimatedDensity[probingLocationsIds] = numObjects / area
            probingLocationsIds = probingLocationsIds(estimatedDensity(probingLocationsIds) == 0)
            radius = radius * this.INCREASE_RATE
    
        
        samples = np.array([X,Y,estimatedDensity])
        return samples
        