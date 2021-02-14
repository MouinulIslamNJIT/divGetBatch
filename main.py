from AugGMM.runGMM import runGMM
from AugMMR.runMMR import runMMR
from  AugSWAP.runSWAP import runSWAP

def main():
    runGMM(20000,100,1,20)
    runMMR(20000, 100, 1, 20)
    runSWAP(20000, 100, 1, 20)

if __name__ == '__main__':
    main()
