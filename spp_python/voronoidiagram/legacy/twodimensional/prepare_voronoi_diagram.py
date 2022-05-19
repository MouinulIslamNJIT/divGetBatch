import numpy as np
    
def prepare_voronoi_diagram(centroids = None): 
    #V: list of all vertex coordinates (V(1,:) is the vertex at infinity)
#CtoV: For each cell, list vertices
    V,CtoV = voronoin(centroids)
    #VtoV: for each vertex, list all outgoing edges to neighboring vertexes
    VtoV = find_vertex_edges(V,centroids,CtoV)
    #Vdist: for each vertex, indicates the distance to the closest centroid
    Vdist = find_vertex_distances(centroids,V,CtoV)
    # remove vertex at infinity
    N_vert = V.shape[1-1]
    VtoVtemp = cell(N_vert - 1,1)
    for v in np.arange(1,N_vert - 1+1).reshape(-1):
        VtoVtemp[v] = VtoV[v + 1]
        edges = VtoVtemp[v]
        edges[1,:] = edges(1,:) - 1
        VtoVtemp[v] = edges
    
    VtoV = VtoVtemp
    V = V(np.arange(2,N_vert+1),:)
    Vdist = Vdist(np.arange(2,N_vert+1))
    return V,VtoV,Vdist