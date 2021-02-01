from IndexTree import BuildIndex
import timeit
from Utils import yelp_data,makeBlobs_data,movieLens_data


from GMM import GMM
from Utils import checkResult,InitialTwoRecordsInGMM
from AugGMM import AugGMM

def run(sampleSize, arity,numberofLevel,k):
    print('dataset size: ', sampleSize, 'k:', k, 'number of arity: ',
          arity, 'number of level: ', numberofLevel)

    X = makeBlobs_data(sampleSize)
    # X = movieLens_data(sampleSize)
    # X = yelp_data(sampleSize)

    xin = X.tolist()
    iTree, indexMap = BuildIndex(xin, arity, numberofLevel,False)
    initRecords = InitialTwoRecordsInGMM(iTree)
    Xgmm = X.tolist()
    start = timeit.default_timer()

    gmmResult = GMM(Xgmm, k,initRecords)

    print("gmm", gmmResult)
    # GMM(Xgmm, Kvalue)
    stop = timeit.default_timer()
    gmm_time = stop - start
    print('Time for gmm: ', gmm_time)

    Xgmm = X.tolist()
    start = timeit.default_timer()

    augGmmResult = AugGMM(iTree,numberofLevel,arity, Xgmm, k,indexMap,initRecords)
    print("aug", augGmmResult)
    stop = timeit.default_timer()
    auggmm_time = stop - start
    print('Time for aug-gmm: ', auggmm_time)

    checkResult(augGmmResult, gmmResult)

def main():

    run(100000,500,1,20)

main()
