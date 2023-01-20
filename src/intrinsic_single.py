#!/usr/bin/python3

# standard libraries
import logging
import requests
import re
import sys
import pandas as pd

# non-standard libraries
from metrics import Metrics
import yfinance

CAP_GAINS_TAX_RATE = 0.15
TIME_HORIZON_YEARS = 10
EARNINGS_MARKDOWN = .33


def get_wacc(ticker):
    """ Get WACC from GuruFocus."""
    # plug in the ticker to the url
    url = f'https://www.gurufocus.com/term/wacc/{ticker}/WACC-Percentage/{ticker}'
    # grab the page content
    page = requests.get(url).text

    # search for the percentage
    match = re.findall(r'[0-9]+\.[0-9]+%', page)[0].replace('%', '')
    wacc = float(match) / 100

    return wacc


def main(ticker):
    """ Perform Intrinsic value calculation."""

    # methodology of valuation
    metrics = Metrics()

    # get yfinance ticker object
    symbol = yfinance.Ticker(ticker) 
        
    # get net income (net earnings)
    try:
        earnings = metrics.net_income(symbol)
    except:
        earnings = 0
    print(f"Earnings: {earnings}")
    
    # get lookahead earnings, set as initial cash flow value
    lookahead = earnings * (1 - CAP_GAINS_TAX_RATE) 

    cash_flows = lookahead 
    print(f"Lookahead earnings: {lookahead}")

    # estimate rate of growth per year
    aegr = (metrics.avg_earnings_growth_rate(symbol) / 100)
    print(f"Avg growth rate: {aegr}")
    # mark down by 1/3rd (to be conservative)%
    adj_aegr = round(aegr * (1 - EARNINGS_MARKDOWN), 2) 

    print(f"Adjusted Avg growth rate: {adj_aegr}")

    # get working average costs of capital
    wacc = get_wacc(symbol.ticker)

    print(f"Weighted Avg Costs of Capital: {wacc}")

    # start discounting cash flows!
    for year in range(0, TIME_HORIZON_YEARS - 1):
        # 1) take existing cash flow
        # 2) take the earnings growth of existing cash flow
        # 3) discount the earnings growth cash 
        # 4) add the result into existing cash flows
        # 5) repeat
        cash_flows += ((cash_flows * adj_aegr) / (1 + wacc))
        print(f"Cash flows after {year + 1} year: {cash_flows}")

    # get free cash flow
    fcf = metrics.free_cash_flow(symbol) 
    print(f"Free Cash Flow: {fcf}")

    # discount terminal value
    term_growth = .04
    terminal_value = (fcf * (1 + term_growth)) / (wacc - term_growth)

    print(f"Terminal Value: {terminal_value}")

    # and add it to the total
    dcf = cash_flows + terminal_value

    # knock off liabilities and minority interest
    liabilities = metrics.liabilities(symbol) 
    dcf -= liabilities

    min_interest = metrics.minority_interest(symbol)
    dcf -= min_interest

    # divide total by shares outstanding
    shares_outstanding = metrics.shares_outstanding(symbol)

    try:
        dcf_per_share = round(dcf / shares_outstanding, 2)
    except:
        dcf_per_share = 0


    # dcf price per share with current price per share
    pps = metrics.price_per_share(symbol)

    # get expected growth over time
    try:
        growth = round((dcf_per_share - pps) / pps, 2) * 100
    except:
        growth = 0

    # output the results
    print(f"\n\n\nCurrent Price per Share of {symbol.ticker}: {pps}")
    print(f"Future Price per Share of {symbol.ticker}: {dcf_per_share}")
    print(f"This is a growth of {growth}% over {TIME_HORIZON_YEARS} years")


if __name__ == "__main__":
    # get ticker object from yahoo finance api
    ticker = sys.argv[1]

    main(ticker)
