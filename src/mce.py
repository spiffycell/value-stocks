#!/usr/bin/python3

import sys
import yfinance as yf


def market_cap_to_equity(symbol):

    try:
        market_cap = symbol.info['marketCap']
    except:
        market_cap = 0

    balance_sheet = symbol.balance_sheet

    try:
        equity = balance_sheet.loc["Total Stockholder Equity"][0]
    except:
        equity = 0

    try:
        mce = round(market_cap / equity, 2)
    except:
        mce = 0

    return mce


symbol = yf.Ticker(sys.argv[1])
mce = market_cap_to_equity(symbol)
print(mce)
