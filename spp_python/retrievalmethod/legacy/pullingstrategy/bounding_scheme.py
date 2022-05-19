import numpy as np
import warnings
    
def bounding_scheme(edges = None,V1 = None,V = None,distance_to_vertex = None,centroids = None,S_last = None,lambda_ = None,rho = None,Vdepth = None): 
    Vtau = - Inf
    Vgrad = NaN
    E = edges.shape[2-1]
    for e in np.arange(1,E+1).reshape(-1):
        edge_length = norm(V(edges(1,e),:) - V1)
        if np.isnan(edges(5,e)) and distance_to_vertex <= edge_length:
            theta = edges(4,e)
            dir = np.array([np.cos(theta),np.sin(theta)])
            V2 = V1 + distance_to_vertex * dir
            if centroids.shape[1-1] == 1:
                C1 = centroids
            else:
                warnings.warn(0,'to be completed')
            upper_bound = (1 - lambda_) * S_last + lambda_ * norm(V2 - C1)
            if upper_bound > Vtau:
                Vtau = upper_bound
                x1 = sum(np.multiply((C1 - V1),dir))
                x2 = np.sqrt(norm(C1 - V1) ** 2 - x1 ** 2)
                t = distance_to_vertex
                Vgrad1 = - (x1 - t) / np.sqrt(x2 ** 2 + (x1 - t) ** 2)
                Vgrad2 = 1 / np.sqrt(rho * pi * Vdepth)
                Vgrad = Vgrad1 * Vgrad2
        else:
            if distance_to_vertex < edges(5,e) and distance_to_vertex <= edge_length:
                theta = edges(4,e)
                dir = np.array([np.cos(theta),np.sin(theta)])
                V2 = V1 + distance_to_vertex * dir
                c1 = edges(2,e)
                C1 = centroids(c1,:)
                upper_bound = (1 - lambda_) * S_last + lambda_ * norm(V2 - C1)
                if upper_bound > Vtau:
                    Vtau = upper_bound
                    x1 = sum(np.multiply((C1 - V1),dir))
                    x2 = np.sqrt(norm(C1 - V1) ** 2 - x1 ** 2)
                    t = distance_to_vertex
                    Vgrad1 = - (x1 - t) / np.sqrt(x2 ** 2 + (x1 - t) ** 2)
                    Vgrad2 = 1 / np.sqrt(rho * pi * Vdepth)
                    Vgrad = Vgrad1 * Vgrad2
    
    return Vtau,Vgrad