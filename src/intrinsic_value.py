#!/usr/bin/python3

# standard libraries
import logging
import re
import requests
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
    try:
        match = re.findall(r'[0-9]+\.[0-9]+%', page)[0].replace('%', '')
        wacc = float(match) / 100
    except:
        wacc = 0.07

    return wacc


def main(dataframe, infile):
    """ Perform Intrinsic value calculation."""

    # methodology of valuation
    metrics = Metrics()

    # get list of ticker symbols
    tickers = list(dataframe.to_dict()['symbol'].values())

    for i in range(0, len(tickers)):
        # get yfinance ticker object
        symbol = yfinance.Ticker(tickers[i]) 
        
        # net income
        niev = round(metrics.net_income_to_ev(symbol), 2)

        # add data to csv
        dataframe.loc[i, 'niev'] = niev


        # get net margin
        net_margin = metrics.net_margin(symbol)

        # add data to csv
        dataframe.loc[i, 'net_margin'] = net_margin


        # cash ratio
        cash = metrics.cash_ratio(symbol)

        # add data to csv
        dataframe.loc[i, 'cash'] = cash

        
        # return on assets
        roa = round(metrics.avg_return_on_assets(symbol), 2)

        # add data to csv
        dataframe.loc[i, 'roa'] = roa


        # get net income (net earnings)
        try:
            earnings = metrics.net_income(symbol)
        except:
            earnings = 0
        print(f"Earnings: {earnings}")
    
        # get lookahead earnings
        lookahead = earnings * (CAP_GAINS_TAX_RATE)
        cash_flows = lookahead 
        print(f"Lookahead earnings: {lookahead}")

        # estimate rate of growth per year
        aegr = (metrics.avg_earnings_growth_rate(symbol) / 100)
        print(f"Avg growth rate: {aegr}")
        # mark down by 1/3rd (to be conservative)%
        adj_aegr = round(aegr * (1 - EARNINGS_MARKDOWN), 2) 

        # add data to csv
        dataframe.loc[i, 'adj growth'] = adj_aegr

        # get average returns on capital
        roc = metrics.avg_return_on_capital(symbol) 

        # add data to csv
        dataframe.loc[i, 'avg roc'] = roc

        print(f"Adjusted Avg growth rate: {adj_aegr}")

        # get working average costs of capital
        wacc = get_wacc(symbol.ticker)

        # add data to csv
        dataframe.loc[i, 'wacc'] = wacc

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
        term_growth = .05

        if wacc < term_growth or wacc == term_growth:
            term_growth = wacc - (wacc * 0.5)

        # get terminal value
        growth_ratio_diff = wacc - term_growth
        
        if growth_ratio_diff == 0:
            growth_ratio_diff = 0.01

        terminal_value = round((fcf * (1 + term_growth)) / (growth_ratio_diff), 2)

        # and add it to the total
        dcf = cash_flows + terminal_value

        # knock off liabilities and minority interest
        liabilities = metrics.liabilities(symbol) 
        dcf -= liabilities

        min_interest = metrics.minority_interest(symbol)
        dcf -= min_interest

        # add data to csv
        dataframe.loc[i, 'dcf'] = round(dcf, 2)

        # divide total by shares outstanding
        shares_outstanding = metrics.shares_outstanding(symbol)

        try:
            dcf_per_share = round(dcf / shares_outstanding, 2)
        except:
            dcf_per_share = 0

        # add data to csv
        dataframe.loc[i, 'future price'] = dcf_per_share

        # dcf price per share with current price per share
        pps = metrics.price_per_share(symbol)

        # add data to csv
        dataframe.loc[i, 'current price'] = pps

        # get expected growth over time
        try:
            growth = round((dcf_per_share - pps) / pps, 2) * 100
        except:
            growth = 0

        # add data to csv
        dataframe.loc[i, 'growth'] = growth

        # output the results
        print(f"\n\n\nCurrent Price per Share of {symbol.ticker}: {pps}")
        print(f"Future Price per Share of {symbol.ticker}: {dcf_per_share}")
        print(f"This is a growth of {growth}% over {TIME_HORIZON_YEARS} years")

        dataframe.to_csv(infile, index=False)


if __name__ == "__main__":
    # get ticker object from yahoo finance api
    infile = sys.argv[1]
    dataframe = pd.read_csv(infile)
    main(dataframe, infile)
