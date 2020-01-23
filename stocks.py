from yahooquery import Ticker


class Stock():
    

def get_stock_summary(ticker):
    stk=Ticker(ticker)

    del stk.summary_profile[ticker]['longBusinessSummary']
    return stk.summary_profile[ticker]

print(get_stock_summary('TSLA'))