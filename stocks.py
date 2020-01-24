from yahooquery import Ticker
import time
import json



class Stock():
    pass



def get_stock_price(ticker):
    st=Ticker(ticker)
    stk=st.price[ticker]
    return {'symbol': stk['symbol'],'name': stk['longName'],'pre-market': stk['preMarketPrice'],'price': stk['regularMarketPrice'], 'day-high': stk['regularMarketDayHigh'],'day-low':  stk['regularMarketDayLow'] }

    
def get_stock_price_history(ticker):
    stk=Ticker(ticker).history()
    hist={}
    hist["axis"]=[x.strftime("%Y-%m-%d") for x in stk.index.tolist()]
    hist["close"]=stk['close'].tolist()
    hist["high"]=stk['high'].tolist()
    hist["low"]=stk['low'].tolist()
    hist["open"]=stk["open"].tolist()
    return hist







