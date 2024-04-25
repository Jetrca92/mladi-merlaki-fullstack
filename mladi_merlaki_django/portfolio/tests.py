from django.test import TestCase
from django.contrib.auth.models import User

from marketdata.models import Stock, Cryptocurrency
from portfolio.models import Portfolio, StockPortfolio, CryptoPortfolio, Transaction
from portfolio.services import StockTransactionsService


class PortfolioModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.portfolio = Portfolio.objects.create(owner=self.user, cash=100000)
        self.stock = Stock.objects.create(
            name="Test Stock",
            symbol="TSTCK",
            market_cap=100,
            sector="test",
            price=1,
            dividend=0.1,
            volume=10,
            country="US",
            exchange="test EXCH",
            is_etf=False,
        )
        self.crypto = Cryptocurrency.objects.create(
            name="TestCoin",
            symbol="TTC",
            logo="none",
            market_cap=12,
            price=100,
            volume=14,
        )
        self.transaction = Transaction.objects.create(
            owner=self.user, 
            symbol='AAPL', 
            asset_class='stock', 
            shares=10, 
            price=150.50, 
            type='buy'
        )

    def test_update_cash(self):
        self.portfolio.update_cash(5000)
        self.assertEqual(self.portfolio.cash, 105000)

    def test_add_stock(self):
        stock_portfolio = StockPortfolio.objects.create(owner=self.portfolio, stock=self.stock)
        self.portfolio.add_stock(stock_portfolio)
        self.assertTrue(self.portfolio.stocks.filter(id=stock_portfolio.id).exists())

    def test_remove_stock(self):
        stock_portfolio = StockPortfolio.objects.create(owner=self.portfolio, stock=self.stock)
        self.portfolio.add_stock(stock_portfolio)
        self.assertTrue(self.portfolio.stocks.filter(id=stock_portfolio.id).exists())
        self.portfolio.remove_stock(stock_portfolio)
        self.assertFalse(self.portfolio.stocks.filter(id=stock_portfolio.id).exists())

    def test_add_crypto(self):
        crypto_portfolio = CryptoPortfolio.objects.create(owner=self.portfolio, coin=self.crypto)
        self.portfolio.add_crypto(crypto_portfolio)
        self.assertTrue(self.portfolio.crypto.filter(owner=self.portfolio, id=crypto_portfolio.id))

    def test_remove_crypto(self):
        crypto_portfolio = CryptoPortfolio.objects.create(owner=self.portfolio, coin=self.crypto)
        self.portfolio.add_crypto(crypto_portfolio)
        self.assertTrue(self.portfolio.crypto.filter(owner=self.portfolio, id=crypto_portfolio.id))
        self.portfolio.remove_crypto(crypto_portfolio)
        self.assertFalse(self.portfolio.crypto.filter(owner=self.portfolio, id=crypto_portfolio.id))

    def test_add_transaction(self):
        self.portfolio.add_transaction(self.transaction)
        self.assertTrue(self.portfolio.transactions.filter(owner=self.user, id=self.transaction.id))

    def test_calculate_stock_total(self):
        stock_portfolio = StockPortfolio.objects.create(owner=self.portfolio, stock=self.stock, shares=10)
        self.portfolio.add_stock(stock_portfolio)
        total_value = self.stock.price * stock_portfolio.shares
        self.assertEqual(self.portfolio.calculate_stock_total(), total_value)

    def test_calculate_crypto_total(self):
        crypto_portfolio = CryptoPortfolio.objects.create(owner=self.portfolio, coin=self.crypto, shares=2)
        self.portfolio.add_crypto(crypto_portfolio)
        total_value = self.crypto.price * crypto_portfolio.shares
        self.assertEqual(self.portfolio.calculate_crypto_total(), total_value)


class StockPortfolioModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.portfolio = Portfolio.objects.create(owner=self.user, cash=100000)
        self.stock = Stock.objects.create(
            name="Test Stock",
            symbol="TSTCK",
            market_cap=100000,
            sector="test",
            price=100,
            dividend=0.1,
            volume=1000,
            country="US",
            exchange="test EXCH",
            is_etf=False,
        )
        self.stock_portfolio = StockPortfolio.objects.create(
            owner=self.portfolio, 
            stock=self.stock, 
            shares=5
        )

    def test_add_shares(self):
        start_shares = self.stock_portfolio.shares
        shares_to_add = 5
        self.stock_portfolio.add_shares(shares_to_add)
        self.assertEqual(self.stock_portfolio.shares, (start_shares + shares_to_add))

    def test_remove_shares(self):
        start_shares = self.stock_portfolio.shares
        shares_to_remove = 4
        self.stock_portfolio.remove_shares(shares_to_remove)
        self.assertEqual(self.stock_portfolio.shares, (start_shares - shares_to_remove))

    def test_total(self):
        self.assertEqual(self.stock_portfolio.total(), (self.stock_portfolio.stock.price * self.stock_portfolio.shares))


class CryptoPortfolioModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.portfolio = Portfolio.objects.create(owner=self.user, cash=100000)
        self.coin = Cryptocurrency.objects.create(
            name="TestCoin",
            symbol="TTC",
            logo="none",
            market_cap=12,
            price=100,
            volume=14,
        )
        self.crypto_portfolio = CryptoPortfolio.objects.create(
            owner=self.portfolio, 
            coin=self.coin, 
            shares=5.4
        )

    def test_add_shares(self):
        start_shares = self.crypto_portfolio.shares
        shares_to_add = 3.34
        self.crypto_portfolio.add_shares(shares_to_add)
        self.assertEqual(self.crypto_portfolio.shares, (start_shares + shares_to_add))

    def test_remove_shares(self):
        start_shares = self.crypto_portfolio.shares
        shares_to_remove = 4.44
        self.crypto_portfolio.remove_shares(shares_to_remove)
        self.assertEqual(self.crypto_portfolio.shares, (start_shares - shares_to_remove))

    def test_total(self):
        self.assertEqual(self.crypto_portfolio.total(), (self.crypto_portfolio.coin.price * self.crypto_portfolio.shares))
    

class BuyStockServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.portfolio = Portfolio.objects.create(owner=self.user, cash=100000)
        self.stock = Stock.objects.create(
            name="Test Stock",
            symbol="TSTCK",
            market_cap=100000,
            sector="test",
            price=100,
            dividend=0.1,
            volume=1000,
            country="US",
            exchange="test EXCH",
            is_etf=False,
        )
            
    def test_buy_stock_sufficient_balance(self):
        starting_balance = self.portfolio.cash
        shares_to_buy = 5

        # No transactions or stock
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.stock.symbol, type="buy").count(), 0)
        self.assertFalse(self.portfolio.stocks.filter(stock=self.stock))

        StockTransactionsService.buy_stock(self.stock.symbol, self.user, shares_to_buy)

        # Transaction created, stock added to portfolio, cash withdrawn
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.stock.symbol, type="buy").count(), 1)
        self.assertTrue(self.portfolio.stocks.filter(stock=self.stock))
        user_portfolio = Portfolio.objects.get(owner=self.user)
        self.assertEqual(user_portfolio.cash, (starting_balance - (self.stock.price * shares_to_buy)))

    def test_buy_stock_insufficient_balance(self):
        self.portfolio.cash = 0
        self.portfolio.save()
        shares_to_buy = 5

        StockTransactionsService.buy_stock(self.stock.symbol, self.user, shares_to_buy)

        # No cash, transaction shouldn't complete
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.stock.symbol, type="buy").count(), 0)
        self.assertFalse(self.portfolio.stocks.filter(stock=self.stock))

    def test_buy_stock_zero_negative_shares(self):
        shares_to_buy = -5
        zero_shares = 0
        StockTransactionsService.buy_stock(self.stock.symbol, self.user, shares_to_buy)
        StockTransactionsService.buy_stock(self.stock.symbol, self.user, zero_shares)

        # No transactions when shares <= 0
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.stock.symbol, type="buy").count(), 0)
        self.assertFalse(self.portfolio.stocks.filter(stock=self.stock))

    def test_buy_stock_does_not_exist(self):
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol="FBB", type="buy").count(), 0)

        StockTransactionsService.buy_stock("FBB", self.user, 5)

        # No transaction if stock does not exist
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol="FBB", type="buy").count(), 0)

    
class SellStockServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.portfolio = Portfolio.objects.create(owner=self.user, cash=100000)
        self.stock = Stock.objects.create(
            name="Test Stock",
            symbol="TSTCK",
            market_cap=100000,
            sector="test",
            price=100,
            dividend=0.1,
            volume=1000,
            country="US",
            exchange="test EXCH",
            is_etf=False,
        )
        self.stock_portfolio = StockPortfolio.objects.create(
            owner=self.portfolio,
            stock=self.stock,
            shares=5,
        )
        self.portfolio.add_stock(self.stock_portfolio)

    def test_sell_stock_sufficient_shares(self):
        starting_balance = self.portfolio.cash
        shares_to_sell = 4

        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.stock.symbol, type="sell").count(), 0)
        self.assertTrue(self.portfolio.stocks.filter(stock=self.stock))

        StockTransactionsService.sell_stock(self.stock.symbol, self.user, shares_to_sell)

        # Sell transaction created, stock should still be in portfolio (1 share), cash updated
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.stock.symbol, type="sell").count(), 1)
        self.assertTrue(self.portfolio.stocks.filter(stock=self.stock))
        user_portfolio = Portfolio.objects.get(owner=self.user)
        self.assertEqual(user_portfolio.cash, (starting_balance + (self.stock.price * shares_to_sell)))

    def test_sell_stock_equal_shares(self):
        shares_to_sell = 5
        self.assertTrue(self.portfolio.stocks.filter(stock=self.stock))

        StockTransactionsService.sell_stock(self.stock.symbol, self.user, shares_to_sell)

        # All shares sold, stock should be removed
        self.assertFalse(self.portfolio.stocks.filter(stock=self.stock))

    def test_sell_stock_invalid_shares(self):
        shares_to_sell = 6
        self.assertTrue(self.portfolio.stocks.filter(stock=self.stock))
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.stock.symbol, type="sell").count(), 0)

        StockTransactionsService.sell_stock(self.stock.symbol, self.user, shares_to_sell)

        # No transaction or sell, shares invalid 
        self.assertTrue(self.portfolio.stocks.filter(stock=self.stock))
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.stock.symbol, type="sell").count(), 0)

    def test_sell_stock_does_not_exist(self):
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol="FBB", type="sell").count(), 0)
        self.assertFalse(self.portfolio.stocks.filter(stock__symbol="FBB"))

        StockTransactionsService.sell_stock("FBB", self.user, 5)
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol="FBB", type="sell").count(), 0)
