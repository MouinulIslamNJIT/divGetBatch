import numpy as np
import warnings
import numpy.matlib
    
def polyfitn(indepvar = None,depvar = None,modelterms = None): 
    # polyfitn: fits a general polynomial regression model in n dimensions
# usage: polymodel = polyfitn(indepvar,depvar,modelterms)
    
    # Polyfitn fits a polynomial regression model of one or more
# independent variables, of the general form:
    
    #   z = f(x,y,...) + error
    
    # arguments: (input)
#  indepvar - (n x p) array of independent variables as columns
#        n is the number of data points
#        p is the dimension of the independent variable space
    
    #        IF n == 1, then I will assume there is only a
#        single independent variable.
    
    #  depvar   - (n x 1 or 1 x n) vector - dependent variable
#        length(depvar) must be n.
    
    #        Only 1 dependent variable is allowed, since I also
#        return statistics on the model.
    
    #  modelterms - defines the terms used in the model itself
    
    #        IF modelterms is a scalar integer, then it designates
#           the overall order of the model. All possible terms
#           up to that order will be employed. Thus, if order
#           is 2 and p == 2 (i.e., there are two variables) then
#           the terms selected will be:
    
    #              {constant, x, x^2, y, x*y, y^2}
    
    #           Beware the consequences of high order polynomial
#           models.
    
    #        IF modelterms is a (k x p) numeric array, then each
#           row of this array designates the exponents of one
#           term in the model. Thus to designate a model with
#           the above list of terms, we would define modelterms as
    
    #           modelterms = [0 0;1 0;2 0;0 1;1 1;0 2]
    
    #        If modelterms is a character string, then it will be
#           parsed as a list of terms in the regression model.
#           The terms will be assume to be separated by a comma
#           or by blanks. The variable names used must be legal
#           matlab variable names. Exponents in the model may
#           may be any real number, positive or negative.
    
    #           For example, 'constant, x, y, x*y, x^2, x*y*y'
#           will be parsed as a model specification as if you
#           had supplied:
#           modelterms = [0 0;1 0;0 1;1 1;2 0;1 2]
    
    #           The word 'constant' is a keyword, and will denote a
#           constant terms in the model. Variable names will be
#           sorted in alphabetical order as defined by sort.
#           This order will assign them to columns of the
#           independent array. Note that 'xy' will be parsed as
#           a single variable name, not as the product of x and y.
    
    #        If modelterms is a cell array, then it will be taken
#           to be a list of character terms. Similarly,
    
    #           {'constant', 'x', 'y', 'x*y', 'x^2', 'x*y^-1'}
    
    #           will be parsed as a model specification as if you
#           had supplied:
    
    #           modelterms = [0 0;1 0;0 1;1 1;2 0;1 -1]
    
    # Arguments: (output)
#  polymodel - A structure containing the regression model
#        polymodel.ModelTerms = list of terms in the model
#        polymodel.Coefficients = regression coefficients
#        polymodel.ParameterVar = variances of model coefficients
#        polymodel.ParameterStd = standard deviation of model coefficients
#        polymodel.R2 = R^2 for the regression model
#        polymodel.AdjustedR2 = Adjusted R^2 for the regression model
#        polymodel.RMSE = Root mean squared error
#        polymodel.VarNames = Cell array of variable names
#           as parsed from a char based model specification.
    
    #        Note 1: Because the terms in a general polynomial
#        model can be arbitrarily chosen by the user, I must
#        package the erms and coefficients together into a
#        structure. This also forces use of a special evaluation
#        tool: polyvaln.
    
    #        Note 2: A polymodel can be evaluated for any set
#        of values with the function polyvaln. However, if
#        you wish to manipulate the result symbolically using
#        my own sympoly tools, this structure can be converted
#        to a sympoly using the function polyn2sympoly.
    
    #        Note 3: When no constant term is included in the model,
#        the traditional R^2 can be negative. This case is
#        identified, and then a more appropriate computation
#        for R^2 is then used.
    
    #        Note 4: Adjusted R^2 accounts for changing degrees of
#        freedom in the model. It CAN be negative, and will always
#        be less than the traditional R^2 values.
    
    # Find my sympoly toolbox here:
