class Metrics:
    def __init__(self, debug):
        """
        Initialization of business metrics and \
                financial accounting attributes.
        """
        self.debug = debug


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

        try:
            liabilities = balance_sheet.loc["Total Liab"][0]
        except:
            liabilities = 0

        print(f"liabilities: {liabilities}")

        try:
            nnwc = current_assets + (0.75 * receivables) + (0.5 * inventory) - liabilities
        except:
            nnwc = 0
        print(f"nnwc: {nnwc}")

        try:
            market_cap = symbol.info['marketCap']
        except:
            market_cap = 0
        print(f"market cap: {market_cap}")

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
        print(f"debt: {debt}")

        try:
            equity = balance_sheet.loc["Total Stockholder Equity"][0]
        except:
            equity = 0
        print(f"equity: {equity}")

        try:
            eqd = round(equity / debt, 2)
        except:
            eqd = 0
        print(f"equity-to-debt: {eqd}")
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

        try:
            market_cap = symbol.info['marketCap']
        except:
            market_cap = 0
        print(f"market cap: {market_cap}")

        try:
            ev = market_cap + total_debt - cce
        except:
            ev = 0
        print(f"ev: {ev}")

        try:
            earnings_yield = round(ebit / ev, 2)
        except:
            earnings_yield = 0
        print(f"earnings yield: {earnings_yield}")
        return earnings_yield


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
        print(f"ebit: {ebit}")

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

        try:
            nwc = current_assets - current_liabilities
        except:
            nwc = 0
        print(f"net working capital: {nwc}")

        try:
            fixed_assets = balance_sheet.loc["Property Plant Equipment"][0]
            print(f"fixed assets: {fixed_assets}")
        except:
            fixed_assets = 0
            print(f"fixed assets: {fixed_assets}")

        try:
            roc = round(ebit / (nwc + fixed_assets), 2)
        except:
            roc = 0
        print(f"return on capial: {roc}")
        return roc

