import sys, math
import urllib2
import json
from BeautifulSoup import BeautifulSoup
#from getKeyStats import *
from getFundStats import *
import yaml
import time
from datetime import datetime
import logging
from tickerResultsFundNewDao import *
import feedparser ;
from google.appengine.api import urlfetch;
from getNewsForTicker import *

# Used to control Print statements
DEBUG=False;

#Load the config file
configFile="gaeAnalyzeFund.yaml"
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

def getOptimalRank():
  return  getValueFromConfigs("optimalRank")

def getOptimalRisk():
  return  getValueFromConfigs("optimalRisk")

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

def getOptimalFiveYearReturn():
  return getValueFromConfigs("optimalFiveYearReturn");

def getOptimalExpenseRatio():
  return getValueFromConfigs("optimalExpenseRatio");


def isRankOptimal( actual, optimal ):
  if int ( actual)  <= int (optimal) :
     logging.error ('*** isRankOptimal: actual is %s' , actual )
     return True
  else:
     logging.error ('*** isRankOptimal: actual is %s' , actual )
     logging.error ('*** isRankOptimal: optimal is %s' , optimal ) 
     return False

#Is the Company Fairly Valued
def isRiskOptimal( actual, optimal ):
  if ( int(actual)  <= int(optimal) ) :
     #logging.debug ('*** isRiskOptimal: actual is %s' , actual )
     return True
  else:
     #logging.debug ('*** isRiskOptimal: actual is %s' , actual )
     #logging.debug ('*** isRiskOptimal: optimal is %s' , optimal ) 
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



def getRecommendationForFund( ticker , optimalValues):
  recommendation="SELL"
  keyStats ,keyCount, keys=getFundStats(ticker,DEBUG);

  # Set Optimal Valeues from Configs
  optimalRank= getOptimalRank();
  optimalRisk= getOptimalRisk() ;
  optimalType=optimalValues.configType;
  optimalYield= getOptimalYield() ;
  optimalFiveYearRet = getOptimalFiveYearReturn();
  optimalExpenseRatio = getOptimalExpenseRatio();
  
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

  # For US Funds the expectedKeyCount is 16
  expectedKeyCount=16;
  isRankOk=False;
  isRiskOk = False;
  isYieldOk= False;
  isFiveYearRetOk = False;
  isExpenseRatioOk = False;
  
  
  if ( keyCount == 0 ):
    print "*** Unable to get statistics for  " , ticker  ," *** "
    return

  tickerName=getValueFromKey( keyStats, getValueFromConfigs("TITLE_KEY"));
  prevClose=getValueFromKey( keyStats, getValueFromConfigs("PREV_CLOSE_KEY"));
  netAssets= getValueFromKey( keyStats, getValueFromConfigs("NET_ASSETS_KEY"));
  ytdReturn= getValueFromKey( keyStats, getValueFromConfigs("YTD_RETURN_KEY"));
  fundYield= getValueFromKey( keyStats, getValueFromConfigs("YIELD_KEY"));
  price =  getValueFromKey( keyStats, getValueFromConfigs("PRICE_KEY"));
  fiveYearRet =  getValueFromKey( keyStats, getValueFromConfigs("FIVE_YEAR_RET_KEY"));
  rankInCategory =  getValueFromKey( keyStats, getValueFromConfigs("RANK_IN_CATEGORY_KEY"));
  beta =  getValueFromKey( keyStats, getValueFromConfigs("BETA_KEY"));
  annualExpRatio =  getValueFromKey( keyStats, getValueFromConfigs("EXP_RATIO_KEY"));
  morningstarRiskRating =  getValueFromKey( keyStats, getValueFromConfigs("MRR_KEY"));
  category =  getValueFromKey( keyStats, getValueFromConfigs("CATEGORY_KEY"));
  
  if ( isRankOptimal( rankInCategory, optimalRank ) ):
    isRankOk=True;
    if ( isRiskOptimal( morningstarRiskRating, optimalRisk ) ):
      isRiskOk=True;
      if ( isHighPct( fundYield, optimalYield , getValueFromConfigs("YIELD_KEY"))):
        isYieldOk=True;
        if ( isHighPct( fiveYearRet,optimalFiveYearRet, getValueFromConfigs("FIVE_YEAR_RET_KEY"))):
          isFiveYearRetOk=True;
          # Test if exp ration is low
          if ( isHighPct( annualExpRatio,optimalExpenseRatio, getValueFromConfigs("EXP_RATIO_KEY")) is False ):
            isExpenseRatioOk=True;
            recommendation="BUY";
 
  title,link = getNewsForTicker(ticker);
  #news=""
  logging.debug( "getRecommendationForFund: Title length is - %d ,keystats= %s", len(title), keyStats) ;
  
  templateValues = {
            'ticker': ticker,
            'tickerName': tickerName,
            'keyCount': keyCount,
            'expectedKeyCount':expectedKeyCount,
            'recommendation': recommendation,
            'price': price,
            'prevClose': prevClose,
            'netAssets': netAssets,
            'ytdReturn': ytdReturn,
            'fiveYearRet': fiveYearRet,
            'optimalFiveYearRet':optimalFiveYearRet,
            'isFiveYearRetOk':isFiveYearRetOk,
            'rankInCategory': rankInCategory,
            'beta': beta,
            'morningstarRiskRating': morningstarRiskRating,
            'annualExpRatio': annualExpRatio,
            'optimalExpenseRatio':optimalExpenseRatio,
            'isExpenseRatioOk': isExpenseRatioOk,
            'category': category,
            'configType': optimalType,
            'optimalRank': optimalRank,
            'isRankOk': isRankOk,
            'optimalRisk': optimalRisk,
            'isRiskOk': isRiskOk,
            'isYieldOk': isYieldOk,
            'optimalYield': optimalYield,
            'fundYield': fundYield
            
        }

  # Add News based on how many items there are.
  loopCount=0 
  while ( len( title ) > loopCount):
      templateValues["title_" + str(loopCount)]= title[loopCount];
      templateValues["link_" + str(loopCount) ]= link[loopCount];
      loopCount = loopCount + 1 ;
      logging.debug( "getRecommendationForFund: Title length is - %d, templateValues = %s ", len(title) , templateValues ) ;
  

  logging.debug('Before Write to DB ticker %s is %s and beta is %s', ticker , recommendation , beta)
  # Write the results to the database
  if ( keyCount == expectedKeyCount ):
       tickerFundResults = TickerResultsFundNew(ticker=ticker
                              ,recommendation=recommendation
                              ,price=float(price)
                              ,rank=float(rankInCategory)
                              ,morningstarRiskRating=float(morningstarRiskRating)
                              ,debtToEquity=float(debtToEquity)
                              ,fundYield=float(fundYield)
                              ,fiveYearRet=float(fiveYearRet)
                              ,annualExpRatio=float(annualExpRatio)
                              )
  tickerFundResults.put()
  
  logging.debug('Recommendation for ticker %s is %s', ticker , recommendation)
  return templateValues


def initializeFundAnalysis():
    
  tstart = datetime.now()
  #print "***  Starting Script at ",  startTime

  #Load Configs from File.
  configs=yaml.load( open("gaeAnalyzeFund.yaml"))
  keyStats={}
  
  tend = datetime.now()
  executionTime= tend - tstart
 
  

  
