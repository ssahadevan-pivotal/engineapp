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
from gaeAnalyzeFund import *
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
from getMacroData import *;
DEBUG=False;

def getTemplateValues():
        #Defaults to Growth for now
        optimalValues=getOptimalValues("Growth")   
        # Set the Optimal Values in the template
        templateValues = {
            'optimalPeRatio': optimalValues.peRatio,
            'optimalPegRatio': optimalValues.pegRatio,
            'optimalDebtToEquity': optimalValues.debtToEquity,
            'optimalYield': optimalValues.divYield,
            'optimalQRevGrowth': optimalValues.qRevGrowth,
            'optimalBeta': optimalValues.beta,
            'optimalType': optimalValues.configType,
        }
        return templateValues

# Get the target URL, without parameters, April 2012
# User by history and discover
def getTargetUrl(uri):
        targetUrl= uri.split('?');
        #logging.error('targetURl is %s ' ,  targetUrl[0]);
        return targetUrl[0];

  
class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        # Commented Out
        #if user is None:
        #    self.redirect(users.create_login_url(self.request.uri))
            
        
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        templateValues,count=getAllOptimalValuesFromDataStore()
        count = int ( count )
        
        if (count < 1):
                initialize("Growth")
                initialize("Income")
                initialize("Value")

        templateValues,count=getAllOptimalValuesFromDataStore()
        self.response.out.write(template.render(path, templateValues))


