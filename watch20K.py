import akshare as ak
import time
import datetime
import talib as ta
import pandas as pd
from tkinter import messagebox

#today
end_dt = datetime.date.today().strftime('%Y%m%d')

# 读取Excel文件
excel_file = 'D:\\Investment\\DailyCheck\\stockspool.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(excel_file, dtype={0: str}, sheet_name="pool")

tscode_list = list(df["证券代码"])
print(tscode_list)

# 监控程序
while True:
    for tscode in tscode_list:
        #stock_data = ak.stock_zh_a_daily(symbol="600375", start_date="20200101", end_date="20230529", adjust="qfq")
        stock_data = ak.stock_zh_a_hist(symbol=tscode, period="daily", start_date="20200101", end_date=end_dt, adjust="qfq")
        stock_data.columns = ['date', 'open', 'close', 'high', 'low', 'vol', 'amount', 'amplitude', 'pct_chg', 'apl_amt',
                      'turnover']
        stock_data['MA20'] = ta.SMA(stock_data.close, timeperiod=20)
        #print("data:", stock_data)

        # 获取最新的收盘价和20日K线数据
        cnt = len(stock_data['close']) -1
        close_price = stock_data['close'][cnt]
        ma_20 = stock_data['MA20'][cnt]

        #print(close_price, ma_20)

        # 判断股价是否接近20日K线附近
        if 1.02 * ma_20 > close_price > ma_20:  # 假设接近定义为股价低于或等于20日K线的1.01倍
            #messagebox.showwarning(title="消息通知", message="600375" + "股票价格接近20日K线附近！")
            print(tscode + "  | 接近20日K线附近！")

    # 等待1分钟
    time.sleep(60)
    print("---------------------")
