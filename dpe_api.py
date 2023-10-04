"""
.. module:: aqms_api
   :platform: Unix
   :synopsis: Everything needed to use the api to query aqms.

.. moduleauthor:: Xavier Barthelemy <xavier.barthelemy@environment.nsw.gov.au>


"""
import os
import sys
import requests
import logging
import urllib
import datetime as dt
import json
###########################################################################################
class aqms_api_class(object):
    """
    This class defines and configures the api to query the aqms database
    """
    def __init__(self, ): 

        self.logger = logging.getLogger(__file__)
        self.url_api = "https://dpe-im-api-airquality-uat.azurewebsites.net"
        self.headers = {'content-type': 'application/json', 'accept': 'application/json'}
        
        self.get_site_url = 'api/Data/get_SiteDetails'
        self.get_parameters = 'api/Data/get_ParameterDetails'
        self.get_observations = 'api/Data/get_Observations'  
        return

###########################################################################################
    def get_site_details(self, ):
        '''
        Build a query to return all the sites details
        '''
        query = urllib.parse.urljoin(self.url_api, self.get_site_url)
        #print(query)
        response = requests.post(url = query, data = '')
        return response

###########################################################################################
    def get_parameters_details(self, ):
        '''
        Build a query to return all the sites details
        '''
        query = urllib.parse.urljoin(self.url_api, self.get_parameters)
        #print(query)
        response = requests.post(url = query, data = '')
        return response

###########################################################################################
    def get_Obs(self, ObsRequest):
        '''
        Build a query to return all the sites details
        '''
        query = urllib.parse.urljoin(self.url_api, self.get_observations)
        
        response = requests.post(url = query, data = json.dumps(ObsRequest), headers = self.headers)
        return response

###########################################################################################
    def ObsRequest_init(self, ):
        '''
        Build a empty dictionary to ready to post to get the obs
        '''
        ObsRequest = {}
        ObsRequest['Parameters'] = []
        ObsRequest['Sites'] = []
        ObsRequest['StartDate'] = ''
        ObsRequest['EndDate'] = ''
        ObsRequest['Categories'] = []
        ObsRequest['SubCategories'] = []
        ObsRequest['Frequency'] = []
        
        return ObsRequest

###########################################################################################

if __name__ == '__main__':    
    AQMS =  aqms_api_class()
    
    ObsRequest = AQMS.ObsRequest_init()
    StartDate = dt.datetime(2020,1,1,12)
    EndDate = dt.datetime(2020,1,2,12)
    
    AllSites = AQMS.get_site_details()
    #print(AllSites)
    for i, site in enumerate(AllSites.json()):
        #print(i, site)
        ObsRequest['Sites'].append(site['Site_Id'])
    
    Allparameters = AQMS.get_parameters_details()
    for i, param in enumerate(Allparameters.json()):
        #print(i, param)
        ObsRequest['Parameters'].append(param['ParameterCode'])
        ObsRequest['Categories'].append(param['Category'])
        ObsRequest['SubCategories'].append(param['SubCategory'])
        ObsRequest['Frequency'].append(param['Frequency'])
    
    #make all list unique
    ObsRequest['Parameters'] = list(set(ObsRequest['Parameters']))
    ObsRequest['Categories'] = list(set(ObsRequest['Categories']))
    ObsRequest['SubCategories'] = list(set(ObsRequest['SubCategories']))
    ObsRequest['Frequency'] = list(set(ObsRequest['Frequency']))
    
    ObsRequest['StartDate'] = StartDate.strftime('%Y-%m-%d')
    ObsRequest['EndDate'] = EndDate.strftime('%Y-%m-%d')
    
    AllObs = AQMS.get_Obs({})
    #ObsRequest['Sites'] = [190]
    #ObsRequest['Parameters'] =  ['WDR']
    #ObsRequest['Categories'] =  ['Averages']
    #ObsRequest['SubCategories'] = ['Hourly']
    #ObsRequest['Frequency'] =  ['Hourly average']
    
    #AllObs = AQMS.get_Obs(ObsRequest)
    print(json.dumps(ObsRequest))
    #print(AllObs)
    
    for i, obs in enumerate(AllObs.json()):
        print(i, obs)
        
