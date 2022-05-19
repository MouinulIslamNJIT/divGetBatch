
class Timer():
    #TIMER Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None): 
        this.totalObservationTime = 0
        return
        
        
    def start(this = None): 
        this.endInstant = 0
        this.startInstant = toc
        return
        
        
    def stop(this = None): 
        this.endInstant = toc
        timeInterval = this.endInstant - this.startInstant
        this.totalObservationTime = this.totalObservationTime + timeInterval
        return
        
        
    def getTotalObservationTime(this = None): 
        totalObservationTime = this.totalObservationTime
        return totalObservationTime
        