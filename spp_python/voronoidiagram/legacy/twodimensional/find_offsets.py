import numpy as np
    
def find_offsets(Vi = None,V1 = None,V2 = None): 
    N_vert = Vi.shape[1-1]
    omega = NaN * np.ones((N_vert,1))
    for v in np.arange(1,N_vert+1).reshape(-1):
        if np.abs(V2(1) - V1(1)) > eps:
            omega[v] = (Vi(v,1) - V1(1)) / (V2(1) - V1(1))
        else:
            omega[v] = (Vi(v,2) - V1(2)) / (V2(2) - V1(2))
    
    return omega