from django.contrib import admin

from portfolio.models import Portfolio, StockPortfolio, CryptoPortfolio, Transaction


admin.site.register(Portfolio)
admin.site.register(StockPortfolio)
admin.site.register(CryptoPortfolio)
admin.site.register(Transaction)