import sys, math
import urllib2
from BeautifulSoup import BeautifulSoup
import logging
from yahoo_finance import Share

def getKeyStatsNew(ticker, DEBUG):
 
  #print "In getKeyStatsNew"
  
  tickerData=Share( ticker) ;
  #print tickerData.get_price();
  
  return tickerData;


def getValueFromKey( keyStats, key ):
  returnValue=keyStats[key]
  # Strip out the %
  returnValue=returnValue.replace('%','')
  # Strip out the Commas
  returnValue=returnValue.replace(',','')
  
  if (( returnValue=="NA" ) or  ( returnValue=="N/A" ) ):
    returnValue="0.0"
    
  return returnValue

#Checks for None and returns Float value
def convertToFloat( dataToConvert ):
  returnValue=dataToConvert;

  if (( returnValue is None )or ( returnValue=="NA" ) or  ( returnValue=="N/A" ) ):
        returnValue=0.0;
  else:
        returnValue=float( returnValue );
  
 
  return returnValue









  