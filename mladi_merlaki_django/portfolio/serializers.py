from django.contrib.auth.models import User

from rest_framework import serializers

from portfolio.models import Portfolio, StockPortfolio, CryptoPortfolio
from marketdata.models import Stock, Cryptocurrency


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'name', 
            'symbol',
            'market_cap',
            'sector', 
            'price',
            'dividend',
            'volume',
            'country',
            'exchange',
            'is_etf',
        )

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = (
            'name', 
            'symbol', 
            'logo',
            'market_cap',
            'price',
            'volume',
        )

class StockPortfolioSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = StockPortfolio
        fields = ('owner', 'stock', 'shares')

class CryptoPortfolioSerializer(serializers.ModelSerializer):
    coin = CryptoSerializer()

    class Meta:
        model = CryptoPortfolio
        fields = ('owner', 'coin', 'shares')

class PortfolioSerializer(serializers.ModelSerializer):
    stocks = StockPortfolioSerializer(many=True)
    crypto = CryptoPortfolioSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = (
            "owner",
            "cash",
            "stocks",
            "crypto",
        )