from django.db import transaction

from portfolio.models import Portfolio, StockPortfolio, Transaction

@transaction.atomic
def buy_stock(stock, user, shares):
    total = float(stock.price) * float(shares)

    #Check if user has sufficient balance
    user_portfolio = Portfolio.objects.get(owner=user)
    if (float(user_portfolio.cash) < total):
        return
    if shares < 0:
        return

    # Add stock to portfolio
    s, _created = StockPortfolio.objects.get_or_create(
        owner=user,
        stock=stock,
    )
    s.add_shares(shares)

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