# http://www.mathworks.com/matlabcentral/fileexchange/loadFile.do?objectId=9577&objectType=FILE
    
    # See also: polyvaln, polyfit, polyval, polyn2sympoly, sympoly
    
    # Author: John D'Errico
# Release: 2.0
# Release date: 2/19/06
    
    if len(varargin) < 1:
        help('polyfitn')
        return polymodel
    
    # get sizes, test for consistency
    n,p = indepvar.shape
    if n == 1:
        indepvar = np.transpose(indepvar)
        n,p = indepvar.shape
    
    m,q = depvar.shape
    if m == 1:
        depvar = np.transpose(depvar)
        m,q = depvar.shape
    
    # only 1 dependent variable allowed at a time
    if q != 1:
        raise Exception('Only 1 dependent variable allowed at a time.')
    
    if n != m:
        raise Exception('indepvar and depvar are of inconsistent sizes.')
    
    # Automatically scale the independent variables to unit variance
    stdind = np.sqrt(diag(cov(indepvar)))
    if np.any(stdind == 0):
        warnings.warn('Constant terms in the model must be entered using modelterms')
        stdind[stdind == 0] = 1
    
    # scaled variables
    indepvar_s = indepvar * diag(1.0 / stdind)
    # do we need to parse a supplied model?
    if iscell(modelterms) or ischar(modelterms):
        modelterms,varlist = parsemodel(modelterms,p)
        if modelterms.shape[2-1] < p:
            modelterms = np.array([modelterms,np.zeros((modelterms.shape[1-1],p - modelterms.shape[2-1]))])
    else:
        if len(modelterms) == 1:
            # do we need to generate a set of modelterms?
            modelterms,varlist = buildcompletemodel(modelterms,p)
        else:
            if modelterms.shape[2-1] != p:
                raise Exception('ModelTerms must be a scalar or have the same # of columns as indepvar')
    
    nt = modelterms.shape[1-1]
    # check for replicate terms
    if nt > 1:
        mtu = unique(modelterms,'rows')
        if mtu.shape[1-1] < nt:
            warnings.warn('Replicate terms identified in the model.')
    
    # build the design matrix
    M = np.ones((n,nt))
    scalefact = np.ones((1,nt))
    for i in np.arange(1,nt+1).reshape(-1):
        for j in np.arange(1,p+1).reshape(-1):
            M[:,i] = np.multiply(M(:,i),indepvar_s(:,j) ** modelterms(i,j))
            scalefact[i] = scalefact(i) / (stdind(j) ** modelterms(i,j))
    
    # estimate the model using QR. do it this way to provide a
# covariance matrix when all done. Use a pivoted QR for
# maximum stability.
    Q,R,E = qr(M,0)
    polymodel.ModelTerms = modelterms
    polymodel.Coefficients[E] = np.linalg.solve(R,(np.transpose(Q) * depvar))
    yhat = M * polymodel.Coefficients
    # recover the scaling
    polymodel.Coefficients = np.multiply(polymodel.Coefficients,scalefact)
    # variance of the regression parameters
    s = norm(depvar - yhat)
    if n > nt:
        Rinv = np.linalg.solve(R,np.eye(nt))
        Var[E] = s ** 2 * np.sum(Rinv ** 2, 2-1) / (n - nt)
        polymodel.ParameterVar = np.multiply(Var,(scalefact ** 2))
        polymodel.ParameterStd = np.sqrt(polymodel.ParameterVar)
    else:
        # we cannot form variance or standard error estimates
# unless there are at least as many data points as
# parameters to estimate.
        polymodel.ParameterVar = inf(1,nt)
        polymodel.ParameterStd = inf(1,nt)
    
    # R^2
# is there a constant term in the model? If not, then
# we cannot use the standard R^2 computation, as it
# frequently yields negative values for R^2.
    if np.any(np.logical_and((M(1,:) != 0),np.all(np.diff(M,1,1) == 0,1))):
        # we have a constant term in the model, so the
# traditional #R^2 form is acceptable.
        polymodel.R2 = np.amax(0,1 - (s / norm(depvar - mean(depvar))) ** 2)
        # compute adjusted R^2, taking into account the number of
