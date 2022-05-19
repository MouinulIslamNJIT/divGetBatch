import numpy as np
import numpy.matlib
    
def find_vertex_edges(V = None,C = None,CtoV = None): 
    N_cells = CtoV.shape[1-1]
    N_vert = V.shape[1-1]
    VtoVtemp = cell(N_vert,1)
    VtoV = cell(N_vert,1)
    if C.shape[1-1] == 3:
        edges = NaN * np.ones((3,3))
        for e in np.arange(1,3+1).reshape(-1):
            if e <= 2:
                c1 = e
                c2 = e + 1
            else:
                c1 = e
                c2 = 1
            edges[:,e] = np.array([[1],[c1],[c2]])
        VtoV[2] = edges
    else:
        for v in np.arange(1,N_vert+1).reshape(-1):
            VtoVtemp[v] = cell(2,1)
        for i in np.arange(1,N_cells+1).reshape(-1):
            Nv = CtoV[i].shape[2-1]
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
                cells = VtoVtemp[v][2](indexes)
                if len(cells) == 2:
                    VtoV[v] = np.array([VtoV[v],np.array([[edges(e)],[cells(1)],[cells(2)]])])
                else:
                    if len(cells) == 4:
                        cells = __builtint__.sorted(cells)
                        if cells(1) == cells(2):
                            VtoV[v] = np.array([VtoV[v],np.array([[edges(e)],[cells(1)],[cells(3)]]),np.array([[edges(e)],[cells(1)],[cells(4)]])])
                        else:
                            if cells(2) == cells(3):
                                VtoV[v] = np.array([VtoV[v],np.array([[edges(e)],[cells(2)],[cells(1)]]),np.array([[edges(e)],[cells(2)],[cells(4)]])])
                            else:
                                if cells(3) == cells(4):
                                    VtoV[v] = np.array([VtoV[v],np.array([[edges(e)],[cells(3)],[cells(1)]]),np.array([[edges(e)],[cells(3)],[cells(2)]])])
                                else:
                                    raise Exception('something wrong')
    
    # add edge direction (outgoing direction from reference vertex)
    for v in np.arange(2,N_vert+1).reshape(-1):
        edges = VtoV[v]
        E = edges.shape[2-1]
        VtoVnew = NaN * np.ones((5,E))
        # push edge pointing to vertex at infinity at the end of the list,
# since it needs to be treated after all the others
        temp,indexes = __builtint__.sorted(edges(1,:),'descend')
        edges = edges(:,indexes)
        for e in np.arange(1,E+1).reshape(-1):
            if edges(1,e) != 1:
                V1 = V(v,:)
                V2 = V(edges(1,e),:)
                dV = (V2 - V1) / norm(V2 - V1)
                theta,rho = cart2pol(dV(1),dV(2))
                C1 = C(edges(2,e),:)
                C2 = C(edges(3,e),:)
                M = (C1 + C2) / 2
                dist = (M(1) - V1(1)) / np.cos(theta)
                dist = np.amin(dist,norm(V2 - V1))
                #             dist2 = norm(M - V1);
                VtoVnew[:,e] = np.array([[edges(np.arange(1,3+1),e)],[theta],[dist]])
            else:
                V1 = V(v,:)
                c1 = edges(2,e)
                c2 = edges(3,e)
                C1 = C(c1,:)
                C2 = C(c2,:)
                M = (C1 + C2) / 2
                m = (M(2) - V1(2)) / (M(1) - V1(1))
                theta = np.arctan(m)
                # create two points along the line passing through V1 at either
# sides of V1. The correct direction is the half line that
# contains the point whose nearest neighbor is either C1 or C2
                X1 = V1 + np.array([np.cos(theta),np.sin(theta)])
                X2 = V1 + np.array([np.cos(theta + pi),np.sin(theta + pi)])
                CX = C(unique(edges(np.arange(2,3+1),:)),:)
                distX1 = np.sum((np.matlib.repmat(X1,CX.shape[1-1],1) - CX) ** 2, 2-1)
                distX2 = np.sum((np.matlib.repmat(X2,CX.shape[1-1],1) - CX) ** 2, 2-1)
                temp,index1 = np.amin(distX1)
                temp,index2 = np.amin(distX2)
                if norm(CX(index1,:) - C1) == 0 or norm(CX(index1,:) - C2) == 0:
                    #                 theta = theta;
                    pass
                else:
                    if norm(CX(index2,:) - C1) == 0 or norm(CX(index2,:) - C2) == 0:
                        theta = theta + pi
                dist = (M(1) - V1(1)) / np.cos(theta)
                VtoVnew[:,e] = np.array([[edges(np.arange(1,3+1),e)],[theta],[dist]])
        VtoV[v] = VtoVnew
    
    return VtoV
    
    return VtoV