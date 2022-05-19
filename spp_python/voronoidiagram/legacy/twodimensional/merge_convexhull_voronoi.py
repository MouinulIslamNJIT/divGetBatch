import numpy as np
import numpy.matlib
import warnings
    
def merge_convexhull_voronoi(Vh = None,VtoVh = None,FtoVh = None,centroids = None,Vv = None,VtoVv = None,Vdistv = None): 
    if np.isnan(Vv):
        N_vertv = 0
    else:
        N_vertv = Vv.shape[1-1]
    
    N_verth = Vh.shape[1-1]
    N_centr = centroids.shape[1-1]
    if N_centr == 1:
        V = Vh
        VtoV = VtoVh
        Vdist = np.sqrt(np.sum((Vh - np.matlib.repmat(centroids,N_verth,1)) ** 2, 2-1))
        for v in np.arange(1,VtoV.shape[1-1]+1).reshape(-1):
            edges = VtoV[v]
            E = edges.shape[2-1]
            for e in np.arange(1,E+1).reshape(-1):
                edges[2,e] = 1
                c = 1
                theta = edges(4,e)
                # project centroid on the edge
                distmax = (centroids(c,:) - V(v,:)) * np.array([[np.cos(theta)],[np.sin(theta)]])
                edges[5,e] = distmax
            VtoV[v] = edges
    else:
        if N_centr > 1:
            #find bounding box
            ub = np.amax(Vh,1)
            lb = np.amin(Vh,1)
            range_ = np.amax(ub - lb)
            maxrange = 10 * np.amax(range_)
            N_facetsh = FtoVh.shape[1-1]
            segmentsh = NaN * np.ones((N_facetsh,4))
            for fh in np.arange(1,N_facetsh+1).reshape(-1):
                vh = FtoVh[fh]
                facets = Vh(vh,:)
                segmentsh[fh,:] = np.array([facets(1,:),facets(2,:)])
            if N_centr == 2:
                V = Vh
                VtoV = VtoVh
                N_vert = N_verth
                C1 = centroids(1,:)
                C2 = centroids(2,:)
                M = (C1 + C2) / 2
                m = (C2(2) - C1(2)) / (C2(1) - C1(1))
                theta[1] = np.arctan(- (1 / m))
                theta[2] = theta(1) + pi
                P = np.array([[M + maxrange * np.array([np.cos(theta(1)),np.sin(theta(1))])],[M + maxrange * np.array([np.cos(theta(2)),np.sin(theta(2))])]])
                for i in np.arange(1,2+1).reshape(-1):
                    segmentv = np.array([M,P(i,:)])
                    out = lineSegmentIntersect(segmentv,segmentsh)
                    facet = out.intAdjacencyMatrix
                    Vt = np.array([out.intMatrixX(facet),out.intMatrixY(facet)])
                    # add new vertex
                    V = np.array([[V],[Vt]])
                    edges = NaN * np.ones((5,3))
                    # update edge
                    v1 = FtoVh[facet](1)
                    v2 = FtoVh[facet](2)
                    # split existing edge
# v1 -> v2
                    edges1 = VtoV[v1](1,:)
                    VtoV[v1][1,edges1 == v2] = N_vert + i
                    #             edges(:,1) = [v1; NaN; NaN; VtoV{v1}(4,edges1 == v2)+pi; norm(V(v1,:) - Vt)/2];
                    edges[:,1] = np.array([[v1],[NaN],[NaN],[VtoV[v1](4,edges1 == v2) + pi],[NaN]])
                    # v2 -> v1
                    edges2 = VtoV[v2](1,:)
                    VtoV[v2][1,edges2 == v1] = N_vert + i
                    #             edges(:,2) = [v2; NaN; NaN; VtoV{v2}(4,edges2 == v1)+pi; norm(V(v2,:) - Vt)/2];
                    edges[:,2] = np.array([[v2],[NaN],[NaN],[VtoV[v2](4,edges2 == v1) + pi],[NaN]])
                    # add new edge
                    if i == 1:
                        #                 edges(:,3) = [N_vert + 2; NaN; NaN; theta(i) + pi; norm(M - Vt)];
                        edges[:,3] = np.array([[N_vert + 2],[NaN],[NaN],[theta(i) + pi],[NaN]])
                    else:
                        if i == 2:
                            #                 edges(:,3) = [N_vert + 1; NaN; NaN; theta(i) + pi; norm(M - Vt)];
                            edges[:,3] = np.array([[N_vert + 1],[NaN],[NaN],[theta(i) + pi],[NaN]])
                    VtoV[N_vert + i] = edges
                N_vert = N_vert + 2
                N_vertv = 0
                ##################################################################
