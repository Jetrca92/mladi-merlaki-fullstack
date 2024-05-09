# Mladi Merlaki

## Installation
```bash
# Create Python3 virtualenv, and install packages.
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
# Run DB migrations.
python3 manage.py migrate
```

## Introduction
Mladi Merlaki: A dynamic online game where players simulate stock and cryptocurrency trading. Start with $100,000 and aim to reach $1,000,000 through savvy investments. Suitable for adults seeking financial challenges and children learning about finance. Learn market dynamics, strategies, and essential concepts. Are you the next Merlak?

## Features

### Market Data Management:
- Users can fetch and update market data for stocks and cryptocurrencies from external APIs.
- Users can view market data for stocks and cryptocurrencies.

### Stock Management:
- Users can retrieve detailed information about specific stocks.
- Users can view market data for stocks.

### Cryptocurrency Management:
- Users can retrieve detailed information about specific cryptocurrencies.
- Users can view market data for cryptocurrencies.

### Application Data:
- Users can view application-level data such as monthly transaction volumes and yearly transaction counts.
- Users can view user counts.

### Portfolio management:
- Users can view their portfolio, including cash balance, stocks, and cryptocurrencies.
- Users can buy and sell stocks.
- Users can buy and sell cryptocurrencies.

### Transactions:
- Users can view their transaction history, including details such as asset type, transaction type, quantity, price, and timestamp.

### Rankings:
- Users can view rankings of the top portfolios based on total value, including stocks, cryptocurrencies, and cash.
