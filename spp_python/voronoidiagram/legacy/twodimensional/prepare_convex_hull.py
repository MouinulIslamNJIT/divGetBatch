import numpy as np
    
def prepare_convex_hull(anchors = None): 
    #V: list of all vertex coordinates
    V = anchors
    #FtoV: For each facet, list vertices
    FtoVtemp = convhulln(V)
    FtoV = cell(FtoVtemp.shape[1-1],1)
    for c in np.arange(1,FtoVtemp.shape[1-1]+1).reshape(-1):
        FtoV[c] = FtoVtemp(c,:)
    
    #VtoV: for each vertex, list all outgoing edges to neighboring vertexes
    VtoV = find_vertex_edges_cu(V,FtoV)
    return V,VtoV,FtoV