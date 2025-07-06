import yfinance as yf
import pandas as pd 
import numpy as np  
import matplotlib.pyplot as plt 

from datetime import datetime

tickers = ['VT', 'VFMO']
start_date = '2018-02-13'
today = pd.Timestamp.today().normalize()
last_business_day = pd.bdate_range(end=today, periods=1)[0]
end_date = last_business_day.strftime('%Y-%m-%d')

data = yf.download(tickers, start=start_date, end=end_date)
data = data.dropna()

returns = data.pct_change().dropna()

print(returns)
returns.plot(title="Daily Returns")
plt.show()
