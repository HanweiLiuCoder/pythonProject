#******* import package *********
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import akshare as ak
import talib as ta
import os
import functions_pool as fp

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    #为了让pandas打印数据对齐
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)

    #选股记录，写入到文件：
    # filename = "D:\JQ-Data\stockpool" + str(datetime.date.today()) + ".txt"
    # file = open(filename, 'a')  # 以追加写入的方式打开文件
    # file.write('-----------begin--------------\n')

    #test test_strategy program
    #arr= ['600031.SH', '600121.SH', '600189.SH', '600238.SH', '600316.SH', '600381.SH', '600405.SH', '600409.SH', '600456.SH', '600486.SH', '600519.SH', '600586.SH', '600660.SH', '600760.SH', '600763.SH', '600765.SH', '600779.SH', '600792.SH', '600809.SH', '600841.SH', '600862.SH', '600876.SH', '600882.SH', '600885.SH', '600887.SH', '600893.SH', '600960.SH', '600969.SH', '601021.SH', '601100.SH', '601375.SH', '601633.SH', '601877.SH', '601888.SH', '601901.SH', '601908.SH', '601919.SH', '601966.SH', '601995.SH', '603131.SH', '603225.SH', '603259.SH', '603267.SH', '603317.SH', '603678.SH', '603799.SH', '603882.SH', '603899.SH', '603906.SH', '603993.SH', '605179.SH', '605376.SH', '688006.SH', '688036.SH', '688063.SH', '688122.SH', '688179.SH', '688200.SH', '688333.SH', '688559.SH', '000333.SZ', '000521.SZ', '000530.SZ', '000547.SZ', '000568.SZ', '000591.SZ', '000615.SZ', '000626.SZ', '000659.SZ', '000725.SZ', '000733.SZ', '000768.SZ', '000799.SZ', '000821.SZ', '000858.SZ', '000902.SZ', '000927.SZ', '002025.SZ', '002080.SZ', '002114.SZ', '002149.SZ', '002179.SZ', '002192.SZ', '002304.SZ', '002340.SZ', '002389.SZ', '002390.SZ', '002444.SZ', '002493.SZ', '002497.SZ', '002568.SZ', '002594.SZ', '002595.SZ', '002610.SZ', '002643.SZ', '002703.SZ', '002706.SZ', '002756.SZ', '002772.SZ', '002812.SZ', '002821.SZ', '002841.SZ', '003026.SZ', '003028.SZ', '003029.SZ', '300015.SZ', '300059.SZ', '300073.SZ', '300124.SZ', '300196.SZ', '300357.SZ', '300408.SZ', '300454.SZ', '300496.SZ', '300595.SZ', '300616.SZ', '300618.SZ', '300648.SZ', '300712.SZ', '300726.SZ', '300750.SZ', '300759.SZ', '300760.SZ', '300827.SZ', '300896.SZ', '300999.SZ']
    #tushare_test_strategy.test_stragegy(['000300.SH'], '2021/05/06', 30, 0)
    #tushare_test_strategy.test_stragegy(arr, '2021/05/06', 30, 1)
    #exit()

    #主程序开始start main program

    #初始化变量
    arr_macd =[] #macd 金叉 并且macd在0轴之上的附近 #并且5日线金叉10日线， 双倍放量，
    arr_dw_macd =[] #（周线MACD共振的股票重点关注）
    arr_macd_dea =[]  #（DEA突破零轴）
    arr_tupo =[]  #MACD金叉过后，突破大平台
    arr_ma20 = []  # ma20接近，前期有过2次以上的涨停

    #全部上市企业一览
    stock_code_list = list(ak.stock_zh_a_spot_em()['代码'])  #东方财富

    #本地获取股票代码一览
    #stock_code_list = []
    #for cd in open('E:\\量化投资\\Stocks_Pool\\tscodes.txt', 'r'):
    #    stock_code_list.append(cd)

    #stock_code_list = ['600131',]
    total = len(stock_code_list)  #股票代码个数

    #设定平均线的频率
    #ma_list = [5,10,20,30,60,120,250]

    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20220501'
    #time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = datetime.date.today().strftime('%Y%m%d')
    #end_dt_hg = datetime.date.today().strftime('%Y-%m-%d')
    #print(end_dt, end_dt_hg)
    #end_dt = '20210301'
    #print(start_dt,time_temp,end_dt)

    #stock_code_list = ['002376','002696','601326']

    #******  循环获取单个股票的日线行情
    for i in range(len(stock_code_list)):
    #for i in range(3700,4857):
        try:
            tscode = str(stock_code_list[i])  #当前处理的股票代码
            comment = tscode

            # 打印进度信息
            print('Processing ', 'Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + tscode)

            daily = fp.cal_ma20(tscode = tscode, start_dt=start_dt, end_dt=end_dt)



            if daily.empty: continue   #如果取得一个空的数据则继续下一个

             #计算MA20均线价格：
            daily['MA20'] = ta.SMA(daily.close, timeperiod=20)

            today =daily.tail(1)  #当日の状況
            today = today.to_dict('records')[0]
            zhangfu_list = list(daily['pct_chg']) #幅変動のリスト

            #print(daily)
            #print(today)
            #print(zhangfu_list)

            if 0< (today['close'] - today['MA20'])/today['MA20'] <= 0.02 and len(zhangfu_list) >= 20:
                print('ma20 line.......',tscode)
                zhangting_cnt = 0
                for i in range(1,20):
                    if zhangfu_list[0-i] >= 9.5:
                        zhangting_cnt += 1

                if zhangting_cnt >= 2:
                    print("过去20天以内有过{0}次涨停，留意股价的变化".format(zhangting_cnt))
                    arr_ma20.append("{0}:过去20天以内有过{1}次涨停，股价接近20日线，留意股价的变化".format(tscode,zhangting_cnt))

        # Exception处理
        except (ValueError,KeyError,TypeError) :
        #except():
            print('Exception happened')
        finally:
            print('Done!')

    #最后输出结果
    # file.write('\n-----------MACD金叉股票--------------\n')
    # file.write(" | ".join(arr_macd))
    # file.write('\n-----------MACD日线，周线金叉共振股票--------------\n')
    # file.write(" | ".join(arr_dw_macd))
    # file.write('\n-----------DEA突破零轴股票--------------\n')
    # file.write(" | ".join(arr_macd_dea))
    # file.write('\n-----------突破大平台--------------\n')
    # file.write(" | ".join(arr_tupo))

    #
    # file.write('\n-----------done--------------\n')
    # file.close()  # 关闭文件
    # print('MACD金叉股票：', arr_macd)
    # print('DEA突破零轴股票：', arr_macd_dea)
    # print('突破大平台：', arr_tupo)
    print("------------检查结果：-----------")
    for i in arr_ma20:
        print(i)
    # print('MACD 日线 周线共振金叉股票：', arr_dw_macd)
