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


class OptimalValues(db.Model):
  """Models an individual Configuration entry with an author, OptimalPeRatio, and date."""
  author = db.UserProperty()
  peRatio = db.StringProperty()
  pegRatio = db.StringProperty()
  debt = db.StringProperty()
  debtToEquity = db.StringProperty()
  qRevGrowth = db.StringProperty()
  divYield = db.StringProperty()
  beta = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  configType = db.StringProperty(default='Growth')


def OptimalValues_key(author):
#  """Constructs a datastore key for a Optimal Values entity with user name."""
  return db.Key.from_path('OptimalValues', author)


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

# Filter the results by type
def getOptimalValuesFromDataStore(type):
    optimalValue=None
    
    current_user=users.get_current_user()
    # Form the query to retrieve the entries for a user
    optimalValues_query = OptimalValues.all()
    optimalValues_query.filter('author', current_user )
    optimalValues_query.filter('configType =', type)

    count = optimalValues_query.count()
    # Fetch the result from the datastore
    optimalValues_result = optimalValues_query.fetch(1)
    logging.debug( 'count is %s ', count )
    
    for ov in optimalValues_result:
       optimalValue = ov

    return optimalValue

   

# Gets all the Optimal Values for a User
def getAllOptimalValuesFromDataStore():
    optimalValues=None
    
    current_user=users.get_current_user()
    # Form the query to retrieve the entries for a user
    optimalValues_query = OptimalValues.all()
    optimalValues_query.filter('author', current_user )
    optimalValues_query.order('configType')

    count = optimalValues_query.count()
    # Fetch the result from the datastore
    fetched = optimalValues_query.fetch(100)

    logging.debug( 'Count is %s ', count) 
    templateValues = {
      'optimalValues': fetched,
      'count': count
      }

    return templateValues, count
