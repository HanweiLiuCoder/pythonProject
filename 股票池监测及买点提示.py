#引入:
import matplotlib.pyplot as plt
import datetime
import time
import pandas as pd
import talib as ta
import akshare as ak
from tkinter import messagebox
import re,os
import csv
import codecs

def daily_check(tscode="000001",support=5, pressure=10):  #默认为上证指数
    #获取分时数据
    date_from = '20200101'
    today = datetime.date.today().strftime("%Y%m%d") #获取前3天的分时图

    countin = "1"      #是否检查对象 0 / 1
    trade_signal= "" #买卖信号 4 / 0 / 8
    ma5= ""  #是否跌破5日均线
    ma13= ""  #是否跌破13日均线
    ma144= "" #是否突破144日均线
    ma255= "" #是否突破255日均线
    macd_zero= "" #macd 是否零上 0 / 1
    macd_life= "" #macd是否金叉 0 / 1
    weekly_macd_zero= "" #周线 macd 是否零上 0 / 1
    weekly_macd_value= "" #周线 macd是否金叉 0 / 1
    kdj_value= "" #kdj 值
    kdj_life= "" #kdj是否金叉
    boll_life= "" #布尔值是否上半轴
    rsi_life= "" #rsi值
    support_value= "" #支撑位
    pressure_value= "" #压力位

    # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
    try:
        daily = ak.stock_zh_a_hist(symbol=tscode, start_date=date_from, end_date=today, adjust="")
    except(KeyError):
        return "Exception"
    finally:
        pass

    if daily.empty:
        return
    # 处理字段命名，以符合 Backtrader 的要求
    daily.columns = [
        'datetime',  #这几列名称非常重要 （感觉，不确定）
        'open',
        'close',
        'high',
        'low',
        'volume',
        'amount',
        'vibration',
        'pct_ch',
        'plusminus',
        'turn'
    ]

    #计算MACD
    daily['dif'], daily['dea'], daily['macd'] = ta.MACD(daily.close, fastperiod=12,slowperiod=26, signalperiod=9)
    daily['macd_flg'] = daily['dif'] > daily['dea']

    #计算KDJ
    daily['slowk'], daily['slowd'] = ta.STOCH(
        daily['high'].values,
        daily['low'].values,
        daily['close'].values,
        fastk_period=9,
        slowk_period=3,
        slowk_matype=0,
        slowd_period=3,
        slowd_matype=0)
    daily['slowj'] = list(map(lambda x, y: 3 * x - 2 * y, daily['slowk'], daily['slowd']))

    #计算均线
    daily['ma_5'] = ta.MA(daily['close'], timeperiod=5)
    daily['ma_10'] = ta.MA(daily['close'], timeperiod=10)
    daily['ma_20'] = ta.MA(daily['close'], timeperiod=10)
    daily['ma_144'] = ta.MA(daily['close'], timeperiod=144)
    daily['ma_255'] = ta.MA(daily['close'], timeperiod=255)
    #print(df_tick)


    #RSI    RSI指标
    #强弱指标保持高于50表示为强势市场，反之低于50表示为弱势市场。
    #强弱指标多在70与30之间波动。当六日指标上升到达80时，表示股市已有超买现象，如果一旦继续上升，超过90以上时，则表示已到严重超买的警戒区，股价已形成头部，极可能在短期内反转回转。
    daily["rsi"] = ta.RSI(daily['close'], timeperiod=14)

    #BOLL
    #1、当布林线开口向上后，只要股价K线始终运行在布林线的中轨上方的时候，说明股价一直处在一个中长期上升轨道之中，这是BOLL指标发出的持股待涨信号，如果TRIX指标也是发出持股信号时，这种信号更加准确。此时，投资者应坚决持股待涨。
    #2、当布林线开口向下后，只要股价K线始终运行在布林线的中轨下方的时候，说明股价一直处在一个中长期下降轨道之中，这是BOLL指标发出的持币观望信号，如果TRIX指标也是发出持币信号时，这种信号更加准确。此时，投资者应坚决持币观望。
    daily['upper'], daily['middle'], daily['lower'] = ta.BBANDS(
        daily.close.values,
        timeperiod=20,
        # number of non-biased standard deviations from the mean
        nbdevup=2,
        nbdevdn=2,
        # Moving average type: simple moving average here
        matype=0)

    #print(daily)

    #取得今天的最新数据
    today = daily.tail(1).to_dict(orient="records")[0]
    #print(today['close'])
    comm = ''

    #均线检查
    if today['close'] >= today['ma_5'] :
        juli = round((today['close']-today['ma_5'])/today['ma_5'],1)*100
        ma5 = "5日均线之上 距{}%".format(juli)
        if juli <= 2:
            trade_signal = 'ma5买入信号'
    else:
        ma5 = "0"

    #均线检查
    if today['close'] >= today['ma_10'] :
        juli = round((today['close']-today['ma_10'])/today['ma_10'],1)*100
        ma10 = "10日均线之上 距{}%".format(juli)
        if juli <= 2:
            trade_signal = 'ma10买入信号'
    else:
        ma10 = "0"

    #均线检查
    if today['close'] >= today['ma_20'] :
        juli = round((today['close']-today['ma_20'])/today['ma_20'],1)*100
        ma20 = "20日均线之上 距{}%".format(juli)
        if juli <= 2:
            trade_signal = 'ma20买入信号'
    else:
        ma20 = "0"

    #均线检查
    if today['close'] >= today['ma_144'] :
        juli = round((today['close']-today['ma_144'])/today['ma_144'],1)*100
        ma144 = "144日均线之上 距{}%".format(juli)
        if juli <= 1:
            trade_signal = 'ma144买入信号'
    else:
        ma144 = "0"
        countin = "0"

        #均线检查
    if today['close'] >= today['ma_255'] :
        juli = round((today['close']-today['ma_255'])/today['ma_255'],1)*100
        ma255 = "255日均线之上 距{}%".format(juli)
        if juli <= 1:
            trade_signal = 'ma255买入信号'
    else:
        ma255 = "0"
        countin = "0"

    if today['dif'] > today['dea'] >0:
        macd_zero = '零轴上方'  #零轴之上
        macd_life = '金叉 dif:{} dea:{}  macd:{}'.format(round(today['dif'],2),round(today['dea'],2),round(today['macd'],2)) #macd金叉

    if today['dea'] > today['dif'] > 0:
        macd_zero = '零轴上方'  #零轴之上
        macd_life = '0' #macd死叉

    if 0 > today['dif'] > today['dea']:
        macd_zero = '0'  #零轴之下
        macd_life = '金叉 dif:{} dea:{}  macd:{}'.format(round(today['dif'],2),round(today['dea'],2),round(today['macd'],2)) #macd金叉
        countin = "0"

    if 0 > today['dea'] > today['dif'] :
        macd_zero = '0'  #零轴之下
        macd_life = '0' #macd死叉
        countin = "0"

    if today['slowk'] >= today['slowd']:
        kdj_value = str(round(today['slowk'],2))
        kdj_life = '金叉'
    else:
        kdj_value = str(round(today['slowk'],2))
        kdj_life = '0'

    if today['close'] > today['middle']:
        boll_life = '布尔轴强势区'
    else:
        boll_life = '0'

    if today['rsi'] > 50:
        rsi_life = 'RSI强势区'
    else:
        rsi_life = '0'

    if 0< (today['close']-support)/support < 0.02:
        trade_signal = '接近支撑位 买入信号'

    if 0< (pressure - today['close'])/today['close'] < 0.02:
        trade_signal = '接近压力位 卖出信号'

    a = ','
    check_retuslt = a.join([tscode+'\t',countin,trade_signal,ma5,ma10,ma20,ma144,ma255,macd_zero,macd_life,weekly_macd_zero,weekly_macd_value,kdj_value,kdj_life,boll_life,rsi_life,support_value,pressure_value])
    print(check_retuslt)
    return check_retuslt


