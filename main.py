from AugGMM.runGMM import runGMM
from AugMMR.runMMR import runMMR
from AugSWAP.runSWAP import runSWAP
from MaintenanceCodes.GrMn import grMn
from MaintenanceCodes.NonIncrMn import  nonIncrMn
from MaintenanceCodes.nonOlMn import nonOlMn
from MaintenanceCodes.OPTMn import OPTMn
from MaintenanceCodes.delete import delete


def main():
    #maintenance code
    #nonOlMn()
    #nonIncrMn()
    #grMn()
    #delete()
    #OPTMn()



    runGMM(20000,100,1,20)
    #runMMR(20000, 100, 1, 20)
    #runSWAP(20000, 100, 1, 20)





if __name__ == '__main__':
    main()
