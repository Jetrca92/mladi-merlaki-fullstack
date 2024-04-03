from django.db import transaction

from marketdata.models import Stock, Cryptocurrency
from portfolio.models import Portfolio, StockPortfolio, Transaction, CryptoPortfolio


@transaction.atomic
def buy_stock(stock_symbol, user, shares):
    stock = Stock.objects.get(symbol=stock_symbol)
    total = float(stock.price) * float(shares)

    # Check if user has sufficient balance
    user_portfolio = Portfolio.objects.get(owner=user)
    if (float(user_portfolio.cash) < total):
        return
    if shares <= 0:
        return

    # Add stock to portfolio
    s, _created = StockPortfolio.objects.get_or_create(
        owner=user_portfolio,
        stock=stock,
    )
    s.add_shares(shares)
    user_portfolio.add_stock(s)

    # Add transaction to Transactions model
    transaction = Transaction.objects.create(
        owner=user, 
        symbol=stock.symbol, 
        asset_class="stock", 
        shares=shares, 
        price=stock.price, 
        type="buy",
    )

    # Deduct price from users cash
    user_portfolio.update_cash(-total)


@transaction.atomic
def buy_crypto(crypto_symbol, user, shares):
    coin = Cryptocurrency.objects.get(symbol=crypto_symbol)
    total = float(coin.price) * float(shares)

    # Check if user has sufficient balance
    user_portfolio = Portfolio.objects.get(owner=user)
    if (float(user_portfolio.cash) < total):
        return
    if shares <= 0:
        return
    
    # Add coin to portfolio
    c, _created = CryptoPortfolio.objects.get_or_create(
        owner=user_portfolio,
        coin=coin,
    )
    c.add_shares(shares)
    user_portfolio.add_crypto(c)

    # Add transaction to Transactions model
    transaction = Transaction.objects.create(
        owner=user, 
        symbol=coin.symbol, 
        asset_class="crypto", 
        shares=shares, 
        price=coin.price, 
        type="buy",
    )

    # Deduct price from users cash
    user_portfolio.update_cash(-total)