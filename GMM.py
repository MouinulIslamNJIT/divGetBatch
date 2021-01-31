
from pyclustering.utils import euclidean_distance_square
import numpy as np

def GMM(U, K,record1,record2):
    S = []
    S.append(record1)
    S.append(record2)
    U.remove(record1)
    U.remove(record2)
    minMap = {}

    for i in U:
        dist = euclidean_distance_square(i, record1)
        minMap[tuple(i)] = dist
    nextItem = record2

    for k in range(K - 2):
        L = []
        for i in U:
            min = minMap[tuple(i)]
            dist = euclidean_distance_square(i, nextItem)
            if min > dist:
                min = dist
                minMap[tuple(i)] = min
            L.append(min)
        index_max = np.argmax(L)
        nextItem = U[index_max]
        S.append(U[index_max])
        U.remove(U[index_max])
    return S
