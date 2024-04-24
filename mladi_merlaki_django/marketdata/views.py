from django.utils.timezone import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from marketdata.models import Cryptocurrency, Stock
from marketdata.serializers import StockSerializer, CryptoSerializer, AppInfoSerializer
from marketdata.services import CryptocurrencyService, StockService, AppDataService, MarketDataService

class StockmarketDataView(APIView):
        
    def get(self, request, format=None):
        MarketDataService.market_update()
        stocks = Stock.objects.all()[0:1000]
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)
    

class StockDataView(APIView):
        
    def get(self, request, id, format=None):
        stock = StockService.get_stock_by_id(id)
        serializer = StockSerializer(stock)
        return Response(serializer.data)
    

class CryptomarketDataView(APIView):
    def get(self, request, format=None):
        MarketDataService.market_update()
        crypto = Cryptocurrency.objects.all()[0:100]
        serializer = CryptoSerializer(crypto, many=True)
        return Response(serializer.data)
    

class CryptocurrencyDataView(APIView):
        
    def get(self, request, id, format=None):
        coin = CryptocurrencyService.get_cryptocurrency_by_id(id)
        serializer = CryptoSerializer(coin)
        return Response(serializer.data)
    

class AppdataView(APIView):
    
    def get(self, request, format=None):
        app_data = AppDataService.get_app_data()
        serializer = AppInfoSerializer(data=app_data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        