# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import pandas as pd
import numpy as np
import datetime
import matplotlib as pl
from jqdatasdk import *

#print('hello world')
auth('18513603098','Cc20051128')

#initialize
today = datetime.date.today()
stocks = list(get_all_securities(['stock']).index)

print(stocks)

for stock_cd in stocks:
    df = get_price(stock_cd, count = 1000, end_date=today, frequency='daily', fields=['open', 'close','low', 'high','volume','pre_close'])
    df['M5'] = df['close'].rolling(5).mean()
    df['M10'] = df['close'].rolling(10).mean()
    df['M20'] = df['close'].rolling(20).mean()
    df['M60'] = df['close'].rolling(60).mean()
    df['M120'] = df['close'].rolling(120).mean()
    df['M250'] = df['close'].rolling(250).mean()
    df['M500'] = df['close'].rolling(500).mean()
   # if df.tail(1).close > df.tail(1).M250:
   #     print("突破250日新高：",stock_cd)
    close_price = float(df.tail(1).close)
    close_m250 = float(df.tail(1).M250)
    if (close_price > close_m250) :
        print("突破250日新高：", stock_cd)
    #print(df.tail(1).close, df.tail(1).M250)
#df.plot()




