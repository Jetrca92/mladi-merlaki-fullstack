from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=32)
    market_cap = models.BigIntegerField()
    sector = models.CharField(max_length=64, null=True)
    price = models.FloatField()
    dividend = models.FloatField(null=True)
    volume = models.BigIntegerField()
    country = models.CharField(max_length=3, null=True)
    exchange = models.CharField(max_length=16)
    is_etf = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
    class Meta:
        ordering = ['-market_cap']

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=32)
    logo = models.CharField(max_length=128)
    market_cap = models.BigIntegerField()
    price = models.FloatField()
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
    class Meta:
        ordering = ['-market_cap']