#install command: pip install mplfinance
import mplfinance as mpf
import tushare as ts
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.pylab import date2num
import numpy as np

#sns.set()
#token 认证
ts.set_token('d65a77709e16a01f2ab84cee8040922ad06df5fe4c65993ff3f7d2cf') #18513603069
pro = ts.pro_api()

daily = pro.daily(ts_code='300669.SZ', start_date='20211015')
print(daily)

daily['trade_date'] = pd.to_datetime(daily['trade_date'], format='%Y%m%d')
daily.set_index('trade_date', inplace=True)

daily.rename(columns={'vol':'volume'},inplace=True)
# 绘图
#mpf.plot(daily,type='candle')
#mpf.plot(daily, type="candle", title='300669.SZ'+"K线图", ylabel="price($)", style="binance")
mpf.plot(
    data=daily,
    type="candle",
    title="Candlestick for MSFT",
    ylabel="price($)",
    style="binance",
    volume=True,
    ylabel_lower="volume(shares)"
)
