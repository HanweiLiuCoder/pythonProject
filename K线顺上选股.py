import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import akshare as ak
import talib as ta
import os

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

def cal_ma(daily):
    # 实现简单平均线MA5,10,20,30,60,120,250,
    # 设定平均线的频率
    ma_list = [5, 10, 20, 60, 120, 250]

    for ma in ma_list:
        daily['ma' + str(ma)] = daily['close'].rolling(ma).mean()

    # 实现量能的平均线V5，10,20
    for ma in ma_list[0:2]:
        daily['vol' + str(ma)] = daily['vol'].rolling(ma).mean()

    # 计算MACD
    daily['dif'], daily['dea'], daily['macd'] = ta.MACD(daily.close, fastperiod=12, slowperiod=26, signalperiod=9)

    # NaN数据填充为0
    daily.fillna(0, inplace=True)  # 填充Nan数据为0

    return daily

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('K线顺上选股开始...')

    #全部上市企业一览
    stock_code_list = list(ak.stock_zh_a_spot_em()['代码'])
    #stock_code_list = ['003031']
    total = len(stock_code_list)  #股票代码个数

    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20000101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    #end_dt = time_temp.strftime('%Y%m%d')
    end_dt = datetime.date.today().strftime("%Y%m%d")
    #print(start_dt,time_temp,end_dt)

    arr_list_day = []
    arr_list_week = []

    #******  循环获取单个股票的日线行情
    for i in range(len(stock_code_list)):
    #for i in range(100):
        tscode = str(stock_code_list[i])  #当前处理的股票代码

        #****** 读取日线数据
        try:
            # 打印进度信息
            print('Processing ','Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + tscode)


            #取得后复权的历史行情数据(日线级别处理)
            daily = ak.stock_zh_a_hist(symbol=tscode, period="daily", start_date=start_dt,
                                                    end_date=end_dt, adjust="hfq").iloc[:,0:6]
            daily.columns = ['date','open','close','high','low','vol']
            #Empty Framedata 取得一个空数据列的时候跳过
            if not daily.empty:
                daily = cal_ma(daily)
            else:
                continue
            #显示处理完毕的股票信息
            #print('daily data:\n', daily)

            #取得后复权的历史行情数据(日线级别处理)
            weekly = ak.stock_zh_a_hist(symbol=tscode, period="weekly", start_date=start_dt,
                                                    end_date=end_dt, adjust="hfq").iloc[:,0:6]
            weekly.columns = ['date','open','close','high','low','vol']
            #Empty Framedata 取得一个空数据列的时候跳过
            if not weekly.empty:
                weekly = cal_ma(weekly)
            else:
                continue
            #显示处理完毕的股票信息
            #print('weekly data:\n', weekly)

            today = list(daily.tail(1).to_dict(orient='index').values())[0]
            thisweek = list(weekly.tail(1).to_dict(orient='index').values())[0]
            #print(today)
            #print(thisweek)

            if today['ma5'] > today['ma10'] > today['ma20'] > today['ma60'] > today['ma120']> today['ma250'] and \
                today['vol5'] > today['vol10'] and \
                today['dif'] > today['dea'] >=0 :
                    print('日K线顺上' + '日量能均线金叉' + '日MACD水上金叉')
                    arr_list_day.append(tscode)

            if thisweek['ma5'] > thisweek['ma10'] > thisweek['ma20'] and \
                thisweek['vol5'] > thisweek['vol10'] and\
                thisweek['dif'] > thisweek['dea'] >=0:
                    print('周K线顺上'+'周量能均线金叉'+'周MACD水上金叉')
                    arr_list_week.append(tscode)

            #处理轴线级别的数据

        #Exception处理
        except(ValueError,KeyError,TypeError) :
        #except():
            print('Exception happened!')
            continue

        finally:
            #pass
            print("done!")

    print('日线K线顺上股票：',arr_list_day)
    print('周线K线顺上股票：',arr_list_week)
    print('日线周线共振：',list(set(arr_list_day).intersection(set(arr_list_week))))