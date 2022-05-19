import numpy as np
from DensitySampler import DensitySampler

class DensitySampler3D(DensitySampler):
    #DENSITYSAMPLER3D Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,dataService = None): 
        if len(dataService)==0:
            dataService = 0
        
        # TODO TODO TODO MATLAB2PYTHON: this@DensitySampler(dataService);
        return
        
        
    def computeArea(this = None,radius = None): 
        area = (4 / 3) * pi * radius ** 3
        return area
        
        
    def computeNumProbingLocations(this = None,numQuadrants = None): 
        numProbingLocations = (numQuadrants + 1) ** 3
        return numProbingLocations
        
        
    def computeInitialDensityRadius(this = None,numProbingLocations = None,areaPercentage = None): 
        radius = (np.multiply(areaPercentage,3.0) / (np.multiply(4.0 * pi,numProbingLocations))) ** (1 / 3)
        return radius
        
        
    def sample(this = None,boundingRegion = None,radius = None,numQuadrants = None): 
        lowerBound = boundingRegion.lowerBound
        upperBound = boundingRegion.upperBound
        step = (upperBound - lowerBound) / numQuadrants
        X,Y,Z = np.meshgrid(np.arange(lowerBound,upperBound+step,step),np.arange(lowerBound,upperBound+step,step),np.arange(lowerBound,upperBound+step,step))
        probingLocations = np.array([X,Y,Z])
        numProbingLocations = probingLocations.shape[1-1]
        probingLocationsIds = np.arange(1,numProbingLocations+1)
        estimatedDensity = NaN * np.ones((numProbingLocations,1))
        while not len(probingLocationsIds)==0 :
    
            __,numObjects = this.dataService.batchedAccess(probingLocations(probingLocationsIds,:),radius * np.ones((len(probingLocationsIds),1)))
            area = this.computeArea(radius)
            estimatedDensity[probingLocationsIds] = numObjects / area
            probingLocationsIds = probingLocationsIds(estimatedDensity(probingLocationsIds) == 0)
            radius = radius * this.INCREASE_RATE
    
        
        samples = np.array([X,Y,Z,estimatedDensity])
        return samples
        