import numpy as np
    
def polydern(p = None,diffvar = None): 
    # polydern: partial derivatives of a n-dimensional polynomial model created by polyfitn.
# usage: pout = polydern(p,diffvar)
    
    # arguments: (input)
#  p - a structure containing a polynomial regression model.  See polyfitn
#      for details.
    
    #  diffvar - integer, which variable to compute the derivative with respect
#      to. If diffvar is a character string, then it refers to an explicit
#      variable in the model that is found in the VarNames field. If so,
#      the variable name must be an exact match for one of the variables
#      listed in p.VarNames.
    
    # arguments: (output)
# pout - a structure containing a polynomial regression model which
#           describes the partial derivative with respect to variable #i.
    
    # Note:
# Polydern modifies the "ModelTerms" and "Coefficients" fields in creating
# the output polynomial. ParameterVar, parameterStd are also updated to
# have the proper shape, as well as scaling them to reflect the derivative.
    
    # The other fields (R2, RMSE, VarNames) are copied without change, even
# though the error measures are no longer meaningful for the derivative
# polynomial.
    
    # This function uses polynomial structure variables created by polyfitn,
# which is part of the PolyfitnTools package by John D'Errico:
#     http://www.mathworks.com/matlabcentral/fileexchange/10065
    
    # See also: polyder, polyfitn, polyvaln
    
    # Polydern author: Jason Goodman
# Error checks, ParameterStd/Var updates and allowance for the variable
# name itself instead of an index added by John D'Errico
    
    # check the number of input args
    if len(varargin) != 2:
        raise Exception('POLYDERN:argumentcount','Exactly two arguments are required')
    
    # is p a struct, created by polyfitn?
    if not isstruct(p)  or not isfield(p,'ModelTerms')  or not isfield(p,'Coefficients') :
        raise Exception('POLYDERN:invalidp','p must be a struct as created by polyfitn')
    
    # check diffvar too. scalar, numeric, integer, real, in the proper range,
# or it must be character, an exact match for one of the variables listed
# in p.VarNames.
    if ischar(diffvar):
        ind = ismember(p.VarNames,diffvar)
        if sum(ind) == 1:
            # we have a hit
            diffvar = find(ind)
        else:
            raise Exception('POLYDERN:invaliddiffvar','diffvar must be a scalar numeric real integer value, or a valid variable name')
    else:
        if not isnumeric(diffvar)  or (np.asarray(diffvar).size != 1) or (np.round(diffvar) != diffvar) or not True :
            # diffvar must be scalar, numeric, etc. Also verify that it is real to
# be complete
            raise Exception('POLYDERN:invaliddiffvar','diffvar must be a scalar numeric real integer value, or a valid variable name')
        else:
            if (diffvar < 1) or (diffvar > p.ModelTerms.shape[2-1]):
                # test that diffvar is at least 1, and is not larger than the
# number of variables in the nmodel
                raise Exception('POLYDERN:invaliddiffvar',np.array(['diffvar (=',num2str(diffvar),') cannot represent the variable index to be differentiated, as it is out of range for this model']))
    
    pout = p
    pout.ModelTerms = []
    pout.Coefficients = []
    remainingterms = True(1,p.ModelTerms.shape[1-1])
    jout = 1
    for jin in np.arange(1,len(p.Coefficients)+1).reshape(-1):
        if (p.ModelTerms(jin,diffvar) != 0):
            pout.Coefficients[jout] = np.multiply(p.Coefficients(jin),p.ModelTerms(jin,diffvar))
            pout.ModelTerms[jout,:] = p.ModelTerms(jin,:)
            pout.ModelTerms[jout,diffvar] = pout.ModelTerms(jout,diffvar) - 1
            jout = jout + 1
        else:
            # this term got dropped from the model
            remainingterms[jin] = False
    
    if (jout == 1):
        ncoeff,nvars = p.ModelTerms.shape
        pout.ModelTerms[1,:] = np.zeros((1,nvars))
        pout.Coefficients = 0
        pout.ParameterVar = 0
        pout.ParameterStd = 0
    else:
        # at least some terms remain, so update the parameter variances and
# standard deviations. First, drop those terms that died.
        pout.ParameterVar = reshape(p.ParameterVar(remainingterms),1,[])
        pout.ParameterStd = reshape(p.ParameterStd(remainingterms),1,[])
        # scale them appropriately. Thus if std(A) is sigma, then std(k*A)
# is k*sigma, but multiply the corresponding variances by k.^2.
        scale = np.transpose(p.ModelTerms(remainingterms,diffvar))
        pout.ParameterStd = np.multiply(pout.ParameterStd,scale)
        pout.ParameterVar = np.multiply(pout.ParameterVar,scale ** 2)
    
    return pout