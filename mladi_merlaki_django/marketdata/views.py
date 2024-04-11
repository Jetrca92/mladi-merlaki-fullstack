from django.contrib.auth.models import User
from django.http import Http404
from django.utils.timezone import datetime

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from marketdata.helpers import market_update, calculate_monthly_volume, calculate_yearly_transactions
from marketdata.models import Cryptocurrency, Stock
from marketdata.serializers import StockSerializer, CryptoSerializer, AppInfoSerializer


class StockmarketDataView(APIView):
        
    def get(self, request, format=None):
        market_update(datetime.today)
        stocks = Stock.objects.all()[0:1000]
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)
    

class StockDataView(APIView):

    def get_object(self, id):
        try:
            return Stock.objects.get(id=id)
        except Stock.DoesNotExist:
            raise Http404
        
    def get(self, request, id, format=None):
        stock = self.get_object(id)
        serializer = StockSerializer(stock)
        return Response(serializer.data)
    

class CryptomarketDataView(APIView):
    def get(self, request, format=None):
        market_update(datetime.today)
        crypto = Cryptocurrency.objects.all()[0:100]
        serializer = CryptoSerializer(crypto, many=True)
        return Response(serializer.data)
    

class CryptocurrencyDataView(APIView):

    def get_object(self, id):
        try:
            return Cryptocurrency.objects.get(id=id)
        except Cryptocurrency.DoesNotExist:
            raise Http404
        
    def get(self, request, id, format=None):
        coin = self.get_object(id)
        serializer = CryptoSerializer(coin)
        return Response(serializer.data)
    

class AppdataView(APIView):
    
    def get(self, request, format=None):
        app_data = {
            "monthly_volume": calculate_monthly_volume(),
            "transactions": calculate_yearly_transactions(),
            "users": User.objects.count(),
        }
        serializer = AppInfoSerializer(data=app_data)
        if serializer.is_valid():
            return Response(serializer.data)
        
        