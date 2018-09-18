import sys, math
import urllib2
import re
from BeautifulSoup import BeautifulSoup
import json


# Download the Key Statistics given a ticker symbol
# Return Key Statistics and list of Keys
def getAdditionalKeyStats(ticker, apiKey, DEBUG):
  myURL='https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + ticker + '&apikey=' + apiKey

  if (DEBUG ):
      print "In getAdditionalKeyStats"
      print myURL

#  response = requests.get(myURL)
    
  c=urllib2.urlopen(myURL)

  jsonData = json.loads(c.read() )

  if (DEBUG):
    print jsonData
    
  return jsonData


#Generic get Data
def getData( function , apiKey, DEBUG ):
  myURL='https://www.alphavantage.co/query?function='+ function +   '&apikey=' + apiKey
  if (DEBUG ):
      print "In getData"
      print myURL

#  response = requests.get(myURL)
    
  c=urllib2.urlopen(myURL)

  jsonData = json.loads(c.read() )

  if (DEBUG):
    print jsonData
    
  return jsonData



#Uncomment to run this directly in python
# Sample data {u'Global Quote': {u'05. price': u'217.8000', u'08. previous close': u'214.0300', u'10. change percent': u'1.7614%'
#, u'03. high': u'218.6900', u'07. latest trading day': u'2018-09-13',
# u'04. low': u'214.3700', u'06. volume': u'2150640', u'01. symbol': u'MA', u'02. open': u'214.7700', u'09. change': u'3.7700'}}
# Uncomment below
DEBUG=False;
ticker="MA"
apiKey='A8ZAY0BFM4335U9N'
additionalStockData = getAdditionalKeyStats(ticker,apiKey,DEBUG)
if ( DEBUG ):
  print additionalStockData

price = additionalStockData['Global Quote']['05. price'];
change = additionalStockData['Global Quote']['09. change'];
volumne = additionalStockData['Global Quote']['06. volume'];
if  ( DEBUG ):
  print "price = " + price + " change = " + change
  
  
function="SECTOR"
sectorData=getData( function , apiKey, DEBUG);
print sectorData;

