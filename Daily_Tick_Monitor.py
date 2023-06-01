#引入:
import matplotlib.pyplot as plt
import datetime
import time
import pandas as pd
import talib as ta
import akshare as ak
from tkinter import messagebox

def tick_check(tscode="000001"):  #默认为上证指数
    #获取分时数据
    today = (datetime.datetime.now()+datetime.timedelta(days=-3)).strftime("%Y-%m-%d %H:%M:%S") #获取前3天的分时图
    df_tick = ak.stock_zh_a_hist_min_em(symbol=tscode, period='1', adjust='', start_date=today)  #分钟数据
    df_tick.columns = ['date', 'open', 'close', 'high', 'low', 'vol', 'amount', 'now']
    df_tick['DIF'], df_tick['DEA'], df_tick['MACD'] = ta.MACD(df_tick.close, fastperiod=12,slowperiod=26, signalperiod=9)
    df_tick['macd_flg'] = df_tick['DIF'] > df_tick['DEA']
    #print(df_tick)

    dif_list = list(df_tick['DIF'])
    dea_list = list(df_tick['DEA'])

    #计算量能的变化
    vol_std = df_tick['vol'].std()
    vol_mean = df_tick['vol'].mean()
    efvar = vol_std / vol_mean
    #量能系数变化剧烈的股票打印出来，进行确认
    if efvar > 1.5:
        #print(tscode, '的量能系数为', efvar, '请关注股价的走势')

        #计算MACD的金叉死叉
        macd_list = list(df_tick['macd_flg'])
        date_list = list(df_tick['date'])
        for i in range(10):  #最近5分钟是否发送MACD的信号变化
            i = len(macd_list)-i-1
            if macd_list[i] != macd_list[i-1] and macd_list[i]==False and dif_list[i]<0 and dea_list[i]<0:
                pass
                #print(tscode, date_list[i], "MACD 水下死叉，卖出！")
            elif macd_list[i] != macd_list[i-1] and macd_list[i]==True and dif_list[i]>0 and dea_list[i]>0:
                print(tscode, date_list[i], "MACD 水上金叉，买入！")

def tick_check2(tscode="000001", p_period='1'):  # 默认为上证指数
    # 获取分时数据
    start_date = (datetime.datetime.now()+datetime.timedelta(days=-7)).strftime("%Y-%m-%d %H:%M:%S") #获取前3天的分时图
    df_tick = ak.stock_zh_a_hist_min_em(symbol=tscode, period=p_period, adjust='',start_date=start_date)  # 30分钟数据
    df_tick.columns = ['date', 'open', 'close', 'high', 'low', 'vol', 'amount', 'now']
    df_tick['DIF'], df_tick['DEA'], df_tick['MACD'] = ta.MACD(df_tick.close, fastperiod=12, slowperiod=26,
                                                              signalperiod=9)
    df_tick['macd_flg'] = df_tick['DIF'] > df_tick['DEA']
    dif_list = list(df_tick['DIF'])
    dea_list = list(df_tick['DEA'])

    # 计算量能的变化
    vol_std = df_tick['vol'].std()
    vol_mean = df_tick['vol'].mean()
    efvar = vol_std / vol_mean
    # 量能系数变化剧烈的股票打印出来，进行确认
    if efvar > 1.5:
        # print(tscode, '的量能系数为', efvar, '请关注股价的走势')

        # 计算MACD的金叉死叉
        macd_list = list(df_tick['macd_flg'])
        date_list = list(df_tick['date'])
        for i in range(10):  # 最近5分钟是否发送MACD的信号变化
            i = len(macd_list) - i - 1
            if macd_list[i] != macd_list[i - 1] and macd_list[i] == False and dif_list[i] < 0 and dea_list[i] < 0:
                pass
                # print(tscode, date_list[i], "MACD 水下死叉，卖出！")
            elif macd_list[i] != macd_list[i - 1] and macd_list[i] == True and dif_list[i] > 0 and dea_list[i] > 0:
                print(tscode, date_list[i], "MACD 水上金叉，买入！")

    #print(df_tick.tail(20))


if __name__ == '__main__':
    cd_list = ['688180', '300856', '300705', '300025', '300355', '430090', '000970', '002556', '000839', '600795', '603327', '002516', '002324', '603001', '002486', '301025', '600101', '600781', '300389', '002540', '600582', '601900', '600655', '300018',
               '003020', '002853', '600671', '600595', '600676', '002066', '600369', '600284', '603685', '002152', '600068',
               '300818', '002773', '831726', '603001', '836826', '601028', '002540', '603328', '430510', '600998', '002204', '688799', '688687', '000510', '000558', '600073', '000061', '601500', '300897', '002956', '002019', '002422', '601933', '002370', '003011', '002985', '688278', '300512', '002736', '601606', '688580', '603298', '600029', '002267', '000670',
               '300144', '688526', '603696', '600346', '600987', '688218', '300697', '600660', '002636', '300032', '688665', '002440', '605108', '603667', '600682', '603716', '002648', '836433']
    try:
        while True:
            print("begin")
            for tscd in cd_list:
                print('check {}...'.format(tscd))
                tick_check(tscode = tscd)
            print("done, sleeping...")
            time.sleep(60)
    except():
        print('Exception happended')
    finally:
        pass
