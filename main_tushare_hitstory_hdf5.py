# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import pandas as pd
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import datetime
import time
import tushare as ts
import os


pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('本程序会把所有股票的历史数据日线行情保持HDF5文件以备活用')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


#实现RSI的函数
def rsi(array_list, periods=14):
    length = len(array_list)
    rsies = [np.nan] * length
    if length <= periods:
        return rsies
    up_avg = 0
    down_avg = 0

    first_t = array_list[:periods + 1]
    for i in range(1, len(first_t)):
        if first_t[i] >= first_t[i - 1]:
            up_avg += first_t[i] - first_t[i - 1]
        else:
            down_avg += first_t[i - 1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsies[periods] = 100 - 100 / (1 + rs)

    for j in range(periods + 1, length):
        up = 0
        down = 0
        if array_list[j] >= array_list[j - 1]:
            up = array_list[j] - array_list[j - 1]
            down = 0
        else:
            up = 0
            down = array_list[j - 1] - array_list[j]
        up_avg = (up_avg * (periods - 1) + up) / periods
        down_avg = (down_avg * (periods - 1) + down) / periods
        rs = up_avg / down_avg
        rsies[j] = 100 - 100 / (1 + rs)
    return rsies


#token 认证
ts.set_token('d65a77709e16a01f2ab84cee8040922ad06df5fe4c65993ff3f7d2cf') #18513603069
#ts.set_token('147cba1b24d84679e3aa93e922c0a4d0165d04dbc2b7a604b0e76597') #15811006559

pro = ts.pro_api()
arr_60=[]  #突破新高的股票代码池
arr_120=[]
arr_250=[]
arr_500=[]
arr_csy=[] #长上影
arr_cxy=[] #长下影
arr_po_year=[] #破年线


#全部上市企业一览
stock_code_list_sse = pro.stock_basic(exchange='SSE', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
stock_code_list_sze = pro.stock_basic(exchange='SZSE', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
stock_code_list = pd.concat([stock_code_list_sse, stock_code_list_sze], axis=0)

stock_pool = list(stock_code_list['ts_code'])
#测试样本时使用
stock_pool = ['603912.SH','300666.SZ','300618.SZ','002049.SZ','300672.SZ']

ma_list = [5,10,20,30,60,120,250]

# 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
start_dt = '20200101'
time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
end_dt = time_temp.strftime('%Y%m%d')


file_location = r'E:\\量化投资\\History\\'

#print(start_dt,time_temp,end_dt)

# 建立数据库连接,剔除已入库的部分
#db = pymysql.connect(host='127.0.0.1', user='root', passwd='admin', db='stock', charset='utf8')
#cursor = db.cursor()
# 设定需要获取数据的股票池
total = len(stock_pool)
# 循环获取单个股票的日线行情

# # 创建hdf文件
h5_store = pd.HDFStore('E:\\量化投资\\History\\a_stock_100.h5', mode='w')
print(h5_store)
exit()

for i in range(len(stock_pool)):

    #因为积分不够，每分钟只能读取500次的限制，所以让程序休眠
    if i>0 and i%500 == 0:
        time.sleep(60)
    #读取日线数据
    try:
        stock_cd = stock_pool[i]
        daily = pro.daily(ts_code=stock_cd, end_date=end_dt)
        #daily = ts.pro_bar(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)

        # 打印进度
        print('Processing ','Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))

        #实现简单平均线MA10,20,30,60,120,250,
        for ma in ma_list:
            daily['ma_' + str(ma)] = daily['close'].rolling(ma).mean()

        #实现MACD
        data = np.array(daily.close)
        ndata = len(data)
        m, n, T = 12, 26, 9
        EMA1 = np.copy(data)
        EMA2 = np.copy(data)
        f1 = (m - 1) / (m + 1)
        f2 = (n - 1) / (n + 1)
        f3 = (T - 1) / (T + 1)
        for i in range(1, ndata):
            EMA1[i] = EMA1[i - 1] * f1 + EMA1[i] * (1 - f1)
            EMA2[i] = EMA2[i - 1] * f2 + EMA2[i] * (1 - f2)
        daily['ma1'] = EMA1
        daily['ma2'] = EMA2
        DIF = EMA1 - EMA2
        daily['DIF'] = DIF
        DEA = np.copy(DIF)
        for i in range(1, ndata):
            DEA[i] = DEA[i - 1] * f3 + DEA[i] * (1 - f3)
        daily['DEA'] = DEA

        # 实现KDJ
        low_list = daily['low'].rolling(window=9).min()
        low_list.fillna(value=daily['low'].expanding().min(), inplace=True)
        high_list = daily['high'].rolling(window=9).max()
        high_list.fillna(value=daily['high'].expanding().max(), inplace=True)

        rsv = (daily['close'] - low_list) / (high_list - low_list) * 100
        daily['KDJ_K'] = rsv.ewm(com=2).mean()
        daily['KDJ_D'] = daily['KDJ_K'].ewm(com=2).mean()
        daily['KDJ_J'] = 3 * daily['KDJ_K'] - 2 * daily['KDJ_D']

        #实现RSI
        daily['RSI6'] = rsi(daily.close,6)
        daily['RSI13'] = rsi(daily.close,13)
        daily['RSI26'] = rsi(daily.close,26)

        # 如果想调整日期顺序，请执行如下代码
        daily.sort_values(by="trade_date", axis=0, ascending=True, inplace=True)
        daily.index = range(len(daily.index))

        print(daily)

        #显示股票的走势
        daily[['ma_5','ma_10','ma_60']].plot(label='trade_date')
        plt.show()

        #file_name = 'E:\\量化投资\\History\\'+stock_cd + '.hdf5'  #hdf5 file
        file_name = 'E:\\量化投资\\History\\'+stock_cd + '.csv' #csv file
        print(file_name)
        # create a new HDF5 file
        #f = h5.File(file_name,'w')
        #daily.to_hdf(file_name, key='trade_date',mode='w')
        daily.to_csv(file_name,encoding='utf-8-sig')


    finally:
        print("done!")

