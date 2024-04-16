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
    Transaction.objects.create(
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
def sell_stock(stock_symbol, user, shares):
    stock = Stock.objects.get(symbol=stock_symbol)
    user_portfolio = Portfolio.objects.get(owner=user)
    total = float(stock.price) * float(shares)

    # Check if stock in user portfolio
    try:
        stock_portfolio = StockPortfolio.objects.get(owner=user_portfolio, stock=stock)
    except StockPortfolio.DoesNotExist:
        return
    
    # Check if user has sufficient shares amount
    if (float(stock_portfolio.shares) < shares):
        return
    if shares <= 0:
        return
    
    # Remove shares or stock from portfolio
    if shares == stock_portfolio.shares:
        user_portfolio.remove_stock(stock)
    stock_portfolio.remove_shares(shares)
    
    # Add transaction to Transactions model
    Transaction.objects.create(
        owner=user, 
        symbol=stock.symbol, 
        asset_class="stock", 
        shares=-shares, 
        price=stock.price, 
        type="sell",
    )

    # Add cash to portfolio
    user_portfolio.update_cash(total)
    
    
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

    # Deduct price from users cash and add transaction to portfolio
    user_portfolio.update_cash(-total)
    user_portfolio.add_transaction(transaction)


@transaction.atomic
def sell_crypto(coin_symbol, user, shares):
    coin = Cryptocurrency.objects.get(symbol=coin_symbol)
    user_portfolio = Portfolio.objects.get(owner=user)
    total = float(coin.price) * float(shares)

    # Check if coin in user portfolio
    try:
        crypto_portfolio = CryptoPortfolio.objects.get(owner=user_portfolio, coin=coin)
    except CryptoPortfolio.DoesNotExist:
        return
    
    # Check if user has sufficient shares amount
    if (float(crypto_portfolio.shares) < shares):
        return
    if shares <= 0:
        return
    
    # Remove shares or coin from portfolio
    if shares == crypto_portfolio.shares:
        user_portfolio.remove_crypto(coin)
    crypto_portfolio.remove_shares(shares)
    
    # Add transaction to Transactions model
    Transaction.objects.create(
        owner=user, 
        symbol=coin.symbol, 
        asset_class="crypto", 
        shares=-shares, 
        price=coin.price, 
        type="sell",
    )

    # Add cash to portfolio
    user_portfolio.update_cash(total)


def calculate_portfolio_rankings(portfolios):
    data = []
    for portfolio in portfolios:
        stocks_total = portfolio.calculate_stock_total()
        crypto_total = portfolio.calculate_crypto_total()
        cash = portfolio.cash
        total = stocks_total + crypto_total + cash
        data.append({
            "username": portfolio.owner.username,
            "stocks_total": stocks_total,
            "crypto_total": crypto_total,
            "cash": cash,
            "total": total,
        })
    return sorted(data, key=lambda x: x['total'], reverse=True)
