#!/usr/bin/python3

import yfinance
from metrics import Metrics

symbol = yfinance.Ticker('AAPL')
roc = Metrics().avg_return_on_capital(symbol)
print(f"Average Return on Capital: {roc}")
