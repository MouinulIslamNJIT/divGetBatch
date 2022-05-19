import numpy as np
import numpy.matlib
    
def find_vertex_distances(centroids = None,V = None,C = None): 
    N_cells = centroids.shape[1-1]
    Vdist = NaN * np.ones((V.shape[1-1],1))
    for i in np.arange(1,N_cells+1).reshape(-1):
        N_vert = C[i].shape[2-1]
        dist = np.sqrt(np.sum((V(C[i],:) - np.matlib.repmat(centroids(i,:),N_vert,1)) ** 2, 2-1))
        Vdist[C[i]] = dist
        if not np.isnan(Vdist) :
            break
    
    return Vdist