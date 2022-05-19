import numpy as np
    
def find_outside_convex_hull(V = None,Vh = None,FtoVh = None): 
    N_vert = V.shape[1-1]
    N_facets = FtoVh.shape[1-1]
    A = NaN * np.ones((N_facets,2))
    b = NaN * np.ones((N_facets,1))
    for facet in np.arange(1,N_facets+1).reshape(-1):
        v1 = FtoVh[facet](1)
        v2 = FtoVh[facet](2)
        V1 = Vh(v1,:)
        V2 = Vh(v2,:)
        A[facet,:] = np.array([V2(2) - V1(2),V1(1) - V2(1)])
        b[facet] = V1(2) * (V2(1) - V1(1)) - V1(1) * (V2(2) - V1(2))
    
    Vout = np.zeros((N_vert,1))
    for v in np.arange(1,N_vert+1).reshape(-1):
        constraints = (A * np.transpose(V(v,:)) - b) >= 0
        if sum(constraints) < N_facets:
            Vout[v] = 1
    
    return Vout