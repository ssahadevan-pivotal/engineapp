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

from google.appengine.api import memcache
from google.appengine.ext import db
import logging
from PagedQuery import *

class TickerResultsNew(db.Model):
  """Models the results for a ticker"""
  #author = db.UserProperty()
  optimalPeRatio = db.FloatProperty()
  optimalPegRatio = db.FloatProperty()
  #debt = db.FloatProperty()
  optimalDebtToEquity = db.FloatProperty()
  optimalQRevGrowth = db.FloatProperty()
  optimalDivYield = db.FloatProperty()
  optimalBeta = db.FloatProperty()
  
  price=db.FloatProperty()
  peRatio = db.FloatProperty()
  pegRatio = db.FloatProperty()
  #debt = db.FloatProperty()
  debtToEquity = db.FloatProperty()
  qRevGrowth = db.FloatProperty()
  divYield = db.FloatProperty()
  beta = db.FloatProperty()
 # priceToSales= db.FloatProperty()
 # priceToBook=db.FloatProperty()
 # bookValue=db.FloatProperty()
 # marketCap=db.FloatProperty()
  
  recommendation=db.StringProperty()
  ticker = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  configType=db.StringProperty(default='Growth')


def TickerResultsNew_key(date):
#  """Constructs a datastore key for a Optimal Values entity with the date key."""
  return db.Key.from_path('TickerResultsNew', date)

# get the Page Size
def getPageSize():
   PAGESIZE =20 ;
   return PAGESIZE ;
  
def getAllTickerResultsNew(page, uri ):
    tickerResults=None;
    pageSize=getPageSize();

    myPagedQuery = PagedQuery(TickerResultsNew.all(), pageSize)
    
    myPagedQuery.order('ticker')
    myPagedQuery.order('-date')
    

    count = myPagedQuery.count()
    page_count = myPagedQuery.page_count()
    
    fetched=None
    if page>1:
      fetched = myPagedQuery.fetch_page(page)
    else:
      fetched = myPagedQuery.fetch_page()
    

    next_page=None;
    prev_page=None;

    if (  myPagedQuery.has_page(page+1) ):
      next_page=page+1;
    if (  myPagedQuery.has_page(page-1) ):
      prev_page=page-1;
      
    
    
    templateValues = {
      'tickerResults': fetched,
      'count': count,
      'next_page':next_page,
      'prev_page':prev_page,
      'page_count':page_count,
      'targetUri':uri
      }

    
   # for t in fetched:
   #    tickerResults = t
   #    logging.error('Fetched values are ticker is %s and recommendation is  %s and Beta is %s ', t.ticker , t.recommendation , t.beta)
       
    logging.error( 'page Navigation links is %s %s', prev_page , next_page)
 
    return templateValues

# filter by qRevGroqth > 20
def getDiscoverResultsNew(page, uri ):
    tickerResults=None
    pageSize=getPageSize();

    myPagedQuery = PagedQuery(TickerResultsNew.all(), pageSize)
    myPagedQuery.filter('qRevGrowth > ', 20.00)

    myPagedQuery.order('-qRevGrowth')
    myPagedQuery.order('ticker')
    myPagedQuery.order('-date')
    

    count = myPagedQuery.count()
    page_count = myPagedQuery.page_count()
    
    fetched=None
    if page>1:
      fetched = myPagedQuery.fetch_page(page)
    else:
      fetched = myPagedQuery.fetch_page()
    

    next_page=None;
    prev_page=None;

    if (  myPagedQuery.has_page(page+1) ):
      next_page=page+1;
    if (  myPagedQuery.has_page(page-1) ):
      prev_page=page-1;
      
    
    
    templateValues = {
      'tickerResults': fetched,
      'count': count,
      'next_page':next_page,
      'prev_page':prev_page,
      'page_count':page_count,
      'targetUri':uri
      }

    
   # for t in fetched:
   #    tickerResults = t
   #    logging.error('Fetched values are ticker is %s and recommendation is  %s and Beta is %s ', t.ticker , t.recommendation , t.beta)
       
    logging.error( 'page Navigation links is %s %s', prev_page , next_page)
 
    return templateValues


# Filter by Ticker
def getHistoryByTicker(page, uri, ticker ):
    tickerResults=None
    pageSize=getPageSize();

    myPagedQuery = PagedQuery(TickerResultsNew.all(), pageSize)
    myPagedQuery.filter('ticker = ', ticker)

    myPagedQuery.order('ticker')
    myPagedQuery.order('-date')
    

    count = myPagedQuery.count()
    page_count = myPagedQuery.page_count()
    
    fetched=None
    if page>1:
      fetched = myPagedQuery.fetch_page(page)
    else:
      fetched = myPagedQuery.fetch_page()
    

    next_page=None;
    prev_page=None;

    if (  myPagedQuery.has_page(page+1) ):
      next_page=page+1;
    if (  myPagedQuery.has_page(page-1) ):
      prev_page=page-1;
      
    
    
    templateValues = {
      'ticker': ticker,
      'tickerResults': fetched,
      'count': count,
      'next_page':next_page,
      'prev_page':prev_page,
      'page_count':page_count,
      'targetUri':uri
      }

    
   # for t in fetched:
   #    tickerResults = t
   #    logging.error('Fetched values are ticker is %s and recommendation is  %s and Beta is %s ', t.ticker , t.recommendation , t.beta)
       
    logging.error( 'page Navigation links is %s %s', prev_page , next_page)
 
    return templateValues

# Filter by Recommendation -  Example: BUY only
def getHistoryByRecommendation(page, uri, ticker, recommendation ):
    tickerResults=None
    pageSize=getPageSize();

    myPagedQuery = PagedQuery(TickerResultsNew.all(), pageSize)
    myPagedQuery.filter('recommendation = ', recommendation)

    myPagedQuery.order('ticker')
    myPagedQuery.order('-date')
    

    count = myPagedQuery.count()
    page_count = myPagedQuery.page_count()
    
    fetched=None
    if page>1:
      fetched = myPagedQuery.fetch_page(page)
    else:
      fetched = myPagedQuery.fetch_page()
    

    next_page=None;
    prev_page=None;

    if (  myPagedQuery.has_page(page+1) ):
      next_page=page+1;
    if (  myPagedQuery.has_page(page-1) ):
      prev_page=page-1;
      
    
    
    templateValues = {
      'ticker': ticker,
      'tickerResults': fetched,
      'count': count,
      'next_page':next_page,
      'prev_page':prev_page,
      'page_count':page_count,
      'targetUri':uri
      }

    
   # for t in fetched:
   #    tickerResults = t
   #    logging.error('Fetched values are ticker is %s and recommendation is  %s and Beta is %s ', t.ticker , t.recommendation , t.beta)
       
    logging.error( 'page Navigation links is %s %s', prev_page , next_page)
 
    return templateValues

