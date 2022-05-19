import numpy as np
    
def find_vertex_edges_cu(V = None,CtoV = None): 
    N_facets = CtoV.shape[1-1]
    N_vert = V.shape[1-1]
    VtoVtemp = cell(N_vert,1)
    VtoV = cell(N_vert,1)
    for v in np.arange(1,N_vert+1).reshape(-1):
        VtoVtemp[v] = cell(2,1)
    
    for i in np.arange(1,N_facets+1).reshape(-1):
        Nv = len(CtoV[0])
        for j in np.arange(1,Nv+1).reshape(-1):
            v1 = CtoV[i](j)
            if j < Nv:
                v2 = CtoV[i](j + 1)
            else:
                v2 = CtoV[i](1)
            VtoVtemp[v1][0] = np.array([VtoVtemp[v1][0],v2])
            VtoVtemp[v2][0] = np.array([VtoVtemp[v2][0],v1])
            VtoVtemp[v1][2] = np.array([VtoVtemp[v1][2],i])
            VtoVtemp[v2][2] = np.array([VtoVtemp[v2][2],i])
    
    # add cells divided by each edge
    for v in np.arange(1,N_vert+1).reshape(-1):
        edges = unique(VtoVtemp[v][0])
        E = len(edges)
        for e in np.arange(1,E+1).reshape(-1):
            indexes = find(VtoVtemp[v][0] == edges(e))
            cells = unique(VtoVtemp[v][2](indexes))
            VtoV[v] = np.array([VtoV[v],np.array([[edges(e)],[cells(1)],[NaN]])])
    
    # add edge direction (outgoing direction from reference vertex)
    for v in np.arange(1,N_vert+1).reshape(-1):
        edges = VtoV[v]
        E = edges.shape[2-1]
        VtoVnew = NaN * np.ones((5,E))
        for e in np.arange(1,E+1).reshape(-1):
            V1 = V(v,:)
            V2 = V(edges(1,e),:)
            dV = (V2 - V1) / norm(V2 - V1)
            theta,rho = cart2pol(dV(1),dV(2))
            dist = NaN
            VtoVnew[:,e] = np.array([[edges(np.arange(1,3+1),e)],[theta],[dist]])
        VtoV[v] = VtoVnew
    
    return VtoV