#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from gaeAnalyzeStock import *
import os
from google.appengine.ext.webapp import template
import yaml
from google.appengine.api import users
from google.appengine.ext import db
import logging
# New DAO
from tickerResultsNewDao import *
from optimalValuesDao import *
from urlparse import urlparse

# For Cloud Enpoints - Work in Progress - July 19, 2013
@endpoints.api(name='analyzeStock',version='v1',
               description='Sharath's Stock Analyzer')
class analyzeStock():
    def getRecommendation(ticker, configType):

        
        initializeStockAnalysis()
        
        #ticker=cgi.escape(self.request.get('ticker'))
        ticker= ticker.upper()
        logging.error('ticker is %s ' , ticker)
        
        #configType=cgi.escape(self.request.get('configType'))
        logging.error('configType is %s ' , configType)
        
        optimalValues=getOptimalValues( configType )
        if ( ticker != "" ):
                templateValues=getRecommendation(ticker, optimalValues)
        else:
                templateValues = {
                    'ticker': ticker,
                    'keyCount': 0,
                    'recommendation': "*** Please enter a valid Ticker ***",
            }

       

        #path = os.path.join(os.path.dirname(__file__), 'results.html')
        #self.response.out.write(template.render(path, templateValues))
        return templateValues;
        
    def getOptimalValues(type):
        initializeStockAnalysis()
        optimalValues=getOptimalValuesFromDataStore(type)
        
        # If OptimalValues are not found in DataStore then get from Configuration File.
        if not ( optimalValues):      
          optimalValues = OptimalValues()

          if users.get_current_user():
            optimalValues.author = users.get_current_user()

        
          optimalValues.peRatio=str ( getOptimalPeRatio() ) 
          optimalValues.pegRatio= str( getOptimalPegRatio() ) 
        
          optimalValues.debtToEquity= str( getOptimalDebtToEquity())
          optimalValues.qRevGrowth=str ( getOptimalQRevGrowth()) 
          optimalValues.divYield=str ( getOptimalYield() )
          optimalValues.beta=str ( getOptimalBeta() )
          optimalValues.configType= getOptimalType()

        return optimalValues
        






