#!/usr/bin/python3

import sys
import yfinance as yf

ticker = sys.argv[1]
symbol = yf.Ticker(ticker)

ebit = symbol.earnings.values[-1][-1]
print(f"ebit: {ebit}")
balance_sheet = symbol.get_balance_sheet()

try:
    cce = balance_sheet.loc["Cash"][0]
except:
    cce = 0
print(f"current assets: {cce}")

try:
    total_debt = balance_sheet.loc["Long Term Debt"][0]
    print(f"total debt: {total_debt}")
except:
    total_debt = 0
    print(f"total debt: {total_debt}")

market_cap = symbol.info['marketCap']
print(f"market cap: {market_cap}")

ev = market_cap + total_debt - cce
print(f"ev: {ev}")

earnings_yield = round(ebit / ev, 2)
print(f"{ticker} earnings yield: {earnings_yield}")
