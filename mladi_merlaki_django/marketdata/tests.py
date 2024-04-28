import json
import os
import unittest
from unittest.mock import patch, Mock, MagicMock

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import datetime
from marketdata.models import Stock, Cryptocurrency
from marketdata.services import AppDataService, StockService, CryptocurrencyService, MarketDataService
from marketdata.utils import load_last_update_date, save_last_update_date
from requests.exceptions import RequestException


class AppDataServicesTest(TestCase):

    def setUp(self):
        self.mock_user = Mock(spec=User)
        self.mock_user.id = 1

        self.mock_transaction1 = Mock(owner=self.mock_user, symbol='ABC', asset_class='stock', shares=10, price=100, type='buy', date=timezone.now())
        self.mock_transaction1.total.return_value = self.mock_transaction1.shares * self.mock_transaction1.price

        self.mock_transaction2 = Mock(owner=self.mock_user, symbol='DEF', asset_class='crypto', shares=20, price=50, type='sell', date=timezone.now())
        self.mock_transaction2.total.return_value = self.mock_transaction2.shares * self.mock_transaction2.price

        self.mock_transaction3 = Mock(owner=self.mock_user, symbol='BTV', asset_class='crypto', shares=1, price=1000, type='buy', date=timezone.now() - timezone.timedelta(days=2*30))
        self.mock_transaction3.total.return_value = self.mock_transaction3.shares * self.mock_transaction3.price
        
        self.mock_transaction4 = Mock(owner=self.mock_user, symbol='BTVR', asset_class='crypto', shares=15, price=100, type='sell', date=timezone.now() + timezone.timedelta(days=2*30))
        self.mock_transaction4.total.return_value = self.mock_transaction4.shares * self.mock_transaction4.price

        self.mock_queryset = MagicMock()
        self.mock_queryset.count.return_value = len([self.mock_transaction1, self.mock_transaction2, self.mock_transaction3, self.mock_transaction4])

    @patch('marketdata.services.Transaction.objects.filter')
    def test_calculate_monthly_volume(self, mock_filter):
        mock_filter.return_value = [self.mock_transaction1, self.mock_transaction2]
        
        monthly_volume = AppDataService.calculate_monthly_volume()
        expected_volume = self.mock_transaction1.total() + self.mock_transaction2.total()
        
        self.assertEqual(monthly_volume, expected_volume)

    @patch('marketdata.services.Transaction.objects.filter')
    def test_calculate_yearly_transactions(self, mock_filter):
        mock_filter.return_value = self.mock_queryset

        yearly_transactions = AppDataService.calculate_yearly_transactions()
        expected_transactions = self.mock_queryset.count()

        self.assertEqual(yearly_transactions, expected_transactions)


class StockServiceTest(TestCase):
    
    def setUp(self):
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

    def test_get_stock_by_id(self):
        self.assertEqual(self.stock, StockService.get_stock_by_id(self.stock.id))
        with self.assertRaises(Http404):
            StockService.get_stock_by_id(9999)


class CryptocurrencyServiceTest(TestCase):

    def setUp(self):
        self.coin = Cryptocurrency.objects.create(
            name="TestCoin",
            symbol="TTC",
            logo="none",
            market_cap=12,
            price=100,
            volume=14,
        )

    def test_get_cryptocurrency_by_id(self):
        self.assertEqual(self.coin, CryptocurrencyService.get_cryptocurrency_by_id(self.coin.id))
        with self.assertRaises(Http404):
            CryptocurrencyService.get_cryptocurrency_by_id(9999)


class MarketDataServiceTest(TestCase):

    def setUp(self):
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = [
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "marketCap": 2000000000000,
                "sector": "Technology",
                "price": 150.50,
                "lastAnnualDividend": 2.00,
                "volume": 1000000,
                "country": "USA",
                "exchangeShortName": "NASDAQ",
                "isEtf": False
            },
            {
                "symbol": "VWAGY",
                "companyName": "Volkswagen AG",
                "marketCap": 150000000000,
                "sector": "Automotive",
                "price": 40.25,
                "lastAnnualDividend": 1.50,
                "volume": 750000,
                "country": "Germany",
                "exchangeShortName": "XETRA",
                "isEtf": False
            },
        ]

        self.mock_crypto_response = MagicMock()
        self.mock_crypto_response.status_code = 200
        self.mock_crypto_response.json.return_value = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "image": "https://example.com/bitcoin_logo.png",
                "market_cap": 1000000000000,
                "current_price": 50000.00,
                "total_volume": 1000000
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "image": "https://example.com/ethereum_logo.png",
                "market_cap": 500000000000,
                "current_price": 2500.00,
                "total_volume": 500000
            },
        ]

    @patch('marketdata.services.requests.get')
    def test_update_stock_data_success(self, mock_get):
        mock_get.return_value = self.mock_response
        MarketDataService.update_stock_data()

        self.assertTrue(Stock.objects.filter(symbol="AAPL").exists())
        self.assertTrue(Stock.objects.filter(symbol="VWAGY").exists())
        self.assertFalse(Stock.objects.filter(symbol="KRK").exists())

    @patch('marketdata.services.requests.get')
    def test_update_stock_data_error(self, mock_get):
        # Mock the requests.get method to raise an error
        mock_get.side_effect = Exception("Test error")

        with self.assertRaises(RequestException):
            try:
                MarketDataService.update_stock_data()
            except Exception as e:
                raise RequestException(f"Caught exception: {e}")

        self.assertEqual(Stock.objects.count(), 0) 

    @patch('marketdata.services.requests.get')
    def test_update_cryptocurrency_data_success(self, mock_get):
        mock_get.return_value = self.mock_crypto_response
        MarketDataService.update_crypto_data()

        self.assertTrue(Cryptocurrency.objects.filter(symbol="BTC").exists())
        self.assertTrue(Cryptocurrency.objects.filter(symbol="ETH").exists())
        self.assertFalse(Cryptocurrency.objects.filter(symbol="ADA").exists())

    @patch('marketdata.services.requests.get')
    def test_update_cryptocurrency_data_error(self, mock_get):
        # Mock the requests.get method to raise an error
        mock_get.side_effect = Exception("Test error")

        with self.assertRaises(RequestException):
            try:
                MarketDataService.update_crypto_data()
            except Exception as e:
                raise RequestException(f"Caught exception: {e}")

        self.assertEqual(Cryptocurrency.objects.count(), 0) 


class TestUtilsFunctions(unittest.TestCase):

    def setUp(self):
        self.temp_file = "last_update_date.json"

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_load_last_update_date_file_exists(self):
        test_date = datetime(2022, 4, 1, 12, 0, 0)
        with open(self.temp_file, "w") as f:
            json.dump(test_date.isoformat(), f)

        loaded_date = load_last_update_date()
        self.assertEqual(loaded_date, test_date)

    def test_load_last_update_date_file_not_exists(self): 
        loaded_date = load_last_update_date()
        self.assertIsNone(loaded_date)
    
    def test_save_last_update_date(self):
        test_date = datetime(2022, 5, 1, 12, 0, 0)
        save_last_update_date(test_date)

        with open(self.temp_file, "r") as f:
            loaded_date_iso = f.read()

        loaded_date = datetime.fromisoformat(json.loads(loaded_date_iso))
        self.assertEqual(loaded_date, test_date)

if __name__ == "__main__":
    unittest.main()


    