class configure(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        # Commented out for now
        if user is None:
            self.redirect(users.create_login_url(self.request.uri))

        path = os.path.join(os.path.dirname(__file__), 'configure.html')
        templateValues,count=getAllOptimalValuesFromDataStore()
        self.response.out.write(template.render(path, templateValues))


class discover(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        # Commented out for now
        #if user is None:
            #self.redirect(users.create_login_url(self.request.uri))
       
        path = os.path.join(os.path.dirname(__file__), 'discover.html')
        page=self.request.get("page", default_value="1");
        page=int(page);

        #targetUrl= (self.request.uri).split('?');
        #logging.error('targetURl is %s ' ,  targetUrl[0]);
        
        templateValues=getDiscoverResultsNew(page,  getTargetUrl(self.request.uri) )
        self.response.out.write(template.render(path, templateValues))


class history(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        # Commented out for now
        #if user is None:
        #    self.redirect(users.create_login_url(self.request.uri))
       
        path = os.path.join(os.path.dirname(__file__), 'history.html')
        page=self.request.get("page", default_value="1");
        page=int(page);
                    
        templateValues=getAllTickerResultsNew(page,  getTargetUrl(self.request.uri) )
        self.response.out.write(template.render(path, templateValues))


class filterHistory(webapp.RequestHandler):
    def get(self):
        defaultTicker="None";
        
        user = users.get_current_user();

        #Get the ticker
        ticker=cgi.escape(self.request.get('ticker'));
        ticker= ticker.upper();
        #logging.error('ticker is %s ' , ticker);
        if (ticker == ""):
                ticker=defaultTicker;

        # Commented out for now
        #if user is None:
        #    self.redirect(users.create_login_url(self.request.uri))
       
        path = os.path.join(os.path.dirname(__file__), 'filterHistory.html')
        page=self.request.get("page", default_value="1");
        page=int(page);
                     
        templateValues=getHistoryByRecommendation(page,  getTargetUrl(self.request.uri), ticker, "BUY" )
        self.response.out.write(template.render(path, templateValues))

    def post(self):
        defaultTicker="MA";
        
        user = users.get_current_user();

        #Get the ticker
        ticker=cgi.escape(self.request.get('ticker'));
        ticker= ticker.upper();
        #logging.error('ticker is %s ' , ticker);
        if (ticker == ""):
                ticker=defaultTicker;
      

        # Commented out for now
        #if user is None:
        #    self.redirect(users.create_login_url(self.request.uri))
       
        path = os.path.join(os.path.dirname(__file__), 'filterHistory.html')
        page=self.request.get("page", default_value="1");
        page=int(page);
                    
        templateValues=getHistoryByTicker(page,  getTargetUrl(self.request.uri), ticker )
        self.response.out.write(template.render(path, templateValues))


class getMacroEconData(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.error('in macroData ');
        # Commented out for now
        #if user is None:
        #    self.redirect(users.create_login_url(self.request.uri))
       
        path = os.path.join(os.path.dirname(__file__), 'macroData.html')
        page=self.request.get("page", default_value="1");
        page=int(page);
                    
        keyStats, count= getMacroData(DEBUG);
        
        caseShillerPe=float ( getValueFromKey( keyStats, "CurrentShiller PE Ratio") );
        max=float ( getValueFromKey( keyStats, "Max:") );
        min=float ( getValueFromKey( keyStats, "Min:") );
        mean=float ( getValueFromKey( keyStats, "Mean:") );
        templateValues = {
                        'caseShillerPe': caseShillerPe ,
                        'max': max ,
                        'min': min ,
                        'mean': mean ,
                        'keyCount': count
                        }
        self.response.out.write(template.render(path, templateValues))            

class submitTicker(webapp.RequestHandler):
    def post(self):

        
        initializeStockAnalysis()
        
        ticker=cgi.escape(self.request.get('ticker'))
        ticker= ticker.upper()
        #logging.error('ticker is %s ' , ticker)

        #Get the tickerType
        tickerType=cgi.escape(self.request.get('tickerType'));
        #logging.error('tickerType is %s ' , tickerType);
        
        configType=cgi.escape(self.request.get('configType'))
        #logging.error('configType is %s ' , configType)
        
        optimalValues=getOptimalValues( configType )
        if ( ticker != "" ):
                if ( tickerType == "Stock" ):
                        templateValues=getRecommendation(ticker, optimalValues);
                elif ( tickerType == "MutualFund"):
                        templateValues=getRecommendationForFund(ticker, optimalValues);
                        #
                        #templateValues = {
                        #'ticker': ticker,
                        #'keyCount': 0,
                        #'recommendation': "*** This is a MutualFund ***",
                        #}
                
        else:
                templateValues = {
                    'ticker': ticker,
                    'keyCount': 2,
                    'recommendation': "*** Please enter a valid Ticker ***",
            }

        templateValues["tickerType"]=tickerType;
        #compareToTicker=cgi.escape(self.request.get('compareToTicker'))
        #compareToTemplateValues=getRecommendation(compareToTicker)

        path = os.path.join(os.path.dirname(__file__), 'results.html')
        self.response.out.write(template.render(path, templateValues))
        


class submitConfiguration(webapp.RequestHandler):
    def post(self):
        
        
        configType = cgi.escape(self.request.get('configType'))
        updatedValues=getOptimalValuesFromDataStore(configType)

        labelPeRatio='optimalPeRatio_' + configType
        labelPegRatio='optimalPegRatio_' + configType
        labelDebtToEquity='optimalDebtToEquity_' + configType
        labelQRevGrowth='optimalQRevGrowth_' + configType
        labelYield='optimalYield_' + configType
        labelBeta='optimalBeta_' + configType
        
        if (updatedValues):
            logging.error('submitConfiguration:*** Found optimal values in datastore for configType %s ', configType )
            updatedValues.peRatio=cgi.escape(self.request.get( labelPeRatio ))
            updatedValues.pegRatio=cgi.escape(self.request.get( labelPegRatio))
            updatedValues.debtToEquity=cgi.escape(self.request.get( labelDebtToEquity ))
            updatedValues.qRevGrowth=cgi.escape(self.request.get(labelQRevGrowth))
            updatedValues.divYield=cgi.escape(self.request.get(labelYield))
            updatedValues.beta=cgi.escape(self.request.get(labelBeta))
            updatedValues.configType=configType
        else:
            logging.error('submitConfiguration:*** Could not find values for user in datastore for configType %s ', configType)
            # Create an entry for the new user
            updatedValues=OptimalValues(author=users.get_current_user()
                                   ,peRatio=optimalPeRatio
                                   ,pegRatio=optimalPegRatio
                                   ,debtToEquity=cgi.escape(self.request.get('optimalDebtToEquity'))
                                   ,qRevGrowth=cgi.escape(self.request.get('optimalQRevGrowth'))
                                   ,divYield=cgi.escape(self.request.get('optimalYield'))
                                   ,beta=cgi.escape(self.request.get('optimalBeta'))
                                   ,configType=configType
                                   )

            
        # Write the updated values to the data store
        updatedValues.put()
        
  
       
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        templateValues,count=getAllOptimalValuesFromDataStore()
        self.response.out.write(template.render(path, templateValues))

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
        

# Adds the Type to the DB. Needed for the first time
def initialize(type):
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
          optimalValues.configType= type
          optimalValues.put()
        

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/configure', configure),
                                          ('/discover', discover),
                                          ('/history', history),
                                          ('/filterHistory', filterHistory),
                                          ('/getMacroEconData', getMacroEconData),
                                          ('/submitConfiguration', submitConfiguration),
                                          ('/submitTicker', submitTicker)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
