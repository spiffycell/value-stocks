#!/usr/bin/python3

import sys
import yfinance as yf

ticker = sys.argv[1]
symbol = yf.Ticker(ticker)
balance_sheet = symbol.get_balance_sheet()

current_assets = balance_sheet.loc["Total Current Assets"][0]
print(f"current assets: {current_assets}")

try:
    receivables = balance_sheet.loc["Net Receivables"][0]
    print(f"receivables: {receivables}")
except KeyError:
    receivables = 0
    print(f"receivables: {receivables}")

try:
    inventory = balance_sheet.loc["Inventory"][0]
    print(f"inventory: {inventory}")
except KeyError:
    inventory = 0
    print(f"inventory: {inventory}")

liabilities = balance_sheet.loc["Total Liab"][0]
print(f"liabilities: {liabilities}")
nnwc = current_assets + (0.75 * receivables) + (0.5 * inventory) - liabilities
print(f"nnwc: {nnwc}")
market_cap = symbol.info['marketCap']
print(f"market cap: {market_cap}")

net_ratio = round(market_cap / nnwc, 2)
print(f"{ticker} net ratio: {net_ratio}")
