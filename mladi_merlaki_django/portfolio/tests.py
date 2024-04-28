from django.test import TestCase
from django.contrib.auth.models import User

from marketdata.models import Stock, Cryptocurrency
from portfolio.models import Portfolio, StockPortfolio, CryptoPortfolio, Transaction
from portfolio.services import StockTransactionsService, CryptocurrencyTransactionsService, PortfolioService


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


class BuyCryptocurrenyServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.portfolio = Portfolio.objects.create(owner=self.user, cash=100000)
        self.coin = Cryptocurrency.objects.create(
            name="TestCoin",
            symbol="TTC",
            logo="none",
            market_cap=120000,
            price=1000,
            volume=14000,
        )

    def test_buy_cryptocurrency_sufficient_balance(self):
        starting_balance = self.portfolio.cash
        shares_to_buy = 5

        # No transactions or coin
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="buy").count(), 0)
        self.assertFalse(self.portfolio.crypto.filter(coin=self.coin))

        CryptocurrencyTransactionsService.buy_crypto(self.coin.symbol, self.user, shares_to_buy)

        # Transaction created, coin added to portfolio, cash withdrawn
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="buy").count(), 1)
        self.assertTrue(self.portfolio.crypto.filter(coin=self.coin))
        user_portfolio = Portfolio.objects.get(owner=self.user)
        self.assertEqual(user_portfolio.cash, (starting_balance - (self.coin.price * shares_to_buy)))

    def test_buy_crypto_insufficient_balance(self):
        self.portfolio.cash = 0
        self.portfolio.save()
        shares_to_buy = 5

        CryptocurrencyTransactionsService.buy_crypto(self.coin.symbol, self.user, shares_to_buy)

        # No cash, transaction shouldn't complete
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="buy").count(), 0)
        self.assertFalse(self.portfolio.crypto.filter(coin=self.coin))

    def test_buy_crypto_zero_negative_shares(self):
        shares_to_buy = -5
        zero_shares = 0
        CryptocurrencyTransactionsService.buy_crypto(self.coin.symbol, self.user, shares_to_buy)
        CryptocurrencyTransactionsService.buy_crypto(self.coin.symbol, self.user, zero_shares)

        # No transactions when shares <= 0
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="buy").count(), 0)
        self.assertFalse(self.portfolio.crypto.filter(coin=self.coin))

    def test_buy_crypto_does_not_exist(self):
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol="FBB", type="buy").count(), 0)

        CryptocurrencyTransactionsService.buy_crypto("FBB", self.user, 5)

        # No transaction if coin does not exist
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="buy").count(), 0)
    

class SellCryptocurrencyServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.portfolio = Portfolio.objects.create(owner=self.user, cash=100000)
        self.coin = Cryptocurrency.objects.create(
            name="TestCoin",
            symbol="TTC",
            logo="none",
            market_cap=120000,
            price=1000,
            volume=14000,
        )
        self.crypto_portfolio = CryptoPortfolio.objects.create(
            owner=self.portfolio,
            coin=self.coin,
            shares=5,
        )
        self.portfolio.add_crypto(self.crypto_portfolio)

    def test_sell_crypto_sufficient_shares(self):
        starting_balance = self.portfolio.cash
        shares_to_sell = 4

        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="sell").count(), 0)
        self.assertTrue(self.portfolio.crypto.filter(coin=self.coin))

        CryptocurrencyTransactionsService.sell_crypto(self.coin.symbol, self.user, shares_to_sell)

        # Sell transaction created, coin should still be in portfolio (1 share), cash updated
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="sell").count(), 1)
        self.assertTrue(self.portfolio.crypto.filter(coin=self.coin))
        user_portfolio = Portfolio.objects.get(owner=self.user)
        self.assertEqual(user_portfolio.cash, (starting_balance + (self.coin.price * shares_to_sell)))

    def test_sell_crypto_equal_shares(self):
        shares_to_sell = 5
        self.assertTrue(self.portfolio.crypto.filter(coin=self.coin))

        CryptocurrencyTransactionsService.sell_crypto(self.coin.symbol, self.user, shares_to_sell)

        # All shares sold, coin should be removed
        self.assertFalse(self.portfolio.crypto.filter(coin=self.coin))

    def test_sell_crypto_invalid_shares(self):
        shares_to_sell = 6
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="sell").count(), 0)
        self.assertTrue(self.portfolio.crypto.filter(coin=self.coin))

        CryptocurrencyTransactionsService.sell_crypto(self.coin.symbol, self.user, shares_to_sell)

        # No transaction or sell, shares invalid 
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol=self.coin.symbol, type="sell").count(), 0)
        self.assertTrue(self.portfolio.crypto.filter(coin=self.coin))

    def test_sell_crypto_does_not_exist(self):
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol="TFBB", type="sell").count(), 0)
        self.assertFalse(self.portfolio.crypto.filter(coin__symbol="TFBB"))

        CryptocurrencyTransactionsService.sell_crypto("TFBB", self.user, 5)
        self.assertEqual(Transaction.objects.filter(owner=self.user, symbol="TFBB", type="sell").count(), 0)


