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
        stocks = Stock.objects.all()[0:20]
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)