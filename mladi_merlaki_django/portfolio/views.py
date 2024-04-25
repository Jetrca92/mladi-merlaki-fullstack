from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from portfolio.services import StockTransactionsService, CryptocurrencyTransactionsService, PortfolioService
from portfolio.models import Portfolio, Transaction
from portfolio.serializers import (
    PortfolioSerializer, 
    StockPortfolioSerializer, 
    CryptoPortfolioSerializer, 
    TransactionSerializer, 
    RankingsSerializer,
)


class PortfolioView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get(self, request, format=None):
        portfolio, _created = Portfolio.objects.get_or_create(owner=request.user)
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data)
    

class BuyStockView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StockPortfolioSerializer(data=request.data)
        if serializer.is_valid():

            # Add stock to portfolio
            StockTransactionsService.buy_stock(
                serializer.validated_data["stock"]["symbol"], 
                request.user, 
                serializer.validated_data["shares"]
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SellStockView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StockPortfolioSerializer(data=request.data)
        if serializer.is_valid():

            # Remove stock from portfolio
            StockTransactionsService.sell_stock(
                serializer.validated_data["stock"]["symbol"], 
                request.user, 
                serializer.validated_data["shares"]
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyCryptoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CryptoPortfolioSerializer(data=request.data)
        if serializer.is_valid():

            # Add crypto to portfolio
            CryptocurrencyTransactionsService.buy_crypto(
                serializer.validated_data["coin"]["symbol"], 
                request.user, 
                serializer.validated_data["shares"]
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellCryptoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CryptoPortfolioSerializer(data=request.data)
        if serializer.is_valid():

            # Remove stock from portfolio
            CryptocurrencyTransactionsService.sell_crypto(
                serializer.validated_data["coin"]["symbol"], 
                request.user, 
                serializer.validated_data["shares"]
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get(self, request, format=None):
        transactions = Transaction.objects.filter(owner=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class RankingsView(APIView):

    def get(self, request, format=None):
        portfolios = Portfolio.objects.all()[0:100]
        rankings = PortfolioService.calculate_portfolio_rankings(portfolios)
        serializer = RankingsSerializer(rankings, many=True)
        return Response(serializer.data)


   