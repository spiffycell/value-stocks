#!/usr/bin/python3

import sys
import yfinance as yf

ticker = sys.argv[1]
symbol = yf.Ticker(ticker)

ebit = symbol.earnings.values[-1][-1]
balance_sheet = symbol.get_balance_sheet()

try:
    current_assets = balance_sheet.loc["Total Current Assets"][0]
except:
    current_assets = 0
print(f"current assets: {current_assets}")

try:
    current_liabilities = balance_sheet.loc["Total Current Liabilities"][0]
except:
    current_liabilities = 0
print(f"current liabilities: {current_liabilities}")

nwc = current_assets - current_liabilities
print(f"net working capital: {nwc}")

try:
    fixed_assets = balance_sheet.loc["Property Plant Equipment"][0]
    print(f"fixed assets: {fixed_assets}")
except:
    fixed_assets = 0
    print(f"fixed assets: {fixed_assets}")

roc = round(ebit / (nwc + fixed_assets), 2)
print(f"{ticker} return on capial: {roc}")

