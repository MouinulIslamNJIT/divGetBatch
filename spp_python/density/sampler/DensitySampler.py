
class DensitySampler():
    #BOUNDINGREGIONSAMPLER Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,dataService = None): 
        this.INCREASE_RATE = 1.01
        if len(varargin) == 1:
            this.dataService = dataService
        
        return
        
        
    def sampleByDistance(this = None,boundingRegion = None,areaPercentage = None,numQuadrants = None): 
        numProbingLocations = this.computeNumProbingLocations(numQuadrants)
        radius = this.computeInitialDensityRadius(numProbingLocations,areaPercentage)
        densitySamples = this.sample(boundingRegion,radius,numQuadrants)
        return densitySamples,numProbingLocations
        
        
    def setIncreaseRate(this = None,increaseRate = None): 
        this.INCREASE_RATE = increaseRate
        return
        
        numProbingLocations = computeNumProbingLocations(this,numQuadrants)
        radius = computeInitialDensityRadius(this,numDummyProbingLocations,areaPercentage)
        densitySamples = sample(this,boundingRegion,radius)
        area = computeArea(this,radius)