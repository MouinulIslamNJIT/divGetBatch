import numpy as np
import numpy.matlib
    
def isfuzzymember(matrix1 = None,matrix2 = None,tolerance = None): 
    ids = np.zeros((matrix1.shape[1-1],1))
    if len(varargin) == 2:
        tolerance = 1.5 * eps
    
    if matrix1.shape[2-1] != matrix2.shape[2-1]:
        throw(MException('MATLAB:isfuzzymember','the two matrices must have the same number of columns'))
    
    for row in np.arange(1,matrix1.shape[1-1]+1).reshape(-1):
        distances = np.sqrt(np.sum((np.matlib.repmat(matrix1(row,:),matrix2.shape[1-1],1) - matrix2) ** 2, 2-1))
        idxs = find(distances < tolerance)
        if not len(idxs)==0 :
            ids[row] = idxs(end())
    
    return ids
    
    return ids