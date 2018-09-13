import sys, math
import urllib2
import json
from BeautifulSoup import BeautifulSoup
#from getKeyStats import *
import yaml
import time
from datetime import datetime
import logging
#from tickerResultsNewDao import *
import feedparser ;
from google.appengine.api import urlfetch;


# Used to control Print statements
DEBUG=False;


#Get the News for ticker
def getNewsForTicker(ticker):
  #url = "http://finance.yahoo.com/q/h?s=" + ticker + "+Headlines";
  url = "http://www.nasdaq.com/symbol/" + ticker + "/news-headlines";
  try:
    handle=urllib2.urlopen(url);
    response=handle.read();
  except:
    e = sys.exc_info()[0];
    logging.error( "getNewsForTicker: Error while fetching news - %s", e) ;
    
  soup=BeautifulSoup( response);
  found=False;
  itemCount = 0 ;
  title={};
  link={};

  divsOfClass=soup.find("div", { "class" : "news-headlines"  });
  # July 2014 - MAPIX did not have any news, so check if divsOfClass is None
  if divsOfClass is None:
    logging.warn( "*** getNewsForTicker: No news found , divsOfClass is %s", divsOfClass) ;
  else:
   for ahref in divsOfClass.findAll('a',{'target':"_self"}):
      if ( itemCount >= 5 ):
        break;
      
      if ( DEBUG ):
        logging.error( "getNewsForTicker: itemCount=%d, ahref=%s ", itemCount, ahref) ;
        
      #if ( ahref != None and ahref.target == "_self") :
      #   found = True;
        

      #if ( ahref.text.strip() == "Older Headlines") :
      #  found = False;
        
      #if found == True :
      title[itemCount]=ahref.text;
      link[itemCount]=ahref['href'];
      itemCount = itemCount + 1 ;
      

  if ( DEBUG ):
    logging.error( "getNewsForTicker: News for ticker %s is title = %s ,link=%s, itemCount=%d ",ticker, title, link, itemCount) ;
  return title, link

