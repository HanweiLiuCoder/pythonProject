#引入:
import matplotlib.pyplot as plt
import datetime
import time
import pandas as pd
import talib as ta
import akshare as ak
from tkinter import messagebox
import re,os

def macd_jincha_check(tscode="000001"):  #默认为上证指数
    #获取分时数据
    date_from = '20200101'
    today = datetime.date.today().strftime("%Y%m%d") #获取前3天的分时图

    # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
    daily = ak.stock_zh_a_hist(symbol=tscode, start_date=date_from, end_date=today, adjust="")

    if daily.empty:
        return 'Empty'

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
    daily['ma_13'] = ta.MA(daily['close'], timeperiod=13)
    daily['ma_144'] = ta.MA(daily['close'], timeperiod=144)
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
    comm = tscode + ','

    #均线检查
    if today['close'] > today['ma_5'] and (today['close']-today['ma_5'])/today['ma_5']<0.01 :
        #print('5日均线之上，距离小于1%，关注5日均线支撑')
        comm += '| 5日均线之上，距离小于1%，关注5日均线支撑'

    if today['close'] < today['ma_5'] and today['close'] > today['ma_13']:
        if (today['close']-today['ma_13'])/today['ma_13']<0.01:
            #print('13日均线之上，距离小于1%，关注13日均线支撑')
            comm += '| 13日均线之上，距离小于1%，关注13日均线支撑'
        else:
            #print('跌破5日均线，继续观察')
            comm += '| 跌破5日均线，继续观察'

    if today['close'] < today['ma_144']:
        #print('跌破144均线，暂时移除股票池')
        comm += '| 跌破144均线，暂时移除股票池\n'
        return comm

    if today['dif'] > today['dea'] >0:
        #print('MACD水上金叉，继续持股')
        comm += '| MACD水上金叉，继续持股'

    if today['dea'] > today['dif'] > 0:
        #print('MACD水上死叉，谨慎持股，观察支撑位置是否止跌')
        comm += '| MACD水上死叉，谨慎持股，观察支撑位置是否止跌'

    if today['dea'] < 0:
        #print('MACD跌破水面，卖出为宜')
        comm += '| MACD跌破水面，卖出为宜\n'
        return comm

    if today['slowk'] > today['slowd']:
        #print('KDJ金叉，持股，K值为{}'.format(today['slowk']))
        comm += 'KDJ金叉，持股，K值为{}'.format(today['slowk'])

    if today['close'] > today['upper']:
        #print('股价冲破布尔上沿，强势，观察KDJ的超买情况')
        comm += '股价冲破布尔上沿，强势，观察KDJ的超买情况'

    if today['close'] > today['middle']:
        #print('布尔水上运行，持股')
        comm += '布尔水上运行，持股'

    if today['close'] < today['middle']:
        #print('布尔水下运行，建议卖出')
        comm += '| 布尔水下运行，建议卖出\n'
        return comm

    if today['rsi'] > 50:
        #print('RSI强势区间，持股')
        comm += 'RSI强势区间，持股'
    if today['rsi'] < 50:
        #print('RSI弱势区间，建议卖出')
        comm += '| RSI弱势区间，建议卖出\n'
        return comm

    comm += '\n'
    return  comm

if __name__ == '__main__':
    #持仓股票一览
    #cd_pool = ['002480','002482','002869','300952','600168','600502','601811','301011','603390']
    pool_file = "C:\\Users\liu-hanwei\PycharmProjects\pythonProject2\maup_pool.txt"
    pool_file_bak = 'C:\\Users\liu-hanwei\PycharmProjects\pythonProject2\daup_pool_bak.txt'

    cd_pool = open(pool_file, "r",encoding="utf-8")
    cd_pool_bak = open(pool_file_bak, "a+",encoding="utf-8")
    #pd_show = pd.DataFrame()

    for line in cd_pool:
        line = line.replace('\n','') #去掉换行符号
        tscode = line.split(',', 1)
        print('Processing ',tscode, '  ......')

        try:
            check_result = macd_jincha_check(tscode[0])
            cd_pool_bak.write(check_result)
        except(IndexError,KeyError):
        #except():
            print("exception happended")
        finally:
            print('done.')

    cd_pool.close()
    cd_pool_bak.close()

    os.remove(pool_file)
    os.rename(pool_file_bak, pool_file)

