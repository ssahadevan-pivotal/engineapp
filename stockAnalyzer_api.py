"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from main import *

package = 'stockAnalyzer'


class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


class StockAnalyzerResponseMessage(messages.Message):
    ticker = messages.StringField(1, required=True)
    recommendation= messages.StringField(2, required=True)
    price = messages.StringField(3);
    pe = messages.FloatField(4);
    pegRatio = messages.FloatField(5);
    debtToEquity= messages.StringField(6);
    qRevGrowth = messages.StringField(7);
    divYield= messages.StringField(8);
    isPeOk=messages.BooleanField(9);
    isPegOk=messages.BooleanField(10);
    isQRevGrowthOk=messages.BooleanField(11);
    isDivYieldOk=messages.BooleanField(12);
    isDebtOk=messages.BooleanField(13);
    tickerName= messages.StringField(14);
    
    optimalPeRatio = messages.FloatField(15);
    optimalPegRatio = messages.FloatField(16);
    optimalDebtToEquity = messages.FloatField(17);
    optimalYield= messages.FloatField(18);
    optimalQRevGrowth= messages.FloatField(19);
    optimalBeta = messages.FloatField(20);

 
                                                
class StockAnalyzerRequestMessage(messages.Message):
    ticker = messages.StringField(1);
    configType= messages.StringField(2);



@endpoints.api(name='stockAnalyzer', version='v1')
class StockAnalyzer(remote.Service):
    """StockAnalyzer API v1."""

    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        return STORED_GREETINGS

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    @endpoints.method( StockAnalyzerRequestMessage, StockAnalyzerResponseMessage,
                      path='stockAnalyzer', http_method='GET',
                      name='stockAnalyzer.getInfo')
    def stockAnalyzer_getInfo(self, request):
        try:
            # response = request.ticker;
            """ Adding Code """
            configType= request.configType;
            optimalValues=getOptimalValues( configType )
            if ( request.ticker != "" ):
                templateValues=getRecommendation(request.ticker, optimalValues)
            else:
                templateValues = {
                    'ticker': request.ticker,
                    'keyCount': 0,
                    'recommendation': "*** Please enter a valid Ticker ***"
                    }
            """ End Added Code """
            
            return StockAnalyzerResponseMessage( ticker=request.ticker
                                                 , recommendation= templateValues['recommendation']
                                                 , price= templateValues['price']
                                                 ,pe = templateValues['pe']
                                                 ,pegRatio =templateValues['pegRatio']
                                                 ,debtToEquity =templateValues['debtToEquity']
                                                 ,qRevGrowth =templateValues['qRevGrowth']
                                                 ,divYield =templateValues['divYield']
                                                 ,isPeOk=templateValues['isPeOk']
                                                 ,isPegOk=templateValues['isPegOk']
                                                 ,isQRevGrowthOk=templateValues['isQRevGrowthOk']
                                                 ,isDivYieldOk=templateValues['isDivYieldOk']
                                                 ,isDebtOk=templateValues['isDebtOk']
                                                 ,tickerName=templateValues['tickerName']
                                                 ,optimalPeRatio=templateValues['optimalPeRatio']
                                                 ,optimalPegRatio=templateValues['optimalPegRatio']
                                                 ,optimalDebtToEquity=templateValues['optimalDebtToEquity']
                                                 ,optimalYield=templateValues['optimalYield']
                                                 ,optimalQRevGrowth=templateValues['optimalQRevGrowth']
                                                 ,optimalBeta=templateValues['optimalBeta']
                                                );
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Got Exception');

APPLICATION = endpoints.api_server([StockAnalyzer])
