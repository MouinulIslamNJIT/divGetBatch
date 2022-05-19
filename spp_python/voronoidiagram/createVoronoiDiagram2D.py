import numpy as np
    
def createVoronoiDiagram2D(centroids = None,boundingRegion = None,k = None): 
    # adapt the input data structures
    centroidsFeatures = vertcat(centroids.features)
    # call the legacy functions
    
    
    
    if len(Vh)==0:
        upperBound = boundingRegion.upperBound
        lowerBound = boundingRegion.lowerBound
        anchors = np.array([[lowerBound,lowerBound],[lowerBound,upperBound],[upperBound,lowerBound],[upperBound,upperBound]])
        Vh,VtoVh,FtoVh = prepare_convex_hull(anchors)
    
    if k <= 3:
        V,VtoV,Vdist,N_vertv = merge_convexhull_voronoi(Vh,VtoVh,FtoVh,centroidsFeatures,NaN,NaN,NaN)
    else:
        Vv,VtoVv,Vdistv = prepare_voronoi_diagram(centroidsFeatures)
        V,VtoV,Vdist,N_vertv = merge_convexhull_voronoi(Vh,VtoVh,FtoVh,centroidsFeatures,Vv,VtoVv,Vdistv)
    
    N_vert = V.shape[1-1]
    N_verth = Vh.shape[1-1]
    factor = np.ones((N_vert,1))
    factor[np.arange[1,N_verth+1]] = 0.25
    factor[np.arange[N_verth + N_vertv + 1,N_vert+1]] = 0.5
    # adapt the output data structures
    voronoiDiagram = struct('centroids',centroids,'topology',np.array([VtoV]),'vertices',struct('distancesFromCentroids',Vdist,'coordinates',V,'factor',factor))
    return voronoiDiagram
    
    return voronoiDiagram