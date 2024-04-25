from django.test import TestCase
from django.contrib.auth.models import User
from marketdata.models import Stock, Cryptocurrency
from portfolio.models import Portfolio, StockPortfolio, CryptoPortfolio, Transaction


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
    


            

