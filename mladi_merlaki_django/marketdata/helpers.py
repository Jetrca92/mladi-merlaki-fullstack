import os
import json
import random
import urllib.parse
import requests

from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.timezone import datetime

from marketdata.models import Stock, Cryptocurrency
from portfolio.models import StockPortfolio, CryptoPortfolio, Portfolio


def update_stock_data():
    url = "https://financialmodelingprep.com/api/v3/stock-screener"
    params = {
        "marketCapMoreThan": 2500000000,
        "isActivelyTrading": True,
        "apikey": "649b10518b05722dbbb49b29a80479fe",
        "isEtf": False,
        "isFund": False,
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Update or create a new instance of Stock with the provided data
    for stock in data:
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


def update_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False,
    }
    response = requests.get(url, params=params)
    data = response.json()

    for coin in data:
        Cryptocurrency.objects.update_or_create(
            symbol=coin["symbol"],
            defaults={
                "name": coin["name"],
                "logo": coin["image"],
                "market_cap": coin["market_cap"],
                "price": coin["current_price"],
                "volume": coin["total_volume"]
            }
        )


def load_last_update_date():
    # Load the last update date from a file or database
    if os.path.exists("last_update_date.json"):
        with open("last_update_date.json", "r") as f:
            return datetime.fromisoformat(json.load(f))
    else:
        return None


def save_last_update_date(date):
    # Save the last update date to a file or database
    with open("last_update_date.json", "w") as f:
        json.dump(date.isoformat(), f)


def market_update(date):
    
    last_update_date = load_last_update_date()

    if last_update_date and last_update_date.date() == datetime.today().date():
        return
    
    update_crypto_data()
    update_stock_data()

    save_last_update_date(datetime.today())