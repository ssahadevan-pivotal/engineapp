import sys, math
import urllib2
from BeautifulSoup import BeautifulSoup
from getKeyStats import getValueFromKey

DEBUG=False;

# Download the Key Statistics given a ticker symbol
# Return Key Statistics and list of Keys
def getFundStats(ticker, DEBUG):
  # Download Key Stats from http://finance.yahoo.com/q/ks?s=MA

  # Open URL
  #  myURL='http://ichart.finance.yahoo.com/table.csv?'+\
  #                       's=%s&d=10&e=20&f=2010&g=d&a=9&b=20&c=2010'%t +\
  #                       '&ignore=.csv'

  # myURL='http://finance.yahoo.com/q/ks?s=%s'%ticker
  myURL='http://finance.yahoo.com/q?s=%s'%ticker
  #print "In getFundStats"
  
  if (DEBUG ):
      print myURL

  
    
  c=urllib2.urlopen(myURL)

  soup=BeautifulSoup(c.read())
  if DEBUG:
    print soup

  keyCount=0
  #StringToFind="EPS"
  key=""
  value=""
  keys={}
  keyStats={}
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
        continue

  
  
  allDivs=soup.findAll("div", { "class" : "title" });
  for div in allDivs:
    value = div.find('h2');
    key="title";
    keys[keyCount]=key;
    keyCount=keyCount + 1
    keyStats[key]=value.text
   

  summaryData=soup.find("table", { "id" : "table1"  });
  if DEBUG:
    print summaryData;
    
  for row in summaryData.findAll('tr'):
    heading=row.find('th');
    col = row.find('td');
    try:
      #print "row=", heading, col;
      tempKey=heading.string.strip();
      # Strip * from NetAssets*:
      tempKey=tempKey.replace('*', '');
      tempKey=tempKey.replace('&sup1;', '');
      tempKey=tempKey.replace('&sup2;', '');
      key=tempKey;
      keys[keyCount]=key;
      keyStats[key]= col.string.strip();
      keyCount=keyCount + 1
    except AttributeError:
       if DEBUG:
         print "*** 1. Error: row is row=", row;

  summaryData=soup.find("table", { "id" : "table2"  });
  if DEBUG:
    print summaryData;
    
  for row in summaryData.findAll('tr'):
    heading=row.find('th');
    col = row.find('td');
    try:
      #print "row=", heading.string.strip(), col.string.strip();
      tempKey=heading.string.strip();
      # Strip * from NetAssets*:
      key=tempKey.replace('*', '');
      keys[keyCount]=key;
      keyStats[key]= col.string.strip();
      keyCount=keyCount + 1
    except AttributeError:
       if DEBUG:
          print "*** 2. Error: row is row=", row;
  
  # Get the Price
  span=soup.find("span", { "class" : "time_rtq_ticker"  });
  #print span;
  priceSpan=span.findNext("span");
  price=priceSpan.text;
  #print "price =", price;
  key="Price:"
  keys[keyCount]=key;
  keyStats[key]= price;
  keyCount=keyCount + 1

  #Get the expense Ratio and category - Find the text and the value is next in the html
  listOfTxtItems={"Annual Report Expense Ratio (net):", "Category:"};
  for item in listOfTxtItems:
     #print "item is :" , item ;
     try:
        tempFoundString = soup.find(text=item)
        valueFound = tempFoundString.next.text ;
        #print tempFoundString , valueFound ;
        key=item;
        keys[keyCount]=key;
        keyStats[key]= valueFound;
        keyCount=keyCount + 1
     except AttributeError:
       print "*** Error: item is=", item;
      
  if DEBUG:
    print keyCount
    print keyStats

  print keys;
  
  return keyStats, keyCount, keys




#print "In getFundStats"
#ticker="MINDX";
#keyStats , keyCount =getFundStats(ticker,DEBUG)
  
