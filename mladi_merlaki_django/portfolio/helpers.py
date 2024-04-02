from django.db import transaction

from marketdata.models import Stock
from portfolio.models import Portfolio, StockPortfolio, Transaction

@transaction.atomic
def buy_stock(stock_id, user, shares):
    stock = Stock.objects.get(symbol=stock_id)
    total = float(stock.price) * float(shares)

    # Check if user has sufficient balance
    user_portfolio = Portfolio.objects.get(owner=user)
    if (float(user_portfolio.cash) < total):
        return
    if shares < 0:
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
