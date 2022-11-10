from os import getenv
import re

class Metrics:
    def __init__(self):
        """
        Initialization of business metrics and \
                financial accounting attributes.
        """
        self.debug = getenv("DEBUG", False)


    def net_net(self, symbol):
        """
        The Graham net-net ratio is a measure of the \
                intrinsic value of the company.

        This is the key indicator of whether or not a \
                company is undervalued. 

        Net-Net takes the liquidation value of the company \
                and measures it against the market cap

        This makes Net-Net a more reliable measure of an \
                undervalued company than Market Cap to Equity.
        """
        balance_sheet = symbol.get_balance_sheet()

        try:
            current_assets = balance_sheet.loc["Total Current Assets"][0]
        except:
            current_assets = 0

        try:
            receivables = balance_sheet.loc["Net Receivables"][0]
        except KeyError:
            receivables = 0

        try:
            inventory = balance_sheet.loc["Inventory"][0]
        except KeyError:
            inventory = 0

        try:
            liabilities = balance_sheet.loc["Total Liab"][0]
        except:
            liabilities = 0


        try:
            nnwc = current_assets + (0.75 * receivables) + (0.5 * inventory) - liabilities
        except:
            nnwc = 0

        try:
            market_cap = symbol.info['marketCap']
        except:
            market_cap = 0

        try:
            net_ratio = round(market_cap / nnwc, 2)
        except:
            net_ratio = 0
        return net_ratio


    def market_cap_to_equity(self, symbol):
        """
        Market Capitalization to Equity is a key indicator, \
                although, not solely sufficient, in determining \
                whether or not a company is undervalued.

        If the Market Cap to Equity ratio is a positive value below \
                0.6, that indicates an interesting opportunity.

        A low Market Cap to Equity means that the market valuation of \
                the company is less than the amount of money owed to \
                investors. So, a potential cash-out to investors would \
                result in profit.
        """
        try:
            print(symbol.ticker)
            market_cap = symbol.info['marketCap']
            print(f'market_cap: {market_cap}')
        except:
            market_cap = 0

        balance_sheet = symbol.balance_sheet

        try:
            equity = balance_sheet.loc["Total Stockholder Equity"][0]
            print(f'equity: {equity}')
        except:
            equity = 0

        try:
            mce = round(market_cap / equity, 2)
        except:
            mce = 0

        print(f"market cap to equity: {mce}")
        return mce


    def avg_return_on_equity(self, symbol):
        cashflow = symbol.cashflow
        b_sheet = symbol.balance_sheet

        growth = []

        try:
            for i in range(0, len(cashflow.loc['Net Income']) - 1):
                growth.append((cashflow.loc['Net Income'][i]) / b_sheet.loc['Total Stockholder Equity'][i])
        except:
            growth = []

        if len(growth) == 0:
            avg = 0
        else:
            avg = sum(growth) / len(growth)
        print(f"Avg return on equity: {avg}%")
        return avg
        

    def return_on_equity(self, symbol):
        try:
            net_income = symbol.cashflow.loc["Net Income"][0]
        except:
            net_income = 0

        balance_sheet = symbol.get_balance_sheet()

        try:
            equity = balance_sheet.loc["Total Stockholder Equity"][0]
            return net_income / equity
        except:
            roe = 0
        return roe


    def inc_date(self, symbol):
        try:
            inc = re.findall(r'[1]+[7-9]+[0-9]+[0-9]+', symbol.info['longBusinessSummary'])
            print(f'inc date: {inc}')
            if not inc:
                inc = ''
            elif len(inc) > 1:
                inc = inc[-1]
            return inc
        except:
            inc = ''
            return inc


    def free_cash_flow(self, symbol):
        """
        Free cash flow is the truth serum of business accounting
        Think of free cash flow as the net receipts

        FCF = (Operational Income) - (Capital Expenditures)
        """
        result = 0

        cashflow = symbol.cashflow
        try:
            op_inflows = cashflow.loc['Total Cash From Operating Activites']
        except:
            op_inflows = 0
        try:
            cap_ex = cashflow.loc['Capital Expenditures']
        except:
            cap_ex = 0
        try:
            recent_fcf = op_inflows[0] - cap_ex[0]
        except:
            recent_fcf = 0
    
        try:
            past_fcf = op_inflows[-1] - cap_ex[-1]
        except:
            past_fcf = 0

        if recent_fcf < 0 and past_fcf < 0:
            result = 1

        return result


    def equity_to_debt_ratio(self, symbol):
        """
        Equity to debt is the inverse of the DE ratio

        DE measures the financial health of the company, \
                by comparing the amount owed to creditors to the \
                amount owed to investors.

        A DE ratio below 2 is good
        """
        balance_sheet = symbol.get_balance_sheet()

        try:
            debt = balance_sheet.loc["Total Liab"][0]
        except:
            debt = 0

        try:
            equity = balance_sheet.loc["Total Stockholder Equity"][0]
        except:
            equity = 0

        try:
            eqd = round(equity / debt, 2)
        except:
            eqd = 0
        return eqd


    def earnings_yield(self, symbol):
        """
        Earnings yield, also known as (EBITDA / Enterprise Value), is \
                a great measurement of earnings against debt.

        Generally, some value investors look at ratios like \
                price-to-equity to determine if a company is \
                fairly-valued. However, PE doesn't factor in \
                debt. Meaning, that a company could have a low \
                price due to a major accumulation of debt, and \
                loss of investor confidence. This is an example \
                of a "value trap".

        Factoring debt into the calculation (like EBITDA / EV), \
                penalizes companies with high amounts of debt, \
                and only exposes the investor to companies with \
                both high earnings and low debt.
        """
        try:
            ebit = symbol.earnings.values[-1][-1]
        except:
            ebit = 0
        balance_sheet = symbol.get_balance_sheet()

        try:
            cce = balance_sheet.loc["Cash"][0]
        except:
            cce = 0

        try:
            total_debt = balance_sheet.loc["Long Term Debt"][0]
        except:
            total_debt = 0

        try:
            market_cap = symbol.info['marketCap']
        except:
            market_cap = 0

        try:
            ev = market_cap + total_debt - cce
        except:
            ev = 0

        try:
            earnings_yield = round(ebit / ev, 2)
        except:
            earnings_yield = 0
        return earnings_yield


    def avg_return_on_assets(self, symbol):
        cashflow = symbol.cashflow
        b_sheet = symbol.balance_sheet

        growth = []

        try:
            for i in range(0, len(cashflow.loc['Net Income']) - 1):
                growth.append((cashflow.loc['Net Income'][i]) / b_sheet.loc['Total Assets'][i])
        except:
            growth = []

        if len(growth) == 0:
            avg = 0
        else:
            avg = sum(growth) / len(growth)
        print(f"Avg return on assets: {avg}%")
        return avg


    def return_on_assets(self, symbol):
        """
        Return on assets is a reliable metric for profitability.
        A high return on assets indicates that a company is highly \
                effective at converting their assets into Net Income.

        A low return on assets can either indicate that the company \
                is ineffective at asset to earnings conversion, or that \
                it operates in a business sector where that conversion \
                isn't central to their ability to operate (i.e. banking).
        """
        try:
            net_income = symbol.cashflow.loc["Net Income"][0]
        except:
            net_income = 0

        try:
            total_assets = symbol.balance_sheet.loc["Total Assets"][0]
        except:
            total_assets = 0

        try:
            roa = net_income / total_assets
        except:
            roa = 0
        return roa


    def net_income_to_ev(self, symbol):
        try:
            net_income = symbol.cashflow.loc["Net Income"][0]
        except:
            net_income = 0

        try:
            market_cap = symbol.info['marketCap']
        except:
            niev = 0
            return niev

        try:
            total_debt = balance_sheet.loc["Long Term Debt"][0]
        except:
            total_debt = 0
        try:
            cce = balance_sheet.loc["Cash"][0]
        except:
            cce = 0

        if market_cap is None:
            niev = 0
            return niev
        else:
            ev = market_cap + total_debt - cce
            niev = net_income / ev

        return niev


    def return_on_capital(self, symbol):
        """
        Joel Greenblatt, in his 'Little Book That Beats the Market' uses \
                ROC as a way to determine companies with high profitability.

        ROC is often used as a substitute for Return on Assets (ROA). Rather \
                than using total assets as a penalizing factor, ROC utilizes \
                Net Working Capital (current assets less current liabilities).

        The net effect of this calculation is to give a more precise view of \
                assets, excluding long-term assets (PPE).
        """
        try:
            ebit = symbol.earnings.values[-1][-1]
        except:
            ebit = 0

        balance_sheet = symbol.get_balance_sheet()

        try:
            current_assets = balance_sheet.loc["Total Current Assets"][0]
        except:
            current_assets = 0

        try:
            current_liabilities = balance_sheet.loc["Total Current Liabilities"][0]
        except:
            current_liabilities = 0

        try:
            nwc = current_assets - current_liabilities
        except:
            nwc = 0

        try:
            fixed_assets = balance_sheet.loc["Property Plant Equipment"][0]
        except:
            fixed_assets = 0

        try:
            roc = round(ebit / (nwc + fixed_assets), 2)
        except:
            roc = 0
        return roc

    def avg_earnings_growth_rate(self, symbol):
        earnings = symbol.earnings.values
        growth = []

        for i in range(0, len(earnings) - 1):
            growth.append((earnings[i + 1][1] - earnings[i][1]) / earnings[i][1])

        if len(growth) == 0:
            avg = 0
        else:
            avg = round((sum(growth) / len(growth)) * 100, 2)
        print(f"Avg earnings growth rate: {avg}%")
        return avg


    def avg_fcf_growth_rate(self, symbol):
        try:
            fcf = symbol.cashflow.loc['Total Cash From Operating Activities'] - symbol.cashflow.loc['Capital Expenditures']
        except:
            try:
                fcf = symbol.cashflow.loc['Total Cash From Operating Activities']
            except:
                fcf = []

        growth = []

        for i in range(0, len(fcf) - 1):
            growth.append((fcf[i + 1] - fcf[i]) / fcf[i])

        try:
            avg = round((sum(growth) / len(growth)) * 100, 2)
        except:
            avg = 0 
        print(f"Avg FCF growth rate: {avg}%")
        return avg


    def wacc(self, symbol, avg_ret):
        """ Working Average Costs of Capital """

        try:
            mvd = symbol.balance_sheet.loc['Long Term Debt'][0]
        except:
            mvd = 0
            print(f"market vlaue of debt: {mvd}")

        try:
            mve = symbol.balance_sheet.loc['Total Stockholder Equity'][0] 
        except:
            mve = 0
        print(f"market value of equity: {mve}")

        tsc = mvd + mve
        print(f"total value of source of capital: {tsc}")

        cost_of_equity = avg_ret

        try:
            cost_of_debt = abs(symbol.financials.loc['Interest Expense'][0] / mvd)
        except:
            cost_of_debt = 0
        print(f"cost of debt: {cost_of_debt}")

        try:
            tax_rate = round(abs(symbol.financials.loc['Income Tax Expense'][0] / symbol.financials.loc['Ebit'][0]), 2)
        except:
            tax_rate = 0
        print(f"tax rate: {tax_rate}")

        try:
            debt_capital_value = ((mvd / tsc) * cost_of_debt * (1 - tax_rate))
        except:
            debt_capital_value = 0

        try:
            equity_capital_value = ((mve / tsc) * cost_of_equity)
        except:
            equity_capital_value = 0

        return (debt_capital_value + equity_capital_value)


    def average_returns(self, roa, roe):
        return (roa + roe / 2)


    def years_to_double(self, wacc, roa):
        try:
            ytd = 1 / roa
        except:
            ytd = 10
        fytd = (wacc * 10) + ytd

        return fytd

