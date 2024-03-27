from django.contrib.auth.models import User
from django.db import models

from marketdata.models import Stock, Cryptocurrency


class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="owner")
    cash = models.FloatField(default=100000)
    stocks = models.ManyToManyField('StockPortfolio', blank=True)
    crypto = models.ManyToManyField('CryptoPortfolio', blank=True)

    def __str__(self):
        return f"{self.owner}"
    

class StockPortfolio(models.Model):
    owner = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, related_name="stock_owner")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, related_name="stock_stock")
    shares = models.IntegerField()

    def __str__(self):
        return f"{self.stock} ({self.owner.owner.username})"


class CryptoPortfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="crypto_portfolio_owner")
    coin = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, blank=True, related_name="coin")
    shares = models.FloatField()

    def __str__(self):
        return f"{self.coin} ({self.owner})"
