import numpy as np
import numpy.matlib
    
def find_unique_points(Vin = None): 
    N_vert = Vin.shape[1-1]
    Vout = Vin(1,:)
    vo = 1
    for v in np.arange(2,N_vert+1).reshape(-1):
        dist = np.sum((np.matlib.repmat(Vin(v,:),Vout.shape[1-1],1) - Vout) ** 2, 2-1)
        if np.amin(dist) > eps:
            vo = vo + 1
            Vout[vo,:] = Vin(v,:)
    
    return Vout