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
    filename = "D:\\投资\\Data" + str(datetime.date.today()) + ".txt"
    file = open(filename, 'a')  # 以追加写入的方式打开文件
    file.write('-----------begin--------------\n')

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
    arr_tupo250 =[]  #MACD金叉过后，突破大平台

    #全部上市企业一览
    stock_code_list = list(ak.stock_zh_a_spot_em()['代码'])  #东方财富

    #本地获取股票代码一览
    #stock_code_list = ['300020']
    #for cd in open('E:\\量化投资\\Stocks_Pool\\tscodes.txt', 'r'):
    #    stock_code_list.append(cd)

    #stock_code_list = ['600131',]
    total = len(stock_code_list)  #股票代码个数

    #设定平均线的频率
    #ma_list = [5,10,20,30,60,120,250]

    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20200101'
    #time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = datetime.date.today().strftime('%Y%m%d')
    #end_dt_hg = datetime.date.today().strftime('%Y-%m-%d')
    #print(end_dt, end_dt_hg)
    #end_dt = '20210301'
    #print(start_dt,time_temp,end_dt)


    #******  循环获取单个股票的日线行情
    for i in range(len(stock_code_list)):
    #for i in range(3700,4857):
        try:
            tscode = str(stock_code_list[i])  #当前处理的股票代码
            comment = tscode

            # 打印进度信息
            print('Processing ', 'Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + tscode)

            daily = fp.cal_macd(zhouqi='daily', tscode = tscode, start_dt=start_dt, end_dt=end_dt)
            if daily.empty: continue   #如果取得一个空的数据则继续下一个

            weekly = fp.cal_macd(zhouqi='weekly', tscode = tscode, start_dt=start_dt, end_dt=end_dt)
            if weekly.empty: continue  #如果取得一个空的数据则继续下一个

            #计算MA144均线价格：
            daily['MA144'] = ta.SMA(daily.close, timeperiod=144)
            daily['MA250'] = ta.SMA(daily.close, timeperiod=250)

            #print(daily,weekly)

            #检查日线MACD的金叉以及量比变化情况
            close_list = list(daily['macd_flg'])
            ma250_list = list(daily['MA250'])
            daily_macd_list = list(daily['macd_flg'])
            dea_list = list(daily['DEA'])
            vol_list = list(daily['vol'])
            m = len(daily_macd_list)-1
            vol_pct = round(float(daily.tail(1)['vol_pct']),1)
            today_pct = float(daily.tail(1)['pct_chg'])
            #print(today_pct)
            #print(daily_macd_list[m-1],daily_macd_list[m])

            #股价没有站上144日均线，直接排除
            #if float(daily['close'].tail(1)) < float(daily['MA144'].tail(1)):
            #    continue
            #print(daily)

            #上市低于10天排除
            #if m < 10:
            #    continue

            tupodays = fp.breakdays2(daily)  #突破了多少天
            if tupodays > 155: #155天新高的股票才有意义去看期间是否有放量
                vol_times = round(max(vol_list[m-tupodays:m-1]) / np.mean(vol_list[m-tupodays:m-1]),1) #前期放量的倍数
            else:
                vol_times = 0

            if today_pct > 0.05 and daily_macd_list[m]==True and daily_macd_list[m-1]==False and float(daily.tail(1)['DEA']) >=-0.3:
                difdea = "DIF:" + str(round(float(daily['DIF'].tail(1)),2)) + "  DEA:" + str(round(float(daily['DEA'].tail(1)),2))
                comment += ' | 日线MACD金叉 '
                comment += difdea
                if vol_pct >= 2.0:
                    comment += ' | 放量{}倍'.format(vol_pct)

                if tupodays > 120:
                    comment += ' | 破{}天新高'.format(tupodays)

                if vol_times >= 2.0:  #期间的量能有过超越均值两倍说明有过放量
                    comment += ' | 期间有过{}倍以上的放量现象\n'.format(vol_times)
                else:
                    comment += '\n'

                file.write(comment)  # 写入内容
                arr_macd.append(tscode)

                #只有在日线MACD金叉的前提下去确认周线MACD的共振情况
                # 检查周线MACD的金叉以及量比变化情况
                weekly_macd_list = list(weekly['macd_flg'])
                m = len(weekly_macd_list) - 1
                #vol_pct = float(weekly.tail(1)['vol_pct'])
                #print(vol_pct)
                #print(weekly_macd_list[m - 1], weekly_macd_list[m])
                # if weekly_macd_list[m] == True and weekly_macd_list[m - 1] == False:
                #     comment += '------| 周线线MACD金叉 | '
                #     difdea = "DIF:" + str(round(float(weekly['DIF'].tail(1)),2)) + "  DEA:" + str(round(float(weekly['DEA'].tail(1)),2))+'\n'
                #     comment += difdea
                #     file.write(comment)  # 写入内容
                #     arr_dw_macd.append(tscode)
            elif tupodays > 300 and vol_times >= 2.0 :
                comment += ' 股价突破{}天新高 而且期间放量{}倍\n'.format(tupodays, vol_times)
                file.write(comment)  # 写入内容
                arr_tupo.append(tscode)

            #DEA突破零轴 而且周线MACD金叉
            #if daily_macd_list[m]==True and dea_list[m]>=0 and dea_list[m-1]<0 and weekly_macd_list[m] == True and weekly_macd_list[m - 1] == False:
            #    comment += ' | DEA 突破零轴\n'
                #tupodays = fp.breakdays2(daily)
                #comment += ' | 突破{}天新高\n'.format(tupodays)  #刚刚突破水上，创新高的概率不高
            #    file.write(comment)  # 写入内容
            #    arr_macd_dea.append(tscode)

            #突破年线的股票重点关注
            if m>10 and close_list[-2] < ma250_list[-2] and close_list[-1] >= ma250_list[-1]:
                comment += ' | 突破年线\n'
                arr_tupo250.append(tscode)

            #打印MACD金叉信息
            if comment != tscode:
                print(comment)

        # Exception处理
        except (IndexError,ValueError,KeyError,TypeError) :
        #except():
            print('Exception happened')
        finally:
            print('Done!')

    #最后输出结果
    file.write('\n-----------MACD金叉股票--------------\n')
    file.write(" | ".join(arr_macd))
    file.write('\n-----------MACD日线，周线金叉共振股票--------------\n')
    file.write(" | ".join(arr_dw_macd))
    file.write('\n-----------DEA突破零轴股票--------------\n')
    file.write(" | ".join(arr_macd_dea))
    file.write('\n-----------突破大平台--------------\n')
    file.write(" | ".join(arr_tupo))
    file.write('\n-----------突破年线--------------\n')
    file.write(" | ".join(arr_tupo250))

    file.write('\n-----------done--------------\n')
    file.close()  # 关闭文件
    print('MACD金叉股票：', arr_macd)
    print('DEA突破零轴股票：', arr_macd_dea)
    print('突破大平台：', arr_tupo)
    print('突破年线：', arr_tupo250)
    print('MACD 日线 周线共振金叉股票：', arr_dw_macd)
