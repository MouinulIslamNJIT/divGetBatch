import os
import numpy as np
    
def polyn2sym(polyn = None): 
    # polyn2sympoly: convert a regression polynomial from polyfitn into its symbolic toolbox form
# usage: sp = polyn2sym(polyn)
    
    # arguments: (input)
#  polyn - a structure as returned from polyfitn
    
    # arguments: (output)
#  s - A symbolic toolbox object
    
    # After conversion into a symbolic toolbox form, any symbolic operations are
# now possible on the polynomial.
    
    # Requirement: The symbolic toolbox, as supplied by the MathWorks.
# http://www.mathworks.com/products/symbolic/functionlist.html
    
    # See also: polyvaln, polyfit, polyval, sym
    
    # Author: John D'Errico
# Release: 3.0
# Release date: 8/23/06
    
    if os.path.exist(str('sym')) != 2:
        raise Exception('Please obtain the symbolic toolbox from the MathWorks')
    
    # initialize the returned argument as symbolic
    s = sym(0)
    # Unpack the fields of polyn for use
    Varlist = polyn.VarNames
    Expon = polyn.ModelTerms
    Coef = polyn.Coefficients
    # how many terms?
    nterms = len(Coef)
    # Was the list of variable names empty?
# If so, then generate a list of names of my own.
    nvars = polyn.ModelTerms.shape[2-1]
    if len(Varlist)==0:
        Varlist = np.array([])
        for i in np.arange(1,nvars+1).reshape(-1):
            Varlist[i] = np.array(['X',num2str(i)])
    
    # make the vars symbolic
    for i in np.arange(1,nvars+1).reshape(-1):
        Varlist[i] = sym(Varlist[i])
    
    # build the polynomial
    for i in np.arange(1,nterms+1).reshape(-1):
        term = sym(Coef(i))
        for j in np.arange(1,nvars+1).reshape(-1):
            term = term * Varlist[j] ** Expon(i,j)
        # accumulate into s
        s = s + term
    
    return s