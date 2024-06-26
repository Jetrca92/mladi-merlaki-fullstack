import requests

from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404
from django.utils import timezone
from django.utils.timezone import datetime

from marketdata.models import Cryptocurrency, Stock
from marketdata.utils import load_last_update_date, save_last_update_date
from portfolio.models import Transaction


class MarketDataService:

    @staticmethod
    @transaction.atomic
    def update_stock_data():
        url = "https://financialmodelingprep.com/api/v3/stock-screener"
        params = {
            "marketCapMoreThan": 2500000000,
            "isActivelyTrading": True,
            "apikey": "649b10518b05722dbbb49b29a80479fe",
            "isEtf": False,
            "isFund": False,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return  
        
        # Update or create a new instance of Stock with the provided data
        for stock in data:

            if stock.get("companyName") is None:
                # Skip stocks with null company names
                continue

            Stock.objects.update_or_create(
                symbol=stock["symbol"],
                defaults={
                    "name": stock["companyName"], 
                    "market_cap": stock["marketCap"], 
                    "sector": stock["sector"], 
                    "price": stock["price"], 
                    "dividend": stock["lastAnnualDividend"], 
                    "volume": stock["volume"], 
                    "country": stock["country"], 
                    "exchange": stock["exchangeShortName"], 
                    "is_etf": stock["isEtf"]
                }
            )

    @staticmethod
    @transaction.atomic
    def update_crypto_data():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": False,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return  
        
        for coin in data:
            Cryptocurrency.objects.update_or_create(
                symbol=coin["symbol"].upper(),
                defaults={
                    "name": coin["name"],
                    "logo": coin["image"],
                    "market_cap": coin["market_cap"],
                    "price": coin["current_price"],
                    "volume": coin["total_volume"]
                }
            )


    @staticmethod
    @transaction.atomic
    def market_update():
        try:
            last_update_date = load_last_update_date()
            if last_update_date and last_update_date.date() == datetime.today().date():
                return
            
            MarketDataService.update_crypto_data()
            MarketDataService.update_stock_data()
            save_last_update_date(datetime.today())
        except Exception as e:
            print(f"Error occurred during market update: {e}")


class CryptocurrencyService:
    
    @staticmethod
    def get_cryptocurrency_by_id(id):
        try:
            return Cryptocurrency.objects.get(id=id)
        except Cryptocurrency.DoesNotExist:
            raise Http404
        

class StockService:

    @staticmethod
    def get_stock_by_id(id):
        try:
            return Stock.objects.get(id=id)
        except Stock.DoesNotExist:
            raise Http404
        

class AppDataService:

    @staticmethod
    def get_app_data():
        app_data = {
            "monthly_volume": AppDataService.calculate_monthly_volume(),
            "transactions": AppDataService.calculate_yearly_transactions(),
            "users": User.objects.count(),
        }
        return app_data
    
    @staticmethod
    def calculate_monthly_volume():
        current_month = timezone.now().month
        monthly_transactions = Transaction.objects.filter(date__month=current_month)
        return round(sum(transaction.total() for transaction in monthly_transactions), 2)

    @staticmethod
    def calculate_yearly_transactions():
        current_year = timezone.now().year
        current_year_transactions = Transaction.objects.filter(date__year=current_year)
        return current_year_transactions.count()
            