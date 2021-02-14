from AugGMM.runGMM import runGMM
from AugMMR.runMMR import runMMR
from  AugSWAP.runSWAP import runSWAP

def main():
    runGMM(50000,500,1,20)
    runMMR(50000, 500, 1, 20)
    runSWAP(50000, 500, 1, 20)

if __name__ == '__main__':
    main()