class PortolioServiceTest(TestCase):

    def setUp(self):
        # Create users, some stocks and crpytos and add to portfolios
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        self.stock1 = Stock.objects.create(
            name='Apple Inc.',
            symbol='AAPL',
            market_cap=2000000000000,
            sector='Technology',
            price=150.0,
            dividend=0.75,
            volume=1000000,
            country='USA',
            exchange='NASDAQ',
            is_etf=False
        )
        self.stock2 = Stock.objects.create(
            name='Alphabet Inc.',
            symbol='GOOGL',
            market_cap=1800000000000,
            sector='Technology',
            price=2800.0,
            dividend=0.0,
            volume=800000,
            country='USA',
            exchange='NASDAQ',
            is_etf=False
        )

        self.crypto1 = Cryptocurrency.objects.create(
            name='Bitcoin',
            symbol='BTC',
            logo='https://example.com/bitcoin_logo.png',
            market_cap=1000000000000,
            price=45000.0,
            volume=500000,
        )
        self.crypto2 = Cryptocurrency.objects.create(
            name='Ethereum',
            symbol='ETH',
            logo='https://example.com/ethereum_logo.png',
            market_cap=500000000000,
            price=3000.0,
            volume=300000,
        )

        self.portfolio1 = Portfolio.objects.create(owner=self.user1, cash=100000)
        self.portfolio2 = Portfolio.objects.create(owner=self.user2, cash=80000)
        self.portfolio3 = Portfolio.objects.create(owner=self.user3, cash=50000)
        self.empty_portfolio = Portfolio.objects.create(owner=self.user1, cash=0)

        self.stock_portfolio1 = StockPortfolio.objects.create(owner=self.portfolio1, stock=self.stock1, shares=20)
        self.crypto_portfolio1 = CryptoPortfolio.objects.create(owner=self.portfolio1, coin=self.crypto1, shares=20)

        self.stock_portfolio2 = StockPortfolio.objects.create(owner=self.portfolio2, stock=self.stock2, shares=5)
        self.crypto_portfolio2 = CryptoPortfolio.objects.create(owner=self.portfolio2, coin=self.crypto2, shares=13)

        self.stock_portfolio3 = StockPortfolio.objects.create(owner=self.portfolio3, stock=self.stock1, shares=1)
        self.crypto_portfolio3 = CryptoPortfolio.objects.create(owner=self.portfolio3, coin=self.crypto2, shares=1)

        self.portfolio1.add_stock(self.stock_portfolio1)
        self.portfolio1.add_crypto(self.crypto_portfolio1)
        self.portfolio2.add_stock(self.stock_portfolio2)
        self.portfolio2.add_crypto(self.crypto_portfolio2)
        self.portfolio3.add_stock(self.stock_portfolio3)
        self.portfolio3.add_crypto(self.crypto_portfolio3)

    def test_portfolio_rankings_basic(self): 
        expected_rankings = [
            {
                "username": self.portfolio1.owner.username,
                "stocks_total": self.portfolio1.calculate_stock_total(),
                "crypto_total": self.portfolio1.calculate_crypto_total(),
                "cash": self.portfolio1.cash,
                "total": self.portfolio1.cash + float(self.portfolio1.calculate_crypto_total()) + float(self.portfolio1.calculate_stock_total())
            },
            {
                "username": self.portfolio2.owner.username,
                "stocks_total": self.portfolio2.calculate_stock_total(),
                "crypto_total": self.portfolio2.calculate_crypto_total(),
                "cash": self.portfolio2.cash,
                "total": self.portfolio2.cash + float(self.portfolio2.calculate_crypto_total()) + float(self.portfolio2.calculate_stock_total())
            },
            {
                "username": self.portfolio3.owner.username,
                "stocks_total": self.portfolio3.calculate_stock_total(),
                "crypto_total": self.portfolio3.calculate_crypto_total(),
                "cash": self.portfolio3.cash,
                "total": self.portfolio3.cash + float(self.portfolio3.calculate_crypto_total()) + float(self.portfolio3.calculate_stock_total())
            },
            {
                "username": self.portfolio1.owner.username,
                "stocks_total": self.empty_portfolio.calculate_stock_total(),
                "crypto_total": self.empty_portfolio.calculate_crypto_total(),
                "cash": self.empty_portfolio.cash,
                "total": self.empty_portfolio.cash + float(self.empty_portfolio.calculate_crypto_total()) + float(self.empty_portfolio.calculate_stock_total())
            }
        ]
        calculated_rankings = PortfolioService.calculate_portfolio_rankings(Portfolio.objects.all())

        self.assertEqual(expected_rankings, calculated_rankings)

    def test_portfolio_rankings_empty(self):
        rankings = PortfolioService.calculate_portfolio_rankings([])

        # Should return empty list
        self.assertEqual([], rankings)
        