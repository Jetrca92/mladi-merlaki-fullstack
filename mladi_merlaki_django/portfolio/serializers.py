from django.contrib.auth.models import User

from rest_framework import serializers

from portfolio.models import Portfolio, StockPortfolio, CryptoPortfolio, Transaction
from marketdata.serializers import StockSerializer, CryptoSerializer


class StockPortfolioSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = StockPortfolio
        fields = ('stock', 'shares')


class CryptoPortfolioSerializer(serializers.ModelSerializer):
    coin = CryptoSerializer()

    class Meta:
        model = CryptoPortfolio
        fields = ('coin', 'shares')


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


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
            model = Transaction
            fields = (
                "owner",
                "symbol",
                "asset_class",
                "shares",
                "price",
                "type",
                "date",
            )



class RankingsSerializer(serializers.Serializer):
    username = serializers.CharField()
    stocks_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    crypto_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    cash = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

