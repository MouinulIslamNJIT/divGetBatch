import os
import numpy as np
    
def polyn2sympoly(polyn = None): 
    # polyn2sympoly: convert a regression polynomial from polyfitn into a sympoly
# usage: sp = polyn2sympoly(polyn)
    
    # arguments: (input)
#  polyn - a structure as returned from polyfitn
    
    # arguments: (output)
#  sp - A sympoly object
    
    # After conversion into a sympoly, any symbolic operations are
# now possible on this form.
    
    # Requirement: The sympoly toolbox, as found on Matlab Central.
# http://www.mathworks.com/matlabcentral/fileexchange/loadFile.do?objectId=9577&objectType=FILE
    
    # See also: polyvaln, polyfit, polyval, sympoly
    
    # Author: John D'Errico
# Release: 1.0
# Release date: 2/19/06
    
    if os.path.exist(str('sympoly')) != 2:
        raise Exception('Please download the sympoly toolbox from Matlab Central')
    
    # Copy over the fields of polyn into sp
    sp.Var = polyn.VarNames
    sp.Exponent = polyn.ModelTerms
    sp.Coefficient = polyn.Coefficients
    # Was the list of variable names empty?
# If so, then generate a list of names of my own.
    if len(sp.Var)==0:
        p = polyn.ModelTerms.shape[2-1]
        varlist = np.array([])
        for i in np.arange(1,p+1).reshape(-1):
            varlist[i] = np.array(['X',num2str(i)])
        sp.Var = varlist
    
    # turn the struct into a sympoly
    sp = sympoly(sp)
    return sp