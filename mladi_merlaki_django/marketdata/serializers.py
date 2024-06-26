from rest_framework import serializers

from marketdata.models import Stock, Cryptocurrency


class StockSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

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
            'id',
        )

class CryptoSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Cryptocurrency
        fields = (
            'name', 
            'symbol', 
            'logo',
            'market_cap',
            'price',
            'volume',
            'id',
        )


class AppInfoSerializer(serializers.Serializer):
    monthly_volume = serializers.DecimalField(max_digits=20, decimal_places=2, rounding='ROUND_HALF_UP')
    transactions = serializers.IntegerField()
    users = serializers.IntegerField()