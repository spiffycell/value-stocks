#!/usr/bin/python3

import yfinance as yf
import sys


def return_on_assets(symbol):

    try:
        net_income = symbol.cashflow.loc["Net Income"][0]
    except:
        net_income = 0
    print(f"net income: {net_income}")

    try:
        total_assets = symbol.balance_sheet.loc["Total Assets"][0]
    except:
        total_assets = 0
    print(f"total assets: {total_assets}")

    try:
        roa = round(net_income / total_assets, 2)
    except:
        roa = 0
    print(f"return on assets: {roa}")
    return roa

symbol = yf.Ticker(sys.argv[1])
roa = return_on_assets(symbol)
print(roa)