##################################################################
            else:
                V = np.array([[Vh],[Vv]])
                VtoV = VtoVh
                for vv in np.arange(1,N_vertv+1).reshape(-1):
                    edges = VtoVv[vv]
                    E = edges.shape[2-1]
                    for e in np.arange(1,E+1).reshape(-1):
                        if edges(1,e) != 0:
                            edges[1,e] = edges(1,e) + N_verth
                    VtoV = np.array([[VtoV],[edges]])
                #         VtoVv{vv} = edges;
                #         VtoV = [VtoVh; VtoVv];
                N_vert = N_verth + N_vertv
                Vout = np.array([[np.zeros((N_verth,1))],[find_outside_convex_hull(Vv,Vh,FtoVh)]])
                # find intersections
#intersections might arise due to:
#-semi-infinite edges
#-edges towards vertex outside the cu
#-edges connecting two vertexes outside the cu
                Vt = []
                N_vert = V.shape[1-1]
                for vv in np.arange(N_verth + 1,N_vert+1).reshape(-1):
                    #-edges connecting two vertexes outside the cu
                    if Vout(vv):
                        #                 VtoV{vv} = NaN;
#                 V(vv,:) = NaN;
                        edges = VtoV[vv]
                        E = edges.shape[2-1]
                        for e in np.arange(1,E+1).reshape(-1):
                            if edges(1,e) != 0:
                                if Vout(edges(1,e)) == 1:
                                    V1 = V(vv,:)
                                    V2 = V(edges(1,e),:)
                                    segmentv = np.array([V1,V2])
                                    out = lineSegmentIntersect(segmentv,segmentsh)
                                    index = out.intAdjacencyMatrix
                                    indexes = find(index)
                                    for i in np.arange(1,len(indexes)+1).reshape(-1):
                                        Vt = np.array([[Vt],[np.array([out.intMatrixX(indexes(i)),out.intMatrixY(indexes(i)),vv,indexes(i)])]])
                            else:
                                theta = edges(4,e)
                                V1 = V(vv,:)
                                V2 = V(vv,:) + maxrange * np.array([np.cos(theta),np.sin(theta)])
                                segmentv = np.array([V1,V2])
                                out = lineSegmentIntersect(segmentv,segmentsh)
                                index = out.intAdjacencyMatrix
                                indexes = find(index)
                                for i in np.arange(1,len(indexes)+1).reshape(-1):
                                    Vt = np.array([[Vt],[np.array([out.intMatrixX(indexes(i)),out.intMatrixY(indexes(i)),vv,indexes(i)])]])
                    else:
                        edges = VtoV[vv]
                        E = edges.shape[2-1]
                        for e in np.arange(1,E+1).reshape(-1):
                            #-semi-infinite edges
#-edges towards vertex outside the cu
                            if edges(1,e) == 0 or Vout(edges(1,e)):
                                #                         N_vert = N_vert + 1; #MT check
                                theta = edges(4,e)
                                V1 = V(vv,:)
                                V2 = V(vv,:) + maxrange * np.array([np.cos(theta),np.sin(theta)])
                                segmentv = np.array([V1,V2])
                                out = lineSegmentIntersect(segmentv,segmentsh)
                                index = out.intAdjacencyMatrix
                                Vt = np.array([[Vt],[np.array([out.intMatrixX(index),out.intMatrixY(index),vv,find(index)])]])
                # handle intersections
                facetsi = unique(Vt(:,4))
                N_facetsi = len(facetsi)
                N_vert = V.shape[1-1]
                for f in np.arange(1,N_facetsi+1).reshape(-1):
                    Vi = Vt(Vt(:,4) == facetsi(f),np.arange(1,2+1))
                    facet = facetsi(f)
                    vv = Vt(Vt(:,4) == facetsi(f),3)
                    N_intersections = Vi.shape[1-1]
                    if N_intersections == 1:
                        # add new vertex
                        V = np.array([[V],[Vi]])
                        Vout = np.array([[Vout],[0]])
                        N_vert = N_vert + 1
                        edges = NaN * np.ones((5,3))
                        # make infinite edge finite
                        dist = norm(Vi - V(vv,:))
                        edgesvv = VtoV[vv]
                        Ev = edgesvv.shape[2-1]
                        for ev in np.arange(1,Ev+1).reshape(-1):
                            if edgesvv(1,ev) == 0 or Vout(edgesvv(1,ev)):
                                thetavv = edgesvv(4,ev)
                                Vtemp = V(vv,:) + dist * np.array([np.cos(thetavv),np.sin(thetavv)])
                                if norm(Vi - Vtemp) < 100 * eps:
                                    edgesvv[1,ev] = N_vert
                                    theta = thetavv
                                    break
                        VtoV[vv] = edgesvv
                        # update edge
                        v1 = FtoVh[facet](1)
                        v2 = FtoVh[facet](2)
                        # split existing edge
