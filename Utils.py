import guppy
import inspect
from pyclustering.utils import euclidean_distance_square
def get_object_size(obj):
    h = guppy.hpy()
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()

    vname = "Index size"

    # for var_name, var_val in callers_local_vars:
    #     if var_val == obj:
    #         vname = str(var_name)

    size = str("{0:.8f} MB".format(float(h.iso(obj).domisize) / (1024*1024)))

    return str("{}: {}".format(vname, size))


def checkResult(augGmmResult, gmmResult):
    if sorted(augGmmResult) == sorted(gmmResult):
        print("array equal")
    else:
        print("array not equal")
        for i in gmmResult:
            if i not in augGmmResult:
                print(i, " not in Aug GMM")

        for i in augGmmResult:
            if i not in gmmResult:
                print(i, " not in GMM")
def div(i,j):
    return euclidean_distance_square(i, j)
def InitialTwoRecordsInGMM(cluster):
    maxdis = 0
    selectedNode1 = None
    selectedNode2 = None

    for node1 in cluster.root.children:
        for node2 in cluster.root.children:
            distmin , distmax = cluster.dismatrix[1][node1.id][node2.id]
            if maxdis < distmax:
                maxdis = distmax
                selectedNode1 = node1
                selectedNode2 = node2
    candR = selectedNode1.elements + selectedNode2.elements

    maxdis = 0

    for i in candR:
        for j in candR:
            if i != j:
                dis = euclidean_distance_square(i, j)
                if maxdis < dis:
                    maxdis = dis
                    record1 = i
                    record2 = j

    selectedNode1.elements.remove(record1)
    selectedNode2.elements.remove(record2)

    return  (record1,record2)

def similarity(r1,r2):
    return 1/(1+euclidean_distance_square(r1, r2))