# degrees of freedom
        polymodel.AdjustedR2 = 1 - np.multiply((1 - polymodel.R2),((n - 1) / (n - nt)))
    else:
        # no constant term was found in the model
        polymodel.R2 = np.amax(0,1 - (s / norm(depvar)) ** 2)
        # compute adjusted R^2, taking into account the number of
# degrees of freedom
        polymodel.AdjustedR2 = 1 - np.multiply((1 - polymodel.R2),(n / (n - nt)))
    
    # RMSE
    polymodel.RMSE = np.sqrt(mean((depvar - yhat) ** 2))
    # if a character 'model' was supplied, return the list
# of variables as parsed out
    polymodel.VarNames = varlist
    # ==================================================
# =============== begin subfunctions ===============
# ==================================================
    
def buildcompletemodel(order = None,p = None): 
    
    # arguments: (input)
#  order - scalar integer, defines the total (maximum) order
    
    #  p     - scalar integer - defines the dimension of the
#          independent variable space
    
    # arguments: (output)
#  modelterms - exponent array for the model
    
    #  varlist - cell array of character variable names
    
    # build the exponent array recursively
    if p == 0:
        # terminal case
        modelterms = []
    else:
        if (order == 0):
            # terminal case
            modelterms = np.zeros((1,p))
        else:
            if (p == 1):
                # terminal case
                modelterms = np.transpose((np.arange(order,0+- 1,- 1)))
            else:
                # general recursive case
                modelterms = np.zeros((0,p))
                for k in np.arange(order,0+- 1,- 1).reshape(-1):
                    t = buildcompletemodel(order - k,p - 1)
                    nt = t.shape[1-1]
                    modelterms = np.array([[modelterms],[np.array([np.matlib.repmat(k,nt,1),t])]])
    
    # create a list of variable names for the variables on the fly
    varlist = cell(1,p)
    for i in np.arange(1,p+1).reshape(-1):
        varlist[i] = np.array(['X',num2str(i)])
    
    # ==================================================
    
def parsemodel(model = None,p = None): 
    
    # arguments: (input)
#  model - character string or cell array of strings
    
    #  p     - number of independent variables in the model
    
    # arguments: (output)
#  modelterms - exponent array for the model
    
    modelterms = np.zeros((0,p))
    if ischar(model):
        model = deblank(model)
    
    varlist = np.array([])
    while not len(model)==0 :

        if iscellstr(model):
            term = model[0]
            model[1] = []
        else:
            term,model = strtok(model,' ,')
        # We've stripped off a model term. Now parse it.
        # Is it the reserved keyword 'constant'?
        if strcmpi(term,'constant'):
            modelterms[end() + 1,:] = 0
        else:
            # pick this term apart
            expon = np.zeros((1,p))
            while not len(term)==0 :

                vn = strtok(term,'*/^. ,')
                k = find(strncmp(vn,varlist,len(vn)))
                if len(k)==0:
                    # its a variable name we have not yet seen
                    # is it a legal name?
                    nv = len(varlist)
                    if ismember(vn(1),'1234567890_'):
                        raise Exception(np.array(['Variable is not a valid name: '',vn,''']))
                    else:
                        if nv >= p:
                            raise Exception('More variables in the model than columns of indepvar')
                    varlist[nv + 1] = vn
                    k = nv + 1
                # variable must now be in the list of vars.
                # drop that variable from term
                i = strfind(term,vn)
                term = term(np.arange((i + len(vn)),end()+1))
                # is there an exponent?
                eflag = False
                if strncmp('^',term,1):
                    term[1] = []
                    eflag = True
                else:
                    if strncmp('.^',term,2):
                        term[np.arange[1,2+1]] = []
                        eflag = True
                # If there was one, get it
                ev = 1
                if eflag:
                    ev = sscanf(term,'%f')
                    if len(ev)==0:
                        raise Exception('Problem with an exponent in parsing the model')
                expon[k] = expon(k) + ev
                # next monomial subterm?
                k1 = strfind(term,'*')
                if len(k1)==0:
                    term = ''
                else:
                    term[k1[1]] = ' '

            modelterms[end() + 1,:] = expon

    
    # Once we have compiled the list of variables and
# exponents, we need to sort them in alphabetical order
    varlist,tags = __builtint__.sorted(varlist)
    modelterms = modelterms(:,tags)
    return polymodel