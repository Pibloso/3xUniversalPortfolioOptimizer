import yfinance as yf
import pandas as pd 
import numpy as np  
import matplotlib.pyplot as plt 

from datetime import datetime

tickers = ['VT', 'VFMO']
borrow_rate = 0.092
start_date = '2018-02-20'
today = pd.Timestamp.today().normalize()
last_business_day = pd.bdate_range(end=today, periods=1)[0]
end_date = last_business_day.strftime('%Y-%m-%d')

cash_yield = yf.Ticker("PSA.TO").info.get("yield", None)
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']

returns = data[tickers].pct_change().dropna()
returns['CASH'] = (1 + cash_yield)**(1/252)-1
returns['BORROW'] = (1 - borrow_rate)**(1/252)-1

print(returns)
plt.plot(returns)
plt.show()
