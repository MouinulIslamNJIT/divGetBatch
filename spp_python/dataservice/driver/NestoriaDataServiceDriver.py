import numpy as np
import os

class NestoriaDataServiceDriver():
    #NESTORIADATASERVICEDRIVER Summary of this class goes here
    #   Detailed explanation goes here
    

        
    def __init__(this = None,requestParameters = None): 
        if len(varargin) == 1:
            NestoriaURL = 'http://api.nestoria.co.uk/api?action=search_listings&encoding=xml'
            this.URL = strcat(NestoriaURL,'&listing_type=',requestParameters.listingType,'&property_type=all&price_max=',num2str(requestParameters.priceMax),'&price_min=',num2str(requestParameters.priceMin),'&room_min=0&sort=',requestParameters.sortingMode)
            this.coordNorthEast = requestParameters.coordNorthEast
            this.coordSouthWest = requestParameters.coordSouthWest
            # total number of feature vectors
            response = retrieveResponse(this,1,strcat('&south_west=',this.coordSouthWest,'&north_east=',this.coordNorthEast))
            try:
                this.numFeatureVectors = str2double(response.getAttributes.getNamedItem('total_results').getValue)
            finally:
                pass
            this.reset()
        
        return
        
        
    def getNumFeatureVectors(this = None): 
        numFeatureVectors = this.numFeatureVectors
        return numFeatureVectors
        
        
    def getFeatureVectorsDimensions(this = None): 
        featureVectorsDimensions = 2
        return featureVectorsDimensions
        
        
    def accessByScore(this = None,sDepth = None,Ms = None): 
        if sDepth >= this.numFeatureVectors():
            objects = []
            scores = []
            return objects,scores
        
        additionalParameters = strcat('&south_west=',this.coordSouthWest,'&north_east=',this.coordNorthEast)
        while (sDepth + Ms) >= this.objectsByScore.shape[1-1]:
    
            this.retrievedPagesByScore = this.retrievedPagesByScore + 1
            newObjects,newScores = retrievePage(this,this.retrievedPagesByScore,additionalParameters)
            if len(newObjects)==0:
                this.numFeatureVectors = len(this.objectsByScore) + len(newScores)
                break
            this.objectsByScore = np.array([[this.objectsByScore],[newObjects]])
            this.scoresByScore = np.array([[this.scoresByScore],[newScores]])
    
        
        if sDepth + Ms <= this.numFeatureVectors():
            objects = this.objectsByScore(np.arange(sDepth + 1,sDepth + Ms+1),:)
            scores = this.scoresByScore(np.arange(sDepth + 1,sDepth + Ms+1))
        else:
            objects = this.objectsByScore(np.arange(sDepth + 1,end()+1),:)
            scores = this.scoresByScore(np.arange(sDepth + 1,end()+1),:)
        
        # score normalization
        if sDepth + Ms == 1:
            this.priceMin = scores
        
        scores = this.priceMin / scores
        return objects,scores
        
        
    def batchedAccess(this = None,vertices = None,radii = None): 
        objects = []
        scores = []
        numVertices = vertices.shape[1-1]
        for i in np.arange(1,numVertices+1).reshape(-1):
            currentPage = 0
            additionalParameters = strcat('&centre_point=',num2str(vertices(i,1)),',',num2str(vertices(i,2)),',',num2str(radii(i)),'km')
            while 1:
    
                currentPage = currentPage + 1
                newObjects,newScores = retrievePage(this,currentPage,additionalParameters)
                if len(newObjects)==0:
                    break
                else:
                    objects = np.array([[objects],[newObjects]])
                    scores = np.array([[scores],[newScores]])
    
        
        return objects,scores
        
        
    def accessByDistance(this = None,vertex = None,numNearestNeighbors = None): 
        objects = []
        scores = []
        currentPage = 0
        additionalParameters = strcat('&centre_point=',num2str(vertex(1)),',',num2str(vertex(2)))
        radius = 2
        while objects.shape[1-1] < numNearestNeighbors:
    
            currentPage = currentPage + 1
            newObjects,newScores = retrievePage(this,currentPage,strcat(additionalParameters,',',num2str(radius),'km'))
            objects = np.array([[objects],[newObjects]])
            scores = np.array([[scores],[newScores]])
            radius = radius + 2
    
        
        objects = objects(np.arange(1,numNearestNeighbors+1),:)
        scores = scores(np.arange(1,numNearestNeighbors+1))
        return objects,scores
        
        
    def reset(this = None): 
        this.objectsByScore = []
        this.scoresByScore = []
        this.retrievedPagesByScore = 0
        return
        
        
    def retrievePage(this = None,page = None,additionalParameters = None): 
        objects = []
        scores = []
        response = retrieveResponse(this,page,additionalParameters)
        numListings = response.getChildNodes.getLength
        child = response.getFirstChild
        for i in np.arange(1,numListings+1).reshape(-1):
            if str(child.getNodeName) == str('listings'):
                try:
                    latitude = str2double(child.getAttributes.getNamedItem('latitude').getValue)
                    longitude = str2double(child.getAttributes.getNamedItem('longitude').getValue)
                    price = str2double(child.getAttributes.getNamedItem('price').getValue)
                    objects = np.array([[objects],[latitude,longitude]])
                    scores = np.array([[scores],[price]])
                finally:
                    pass
            child = child.getNextSibling
        
        return objects,scores
        
        
    def retrieveResponse(this = None,page = None,additionalParameters = None): 
        if len(varargin) == 2:
            additionalParameters = ''
        
        tempfile = 'file.xml'
        newPageURL = strcat(this.URL,'&page=',num2str(page),additionalParameters)
        urlwrite(newPageURL,tempfile)
        f = open(tempfile,'r','l','ISO-8859-1')
        strResponse = np.transpose(fread(f,'*char'))
        f.close()
        os.delete(tempfile)
        try:
            documentBuilder = javax.xml.parsers.DocumentBuilderFactory.newInstance()
            xmlResponse = documentBuilder.newDocumentBuilder.parse(java.io.StringBufferInputStream(strResponse))
        finally:
            pass
        
        response = xmlResponse.getChildNodes.item(0).getChildNodes.item(3)
        return response
        