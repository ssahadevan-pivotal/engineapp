import sys, math
import urllib2
import re
from BeautifulSoup import BeautifulSoup


# Download the Key Statistics given a ticker symbol
# Return Key Statistics and list of Keys
def getKeyStats(ticker, DEBUG):
  # Download Key Stats from http://finance.yahoo.com/q/ks?s=MA

  # Open URL
  #  myURL='http://ichart.finance.yahoo.com/table.csv?'+\
  #                       's=%s&d=10&e=20&f=2010&g=d&a=9&b=20&c=2010'%t +\
  #                       '&ignore=.csv'
  #getKeyStatsNew( ticker, DEBUG) ;
  
  #myURL='http://finance.yahoo.com/q/ks?s=%s'%ticker
  #myURL='http://www.nasdaq.com/symbol/'%ticker
  myURL='http://www.nasdaq.com/symbol/' + ticker
  #print "In getKeyStats "
  if (DEBUG ):
      print myURL

  
    
  c=urllib2.urlopen(myURL)

  soup=BeautifulSoup(c.read())
  if DEBUG:
    print soup

  #print "***** soup  ends ***";
  keyCount=0

  key=""
  value=""
  keys={}
  keyStats={}
  keyFlag=True;
  ValueFlag=False;
  for data in soup('div'):
    # Find the div with the class below
    if ('class' in dict(data.attrs) and data['class']=='row overview-results relativeP'):
      if DEBUG:
        print "*** My My Found div ***"
        print data
      for tableCells in data('div'):
         if ('class' in dict(tableCells.attrs) and tableCells['class']=='table-cell'):
          #print "***  cell ***"
          # print tableCells.contents
          # print tableCells.getText();
          if ( keyFlag ):
            key=tableCells.getText();
            keys[keyCount]=key
            keyCount=keyCount + 1
            keyFlag=False;
            if DEBUG:
              print "*** Key is ***"
              print key
              print len(key)
          else:
            value=tableCells.getText();
            keyStats[key]=value
            keyFlag=True;
            if DEBUG:
              print "*** value = ***"
              print value
          continue;
        


  #key=""
  #value=""
  #keys={}
  #keyStats={}
  for td in soup('td'):
  # Prints the heading
    if ('class' in dict(td.attrs) and td['class']=='yfnc_tablehead1'):
      key=td.text
      keys[keyCount]=key
      keyCount=keyCount + 1
      if DEBUG:
        print "*** Key is ***"
        print key
        
      continue
  # Prints the Value
    if ('class' in dict(td.attrs) and td['class']=='yfnc_tabledata1'):
        value=td.text
        if DEBUG:
          print "*** value = ***"
          print value
          
        keyStats[key]=value
        #print "keyStats[key] is " + keyStats[key] 
        continue

  # Look for Title
  allDivs=soup.findAll("title");
  for div in allDivs:
    value = div.getText();
    key="title";
    keys[keyCount]=key;
    keyCount=keyCount + 1
    keyStats[key]=value
    #print "Title added" 

  #Printing keystats
  if DEBUG:
    for k in keyStats:
      print keyStats[k]
      print keyCount

  return keyStats, keyCount


#def getValueFromKey( keyStats, key ):
#  return keyStats[key]


def getValueFromKey( keyStats, key ):
  returnValue="0.0";
  #Check if key exists - Sep 2018
  if ( key in keyStats ):
    returnValue=keyStats[key];
    #print returnValue;
    # Strip out the %
    returnValue=returnValue.replace('%','')
    # Strip out the Commas
    returnValue=returnValue.replace(',','')
    returnValue=returnValue.replace('&nbsp;','')
    returnValue=returnValue.replace('$','')
  
  return returnValue

#Checks for None and returns Float value
def convertToFloat( dataToConvert ):
  returnValue=dataToConvert;

  if (( returnValue is None )or ( returnValue=="NA" ) or  ( returnValue=="N/A" ) ):
        returnValue=0.0;
  else:
        returnValue=float( returnValue );
  
 
  return returnValue

#Uncomment to run this directly in python
#DEBUG=True;
#ticker="MA" 
#keyStats , keyCount =getKeyStats(ticker,DEBUG)
#eps= getValueFromKey (keyStats,  'Earnings Per Share (EPS)' );

#print "EPS is " + eps;
#print keyStats['title']

        
#print keyStats, keyCount;
  
  
