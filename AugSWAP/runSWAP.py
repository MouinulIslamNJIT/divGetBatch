
import timeit
from Utils import createSimMatrix, topkitems, div
from SWAP import SWAP
from  AugSWAP import AugSWAP
from IndexTree import BuildIndex
from Utils import checkResult
from Utils import yelp_data,makeBlobs_data,movieLens_data


def run(sampleSize, arity, numberofLevel, k):

    print('dataset size: ', sampleSize, 'k:', k, 'number of arity: ',
          arity, 'number of level: ', numberofLevel)

    # X = makeBlobs_data(sampleSize)
    # X = movieLens_data(sampleSize)
    X = yelp_data(sampleSize)

    X = X.tolist()
    query = [1, -1, 1]
    r = createSimMatrix(query, X)
    ub = 1000000

    start = timeit.default_timer()
    res = SWAP(X, r, k, ub)
    stop = timeit.default_timer()
    print('Time for calculate swap: ', stop - start)

    # print("swap: ",res)

    iTree,indexMap = BuildIndex(X, arity, numberofLevel,True)

    start = timeit.default_timer()
    augres = AugSWAP(X, iTree, r, k, ub)
    stop = timeit.default_timer()
    print('Time for calculate Aug swap: ', stop - start)

    # print("AugSwap: ",augres)

    checkResult(augres, res)

run(50000, 50, 1, 20)