import sys, math
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from getKeyStats import *
import yaml
import time
from datetime import datetime
import logging
from tickerResultsNewDao import *
import feedparser ;
from google.appengine.api import urlfetch;
from getNewsForTicker import *
from getAdditionalKeyStats import *


# Used to control Print statements
DEBUG=False;

#Load the config file
configFile="gaeAnalyzeStock.yaml"
configs=yaml.load( open( configFile ))

SELL="SELL"
BUY="BUY"


#Get the list of Tickers from Config File
def getTickers():
  tickerList=getValueFromConfigs("tickerList")
  if ( DEBUG ):
    print "Ticker list is " , tickerList
  return tickerList

def getValueFromConfigs(key):
  if ( DEBUG ):
    print "configs[ " , key , " ]=" , configs[key]
  return configs[key]

def getOptimalPeRatio():
  return  getValueFromConfigs("optimalPeRatio")

def getOptimalPegRatio():
  return  getValueFromConfigs("optimalPegRatio")

def getOptimalDebtToEquity():
  return  getValueFromConfigs( "optimalDebtToEquity")

def getOptimalQRevGrowth():
  return  getValueFromConfigs( "optimalQRevGrowth")

def getOptimalYield():
  return  getValueFromConfigs("optimalYield")

def getOptimalBeta():
  return  getValueFromConfigs("optimalBeta")

def getOptimalType():
  return getValueFromConfigs("optimalType")

def isBetaOptimal( actual, optimal ):
  if actual <= optimal:
     #logging.debug ('*** isBetaOptimal: actual is %s' , actual )
     return True
  else:
     #logging.debug ('*** isBetaOptimal: actual is %s' , actual )
     #logging.debug ('*** isBetaOptimal: optimal is %s' , optimal ) 
     return False

#Is the Company Fairly Valued
def isFairlyValued( actual, optimal ):
  if (actual > 0 and actual <= optimal ) :
     #logging.debug ('*** isFairlyValued: actual is %s' , actual )
     return True
  else:
     #logging.debug ('*** isFairlyValued: actual is %s' , actual )
     #logging.debug ('*** isFairlyValued: optimal is %s' , optimal ) 
     return False

# is the company Highly leveraged?
def isHighlyLevered( debtToEquity, optimalDebtToEquity):
  
  if ( debtToEquity=="N/A"):
    # No Debt
    return False
  else:
    if ( float( debtToEquity ) > optimalDebtToEquity ):
      #logging.debug( '*** DebtToEquity is greater than optimalDebtToEquity')
      return True
    else:
      return False
   

#Is a high Percentage company - Used for Growth and Yield. Pass in Key as 3rd arg
def isHighPct( pct, optimalPct, key ):
  
  # If set to optimalPct is set zero, return true.  This is an switch to skip this routine.
  if ( optimalPct == 0 ) or (optimalPct == 0.0):
    if (DEBUG):
      logging.error( '*** isHighPct: Ignoring %s' , key)
    return True
  
  if ( pct=="N/A") or ( pct == 0 ):
    # No Growth
    if (DEBUG):
      logging.error ('*** isHighPct: Key is %s' , key )
      logging.error ('*** isHighPct: pct is %s' , pct )
      logging.error ('*** isHighPct: optimalPct is %s' , optimalPct )
    return False

  # Strip out the %
  pct=pct.replace('%','')
  #optimalPct=optimalPct.replace('%','')
  if ( float(pct) >= float( optimalPct) ) : 
     return True
  else:
     if (DEBUG):
       logging.error ('*** isHighPct: Key is %s' , key )
       logging.error ('*** isHighPct: pct is %s' , pct )
       logging.error ('*** isHighPct: optimalPct is %s' , optimalPct )
     return False



