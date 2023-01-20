import sys
import yfinance
from metrics import Metrics

ticker = sys.argv[1]
symbol = yfinance.Ticker(ticker)

metric = Metrics()

roa = metric.return_on_assets(symbol)
print(f'ROA: {metric.return_on_assets(symbol)}')
roe = metric.return_on_equity(symbol)
print(f'ROE: {metric.return_on_equity(symbol)}')

print(f"MCE: {metric.market_cap_to_equity(symbol)}")
print(f"NC/E: {metric.net_income_to_ev(symbol)}")
metric.avg_earnings_growth_rate(symbol)
metric.avg_fcf_growth_rate(symbol)
print(f"Inc date: {metric.inc_date(symbol)}")
exp_rat = metric.expense_ratio(symbol)
print(f"Expense ratio: {exp_rat}")