# v1 -> v2
                        edges1 = VtoV[v1](1,:)
                        VtoV[v1][1,edges1 == v2] = N_vert
                        edges[:,1] = np.array([[v1],[NaN],[NaN],[VtoV[v1](4,edges1 == v2) + pi],[NaN]])
                        # v2 -> v1
                        edges2 = VtoV[v2](1,:)
                        VtoV[v2][1,edges2 == v1] = N_vert
                        edges[:,2] = np.array([[v2],[NaN],[NaN],[VtoV[v2](4,edges2 == v1) + pi],[NaN]])
                        #                 distvv = VtoV{vv}(5,VtoV{vv}(1,:) == N_vert);
#                 edges(:,3) = [vv; NaN; NaN; theta + pi; NaN];
                        VtoV[N_vert] = edges
                    else:
                        v1 = FtoVh[facet](1)
                        v2 = FtoVh[facet](2)
                        V1 = V(v1,:)
                        V2 = V(v2,:)
                        Vi = find_unique_points(Vi)
                        omega = find_offsets(Vi,V1,V2)
                        omega,index = __builtint__.sorted(omega,'ascend')
                        Vi = Vi(index,:)
                        N_inter = Vi.shape[1-1]
                        # add new vertexes
                        V = np.array([[V],[Vi]])
                        Vout = np.array([[Vout],[np.zeros((N_inter,1))]])
                        for vu in np.arange(N_vert + 1,N_vert + N_inter+1).reshape(-1):
                            edges = NaN * np.ones((5,3))
                            if vu == N_vert + 1:
                                edgesv1 = VtoV[v1]
                                edges[1,1] = v1
                                edges[4,1] = edgesv1(4,edgesv1(1,:) == v2) + pi
                                #                        edges(5,1) = norm(V(vu,:) - V(v1,:))/2;
                                edges[1,2] = vu + 1
                                edges[4,2] = edgesv1(4,edgesv1(1,:) == v2)
                                #                        edges(5,2) = norm(V(vu,:) - V(vu+1,:))/2;
                                edgesv1[1,edgesv1[1,:] == v2] = vu
                                VtoV[v1] = edgesv1
                            else:
                                if vu == N_vert + N_inter:
                                    edgesv2 = VtoV[v2]
                                    edges[1,1] = v2
                                    edges[4,1] = edgesv2(4,edgesv2(1,:) == v1) + pi
                                    #                        edges(5,1) = norm(V(vu,:) - V(v2,:))/2;
                                    edges[1,2] = vu - 1
                                    edges[4,2] = edgesv2(4,edgesv2(1,:) == v1)
                                    #                        edges(5,2) = norm(V(vu,:) - V(vu-1,:))/2;
                                    edgesv2[1,edgesv2[1,:] == v1] = vu
                                    VtoV[v2] = edgesv2
                                else:
                                    edgesv1 = VtoV[vu - 1]
                                    edges[1,1] = vu + 1
                                    edges[4,1] = edgesv1(4,edgesv1(1,:) == vu)
                                    #                        edges(5,1) = norm(V(vu,:) - V(vu+1,:))/2;
                                    edges[1,2] = vu - 1
                                    edges[4,2] = edgesv1(4,edgesv1(1,:) == vu) + pi
                                    #                        edges(5,2) = norm(V(vu,:) - V(vu-1,:))/2;
                            edges[1,3] = 0
                            VtoV[vu] = edges
                        N_vert = N_vert + N_inter
                for vv in np.arange(N_verth + 1,N_verth + N_vertv+1).reshape(-1):
                    # add missing edges originating from vertexes inside the cu to
