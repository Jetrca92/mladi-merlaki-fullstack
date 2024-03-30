from django.http import Http404
from django.utils.timezone import datetime

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from marketdata.helpers import market_update
from marketdata.models import Cryptocurrency, Stock
from marketdata.serializers import StockSerializer, CryptoSerializer


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
        