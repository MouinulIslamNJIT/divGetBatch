import numpy as np
    
def polyvaln(polymodel = None,indepvar = None): 
    # polyvaln: evaluates a polynomial model as a function of its variables
# usage: ypred = polyvaln(polymodel,indepvar)
    
    # arguments: (input)
#  indepvar - (n x p) array of independent variables as columns
#        n is the number of data points to evaluate
#        p is the dimension of the independent variable space
    
    #        IF n == 1, then I will assume there is only a
#        single independent variable.
    
    #  polymodel - A structure containing a regression model from polyfitn
#        polymodel.ModelTerms = list of terms in the model
#        polymodel.Coefficients = regression coefficients
    
    #        Note: A polymodel can be evaluated for any set of
#        values with the function polyvaln. However, if you
#        wish to manipulate the result symbolically using my
#        own sympoly tools, this structure should be converted
#        to a sympoly using the function polyn2sympoly.
    
    # Arguments: (output)
#  ypred - nx1 vector of predictions through the model.
    
    
    # See also: polyfitn, polyfit, polyval, polyn2sympoly, sympoly
    
    # Author: John D'Errico
# Release: 1.0
# Release date: 2/19/06
    
    # get the size of indepvar
    n,p = indepvar.shape
    if (n == 1) and (polymodel.ModelTerms.shape[2-1] == 1):
        indepvar = np.transpose(indepvar)
        n,p = indepvar.shape
    else:
        if (polymodel.ModelTerms.shape[2-1] != p):
            raise Exception('Size of indepvar array and this model are inconsistent.')
    
    # Evaluate the model
    nt = polymodel.ModelTerms.shape[1-1]
    ypred = np.zeros((n,1))
    for i in np.arange(1,nt+1).reshape(-1):
        t = np.ones((n,1))
        for j in np.arange(1,p+1).reshape(-1):
            t = np.multiply(t,indepvar(:,j) ** polymodel.ModelTerms(i,j))
        ypred = ypred + t * polymodel.Coefficients(i)
    
    return ypred