if __name__ == '__main__':
    #持仓股票一览
    #cd_pool = ['002480','002482','002869','300952','600168','600502','601811','301011','603390']
    pool_file = 'E:\量化投资\Stocks_Pool\stock_pool.csv'
    pool_file_bak = 'E:\量化投资\Stocks_Pool\stock_pool_bak.csv'

    #cd_pool = open(pool_file, "r",encoding="utf-8")
    ts_data = []
    with open(pool_file,encoding="utf-8-sig") as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        birth_header = next(csv_reader)  # 读取第一行每一列的标题

        for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
            ts_data.append(row)
        #print(ts_data)

    #write headline to bak file:
    headline = ['tscode','countin','trade_signal','ma5','ma10','ma20','ma144','ma255','macd_zero','macd_life','weekly_macd_zero','weekly_macd_value','kdj_value','kdj_life','boll_life','rsi_life','support_value','pressure_value']

    # 此为list数据形式不是numpy数组不能使用np,shape函数,但是我们可以使用np.array函数将list对象转化为numpy数组后使用shape属性进行查看。
    new_file =  open(pool_file_bak, "w", newline='',encoding="utf-8-sig")
    writer = csv.writer(new_file)
    writer.writerow(headline)

    for line in ts_data:
        tscode = line[0][0:6]
        try:
            zhicheng = float(line[15])
            yali = float(line[16])
        except(AttributeError,ValueError,IndexError):
            zhicheng = 0.0001 #避免division by zero
            yali = 0.0001 #避免division by zero
        finally:
            pass

        print('Prcessing ',tscode)
        result = daily_check(tscode,support=zhicheng, pressure=yali)

        #写入文件
        try:
            check_result = result.split(',')
            writer.writerow(check_result)
        except(AttributeError, ValueError, IndexError):
            print("exception happened!")
        finally:
            pass

    new_file.close()

    #os.remove(pool_file)
    #os.rename(pool_file_bak, pool_file)

