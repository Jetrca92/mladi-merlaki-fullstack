from django.contrib.auth.models import User
from django.db import models

from marketdata.models import Stock, Cryptocurrency


class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="owner")
    cash = models.FloatField(default=100000)
    stocks = models.ManyToManyField('StockPortfolio', blank=True)
    crypto = models.ManyToManyField('CryptoPortfolio', blank=True)

    def update_cash(self, amount):
        self.cash += amount
        self.save()

    def add_stock(self, stock):
        self.stocks.add(stock)
        self.save()

    def add_crypto(self, coin):
        self.crypto.add(coin)
        self.save()

    def calculate_stock_total(self):
        total = 0
        for stock in self.stocks.all():
            total += stock.total()
        return total
    
    def calculate_crypto_total(self):
        total = 0
        for coin in self.crypto.all():
            total += coin.total()
        return total

    
    def __str__(self):
        return f"{self.owner}"
    

class StockPortfolio(models.Model):
    owner = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, related_name="stock_owner")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, related_name="stock_stock")
    shares = models.IntegerField(default=0)

    def add_shares(self, shares):
        self.shares += shares
        self.save()

    def total(self):
        return self.stock.price * self.shares

    def __str__(self):
        return f"{self.stock} ({self.owner.owner.username})"


class CryptoPortfolio(models.Model):
    owner = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, related_name="crypto_portfolio_owner")
    coin = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, blank=True, related_name="coin")
    shares = models.FloatField(default=0)

    def add_shares(self, shares):
        self.shares += shares
        self.save()

    def total(self):
        return self.coin.price * self.shares

    def __str__(self):
        return f"{self.coin} ({self.owner})"
    

class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_owner")
    symbol = models.CharField(max_length=10)
    asset_class = models.CharField(max_length=32) # stock or crypto
    shares = models.FloatField()
    price = models.FloatField()
    type = models.CharField(max_length=10) # buy or sell
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.owner} {self.type} {self.shares} shares of {self.asset_class} at {self.price} on {self.date}"
    
    def total(self):
        return self.shares * self.price
