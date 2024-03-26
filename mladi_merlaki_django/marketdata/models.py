from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=32)
    market_cap = models.IntegerField()
    sector = models.CharField(max_length=64)
    price = models.FloatField()
    dividend = models.FloatField()
    volume = models.IntegerField()
    country = models.CharField(max_length=3)
    exchange = models.CharField(max_length=16)
    is_etf = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=32)
    logo = models.CharField(max_length=128)
    market_cap = models.IntegerField()
    price = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.symbol})"