# infinity
                    if not Vout(vv) :
                        edgesvv = VtoV[vv]
                        Evv = edgesvv.shape[2-1]
                        for evv in np.arange(1,Evv+1).reshape(-1):
                            vi = edgesvv(1,evv)
                            if vi > N_verth + N_vertv:
                                theta = edgesvv(4,evv)
                                edgesvi = VtoV[vi]
                                edgesvi[1,3] = vv
                                edgesvi[4,3] = theta + pi
                                VtoV[vi] = edgesvi
                            else:
                                if vi == 0:
                                    theta = edgesvv(4,evv)
                                    dir = np.array([np.cos(theta),np.sin(theta)])
                                    for vii in np.arange(N_verth + N_vertv + 1,N_vert+1).reshape(-1):
                                        temp = V(vii,:) - V(vv,:)
                                        temp = temp / norm(temp)
                                        if dir * np.transpose(temp) > 1 - 100 * eps:
                                            edgesvii = VtoV[vii]
                                            edgesvii[1,3] = vv
                                            edgesvii[4,3] = theta + pi
                                            VtoV[vii] = edgesvii
                                            VtoV[vv][1,edgesvv[1,:] == 0] = vii
                    else:
                        if Vout(vv):
                            edgesvv = VtoV[vv]
                            Evv = edgesvv.shape[2-1]
                            for evv in np.arange(1,Evv+1).reshape(-1):
                                v2 = edgesvv(1,evv)
                                if v2 != 0:
                                    #count intersections
                                    segmentv = np.array([V(vv,:),V(v2,:)])
                                    out = lineSegmentIntersect(segmentv,segmentsh)
                                    index = out.intAdjacencyMatrix
                                    if sum(index) == 1:
                                        theta = edgesvv(4,evv)
                                        dir = np.array([np.cos(theta),np.sin(theta)])
                                        for vi in np.arange(N_verth + N_vertv + 1,N_vert+1).reshape(-1):
                                            temp = V(vi,:) - V(vv,:)
                                            temp = temp / norm(temp)
                                            if dir * np.transpose(temp) > 1 - 100 * eps:
                                                edgesvi = VtoV[vi]
                                                edgesvi[1,3] = v2
                                                edgesvi[4,3] = theta
                                                VtoV[vi] = edgesvi
                                                edgesv2 = VtoV[v2]
                                                VtoV[v2][1,edgesv2[1,:] == vv] = vi
                                    else:
                                        if sum(index) == 2:
                                            theta = edgesvv(4,evv)
                                            dir = np.array([np.cos(theta),np.sin(theta)])
                                            vt = []
                                            for vi in np.arange(N_verth + N_vertv,N_vert+1).reshape(-1):
                                                temp = V(vi,:) - V(vv,:)
                                                temp = temp / norm(temp)
                                                if dir * np.transpose(temp) > 1 - 100 * eps:
                                                    vt = np.array([vt,vi])
                                            diff = V(vt(2),:) - V(vt(1),:)
                                            theta,rho = cart2pol(np.diff(1),np.diff(2))
                                            #                             dist = norm(diff);
                                            edgesvt1 = VtoV[vt(1)]
                                            edgesvt1[1,3] = vt(2)
                                            edgesvt1[4,3] = theta
                                            #                             edgesvt1(5,3) = dist/2;
                                            VtoV[vt[1]] = edgesvt1
                                            edgesvt2 = VtoV[vt(2)]
                                            edgesvt2[1,3] = vt(1)
                                            edgesvt2[4,3] = theta + pi
                                            #                             edgesvt2(5,3) = dist/2;
                                            VtoV[vt[2]] = edgesvt2
                # remove vertexes outside cu and re-assign labels
                vin = find(Vout == 0)
                N_vert = len(vin)
                V = V(vin,:)
                VtoVnew = cell(N_vert,1)
                for i in np.arange(1,N_vert+1).reshape(-1):
                    VtoVnew[i] = VtoV[vin(i)]
                    edges = VtoVnew[i]
                    E = edges.shape[2-1]
                    for e in np.arange(1,E+1).reshape(-1):
                        VtoVnew[i][1,e] = find(vin == edges(1,e))
                VtoV = VtoVnew
                N_vertv = N_vertv - sum(Vout)
            N_vert = V.shape[1-1]
            Vdist = NaN * np.ones((N_vert,1))
            for v in np.arange(1,N_vert+1).reshape(-1):
                dist = np.sqrt(np.sum((np.matlib.repmat(V(v,:),centroids.shape[1-1],1) - centroids) ** 2, 2-1))
                mindist,minindex = np.amin(dist)
                Vdist[v] = mindist
                if v <= N_verth or v > N_verth + N_vertv:
                    edges = VtoV[v]
                    E = edges.shape[2-1]
                    for e in np.arange(1,E+1).reshape(-1):
                        v2 = edges(1,e)
                        V1 = V(v,:)
                        V2 = V(v2,:)
                        M = (V1 + V2) / 2
                        dist = np.sqrt(np.sum((np.matlib.repmat(M,centroids.shape[1-1],1) - centroids) ** 2, 2-1))
                        mindist = np.amin(dist)
                        nearest_centroids = find(dist == mindist)
                        if len(nearest_centroids) == 1:
                            edges[2,e] = nearest_centroids
                        else:
                            if len(nearest_centroids) == 2:
                                edges[np.arange[2,3+1],e] = nearest_centroids
                            else:
                                warnings.warn('more than two nearest centroids')
                        c = edges(2,e)
                        theta = VtoV[v](4,e)
                        # project centroid on the edge
                        distmax = (centroids(c,:) - V(v,:)) * np.array([[np.cos(theta)],[np.sin(theta)]])
                        edges[5,e] = distmax
                    VtoV[v] = edges
    
    return V,VtoV,Vdist,N_vertv