def getRecommendation( ticker , optimalValues):
  recommendation="SELL"
 
  apiKey= getValueFromConfigs('API_KEY');
  
  #TBD - Might be able to remove this
  keyCount=0 ; 
  #keyStats ,keyCount, keys=getKeyStats(ticker,DEBUG)
  logging.error("getRecommendation:keycount is %s", keyCount );
  keyStats, keyCount=getKeyStats(ticker,DEBUG)
  logging.error("getRecommendation:keycount is %s", keyCount );

  
  additionalStockData = getAdditionalKeyStats(ticker,apiKey,DEBUG)
  #print additionalStockData
  
  # Set Optimal Valeues from Configs
  optimalPeRatio=float ( optimalValues.peRatio )
  optimalPegRatio=float ( optimalValues.pegRatio )
  optimalDebt=optimalValues.debt
  optimalDebtToEquity=float ( optimalValues.debtToEquity )
  optimalQRevGrowth=float ( optimalValues.qRevGrowth )
  optimalYield=float ( optimalValues.divYield )
  optimalBeta=float ( optimalValues.beta )
  optimalType=optimalValues.configType
  
  pegRatio= 0.0
  debtToEquity=0.0
  qRevGrowth=0.0
  divYield=0.0
  eps=0.0
  pe=0.0
  price=0.0
  beta=0.0
  tickerName="Unknown"
  fiftyDayMovAvg=0.0;
  twoHundredDayMovAvg=0.0
  bookValue=0.0;
  marketCap=0.0;
  priceToSales=0.0;
  priceToBook=0.0;
  oneYearTarget=0.0;

  # For US Stocks & ADR's the expectedKeyCount is 16
  expectedKeyCount=10;
  isPeOk=False;
  isPegOk=False;
  isQRevGrowthOk=False;
  isDivYieldOk=False;
  isDebtOk=False;
  isOneYearTargetOk=False;
  if (keyCount >= expectedKeyCount ):
      #eps= keystats['Earnings Per Share (EPS)'];
      #eps=getValueFromKey (keyStats,  getValueFromConfigs('EPS_KEY') );
      #logging.error("eps is %s", eps );
      
      pe= getValueFromKey (keyStats,  getValueFromConfigs('PE_KEY') )  ;
      logging.error("pe is %s" ,pe);
      #pe=convertToFloat( getValueFromKey (keyStats,  getValueFromConfigs('PE_KEY') ) ) ;
      #if ( pe is None ):
      #  pe=0.0;
      #else:
      #  pe=float( pe );
        
      #price = getValueFromKey (keyStats,  getValueFromConfigs('PRICE_KEY') ) ;
      price = additionalStockData['Global Quote']['05. price'];
      change = additionalStockData['Global Quote']['09. change'];
      volumne = additionalStockData['Global Quote']['06. volume'];
      logging.error("Price is %s", price );

      oneYearTarget= getValueFromKey (keyStats,'1 Year Target');
      
      logging.error(" oneYearTarget is %s", oneYearTarget);

      if ( isFairlyValued(price, oneYearTarget)):
       recommendation=BUY;
       isOneYearTargetOk=True;
       
      tickerName = ticker;
      bookValue=convertToFloat( "0.0" );
      marketCap= getValueFromKey (keyStats, 'Market Cap' ) ; 
      priceToSales=convertToFloat( "0.0" );
      priceToBook=convertToFloat( "0.0" );
      
      pegRatio=convertToFloat( "0.0" );
      
      
      fiftyDayMovAvg= convertToFloat( "0.0" ) ;
      
      twoHundredDayMovAvg= convertToFloat( "0.0" ) ;
      
      if (DEBUG):
        print "pegRatio is ", pegRatio

      # If there is no debt, this works. If there is debt, say XOM fails because its says
      # string 3.6B etc
      #debtToEquity=getValueFromKey( keyStats , getValueFromConfigs("DEBT_TO_EQUITY_KEY") )
      debtToEquity= "7.0" ;
      if (DEBUG):
        print "debtToEquity is ", debtToEquity

      # Replace %. If NA value will be 0.
      #qRevGrowth=getValueFromKey( keyStats , getValueFromConfigs("Q_REV_GROWTH_KEY") )
      qRevGrowth="7.0";
      if (DEBUG):
        print "qRevGrowth is ", qRevGrowth

      # Replace %. If NA value will be 0.
      divYield=getValueFromKey( keyStats , getValueFromConfigs("YIELD_KEY") )
      if ( divYield is None ):
         divYield="0.0";
      #logging.error("divYield is %s", divYield);
      #beta=getValueFromKey( keyStats , getValueFromConfigs("BETA_KEY") )
      beta="7.0";

      if (DEBUG):
        print "pegRatio is ", pegRatio, " debtToEquity is ", debtToEquity, " qRevGrowth is ", qRevGrowth ," yield is ", divYield

      #logging.error('Before isFairlyValued:')
      if ( isFairlyValued(pe, optimalPeRatio)):
         isPeOk=True; 
         if ( isHighPct( divYield, optimalYield , getValueFromConfigs("YIELD_KEY"))):
            isDivYieldOk=True;
            logging.error('After isHighPct - Yield')
            recommendation=BUY
        
   

  #Currently not used because it slows the response. 
  title,link = getNewsForTicker(ticker);
  #news=""
  logging.debug( "getRecommendation: Title length is - %d", len(title)) ;
  
  templateValues = {
            'ticker': ticker,
            'tickerName': tickerName,
            'keyCount': keyCount,
            'expectedKeyCount':expectedKeyCount,
            'recommendation': recommendation,
            'price': price,
            'pe': pe,
            'pegRatio': pegRatio,
            'debtToEquity': debtToEquity,
            'qRevGrowth': qRevGrowth,
            'divYield': divYield,
            'beta':beta,
            'oneYearTarget': oneYearTarget,
            'fiftyDayMovAvg':fiftyDayMovAvg,
            'twoHundredDayMovAvg':twoHundredDayMovAvg,
            'bookValue':bookValue,
            'marketCap':marketCap,
            'priceToSales':priceToSales,
            'priceToBook':priceToBook,
            'optimalPeRatio': optimalPeRatio,
            'optimalPegRatio': optimalPegRatio,
            'optimalDebtToEquity': optimalDebtToEquity,
            'optimalYield': optimalYield,
            'optimalQRevGrowth': optimalQRevGrowth,
            'optimalBeta': optimalBeta,
            'configType': optimalType,
            'isPeOk': isPeOk,
            'isOneYearTargetOk': isOneYearTargetOk,
            'isQRevGrowthOk': isQRevGrowthOk,
            'isDivYieldOk': isDivYieldOk,
            'isDebtOk': isDebtOk                
        }

  # Add News based on how many items there are.
  # Commented out Sep 2018
  loopCount=0 
  while ( len( title ) > loopCount):
      templateValues["title_" + str(loopCount)]= title[loopCount];
      templateValues["link_" + str(loopCount) ]= link[loopCount];
      loopCount = loopCount + 1 ;
      logging.debug( "getRecommendation: Title length is - %d, templateValues = %s ", len(title) , templateValues ) ;
  

  logging.debug('Before Write to DB ticker %s is %s and beta is %s', ticker , recommendation , beta)
  # Write the results to the database
  if ( keyCount == expectedKeyCount ):
    tickerResults = TickerResultsNew(ticker=ticker
                               ,recommendation=recommendation
                               ,price=float(price)
                               ,peRatio=float(pe)
                               ,pegRatio=float(pegRatio)
                               ,debtToEquity=float(debtToEquity)
                               ,qRevGrowth=float(qRevGrowth)
                               ,divYield=float(divYield)
                               ,beta=float( beta )
                               ,optimalPeRatio=float(optimalPeRatio)
                               ,optimalPegRatio=float( optimalPegRatio)
                               ,optimalDebtToEquity=float( optimalDebtToEquity )
                               ,optimalDivYield=float( optimalYield )
                               ,optimalQRevGrowth=float( optimalQRevGrowth)
                               ,optimalBeta=float( optimalBeta )
                               ,configType= str(optimalType)
                               )
    tickerResults.put()
  
  logging.debug('Recommendation for ticker %s is %s', ticker , recommendation)
  return templateValues


def initializeStockAnalysis():
    
  tstart = datetime.now()
  #print "***  Starting Script at ",  startTime

  #Load Configs from File.
  configs=yaml.load( open("gaeAnalyzeStock.yaml"))
  keyStats={}
  
  tend = datetime.now()
  executionTime= tend - tstart
 
  

  
