import sys, math
import urllib2
from BeautifulSoup import BeautifulSoup

DEBUG=False;

# Download the macro data
# Return Key Statistics and list of Keys
def getMacroData(DEBUG):
  myURL='http://www.multpl.com/shiller-pe/'

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
    if ('class' in dict(td.attrs) and td['class']=='stats'):
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

  # Look for Title
  allDivs=soup.find("div", { "id" : "current" });
  tempValue = allDivs.text;
  #print tempValue;
  indexOfSeparator = tempValue.find(':') ;
  key = tempValue[:indexOfSeparator];
  #print key;
  #Value is 26.25 ( so + 5)
  startIndex=indexOfSeparator+1;
  endIndex= startIndex + 5 ;
  value = tempValue[startIndex:endIndex];
  if DEBUG:
    print key , " is " , value;
  keys[keyCount]=key
  keyCount=keyCount + 1
  keyStats[key]=value;

  # Looks for other Stats
  statsTable=soup.find("table", { "id" : "stats" });
  if DEBUG:
    print statsTable;
  for row in statsTable.findAll('tr'):
    #print "row is " , row;
    col = row.findAll('td');
    if DEBUG:
      print "col[0] is " , col[0].text ;
      print "col[1] is " , col[1].text ;
    key = col[0].text;
    value = col[1].text;
    keys[keyCount]=key
    keyCount=keyCount + 1
    keyStats[key]=value;

  # if DEBUG:
  #for k in keyStats:
  #     print keyStats[k]

  #print keyStats["Diluted EPS (ttm):"]
  if DEBUG:
    print keyCount

  return keyStats, keyCount


def getValueFromKey( keyStats, key ):
  return keyStats[key]

# To Debug comment out following lines and run independently in pythonwin
#print "Starting getMacroData"
#keyStats , keyCount =getMacroData(DEBUG);
#print keyStats, keyCount;
  
  