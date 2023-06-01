#******* import package *********
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import os
import akshare as ak

#pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

#test test_strategy program
#arr= ['600031.SH', '600121.SH', '600189.SH', '600238.SH', '600316.SH', '600381.SH', '600405.SH', '600409.SH', '600456.SH', '600486.SH', '600519.SH', '600586.SH', '600660.SH', '600760.SH', '600763.SH', '600765.SH', '600779.SH', '600792.SH', '600809.SH', '600841.SH', '600862.SH', '600876.SH', '600882.SH', '600885.SH', '600887.SH', '600893.SH', '600960.SH', '600969.SH', '601021.SH', '601100.SH', '601375.SH', '601633.SH', '601877.SH', '601888.SH', '601901.SH', '601908.SH', '601919.SH', '601966.SH', '601995.SH', '603131.SH', '603225.SH', '603259.SH', '603267.SH', '603317.SH', '603678.SH', '603799.SH', '603882.SH', '603899.SH', '603906.SH', '603993.SH', '605179.SH', '605376.SH', '688006.SH', '688036.SH', '688063.SH', '688122.SH', '688179.SH', '688200.SH', '688333.SH', '688559.SH', '000333.SZ', '000521.SZ', '000530.SZ', '000547.SZ', '000568.SZ', '000591.SZ', '000615.SZ', '000626.SZ', '000659.SZ', '000725.SZ', '000733.SZ', '000768.SZ', '000799.SZ', '000821.SZ', '000858.SZ', '000902.SZ', '000927.SZ', '002025.SZ', '002080.SZ', '002114.SZ', '002149.SZ', '002179.SZ', '002192.SZ', '002304.SZ', '002340.SZ', '002389.SZ', '002390.SZ', '002444.SZ', '002493.SZ', '002497.SZ', '002568.SZ', '002594.SZ', '002595.SZ', '002610.SZ', '002643.SZ', '002703.SZ', '002706.SZ', '002756.SZ', '002772.SZ', '002812.SZ', '002821.SZ', '002841.SZ', '003026.SZ', '003028.SZ', '003029.SZ', '300015.SZ', '300059.SZ', '300073.SZ', '300124.SZ', '300196.SZ', '300357.SZ', '300408.SZ', '300454.SZ', '300496.SZ', '300595.SZ', '300616.SZ', '300618.SZ', '300648.SZ', '300712.SZ', '300726.SZ', '300750.SZ', '300759.SZ', '300760.SZ', '300827.SZ', '300896.SZ', '300999.SZ']
#tushare_test_strategy.test_stragegy(['000300.SH'], '2021/05/06', 30, 0)
#tushare_test_strategy.test_stragegy(arr, '2021/05/06', 30, 1)
#exit()

#主程序开始start main program

#token 认证
#ts.set_token('d65a77709e16a01f2ab84cee8040922ad06df5fe4c65993ff3f7d2cf') #18513603069
#ts.set_token('147cba1b24d84679e3aa93e922c0a4d0165d04dbc2b7a604b0e76597') #15811006559
#pro = ts.pro_api()


#初始化变量
arr_2lines =[] #macd 金叉 并且macd在0轴之上的附近 #并且5日线金叉10日线


#全部上市企业一览
stock_code_list = list(ak.stock_zh_a_spot_em()['代码'])
#stock_code_list = ['603912.SH','688265','688265','002049','300672']
total = len(stock_code_list)  #股票代码个数

#测试样本时使用
#stock_pool = ['603912.SH','300666.SZ','300618.SZ','002049.SZ','300672.SZ']

#设定平均线的频率
ma_list = [20,80]

# 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
start_dt = '20190101'
time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
end_dt = time_temp.strftime('%Y%m%d')
#end_dt = '2021/05/06'
#print(start_dt,time_temp,end_dt)

#获取交易所交易日历的list cal_date
#list_calendar = list(pro.trade_cal(exchange='', start_date=start_dt, end_date=end_dt)['cal_date'])
#print(list_calendar)

#exit()

#******  建立数据库连接,剔除已入库的部分
#db = pymysql.connect(host='127.0.0.1', user='root', passwd='admin', db='stock', charset='utf8')
#cursor = db.cursor()
# 设定需要获取数据的股票池



#****** 北上资金的走势
#print('北上资金的走势')
#ns_money = pro.moneyflow_hsgt(start_date='20210101', end_date=end_dt).head(20)
#ns_money.set_index('trade_date', inplace=True)
#print(ns_money)
#ns_money['north_money'].plot()
#plt.show()
#print(bs_money)

#******  循环获取单个股票的日线行情
#for i in range(len(stock_code_list)):
for i in range(1,500):
    tscode = str(stock_code_list[i])  #当前处理的股票代码

    #因为积分不够，每分钟只能读取500次的限制，所以让程序休眠
    #if i > 0 and i%500 == 0:
    #    time.sleep(60)

    #****** 读取日线数据
    try:
        # 打印进度信息
        print('Processing ','Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + tscode)

        daily = ak.stock_zh_a_hist(symbol=tscode, period="daily", start_date=start_dt,
                                                end_date=end_dt, adjust="qfq")

        #Empty Framedata 取得一个空数据列的时候跳过
        if daily.empty:
            continue

        #实现简单平均线MA5,10,20,30,60,120,250,
        for ma in ma_list:
            daily['ma_' + str(ma)] = daily['收盘'].rolling(ma).mean()

        #NaN数据填充为0
        daily.fillna(0, inplace=True) #填充Nan数据为0

        #显示处理完毕的股票信息
        #print(daily)

        #20line金叉80line
        m20 = float(daily.tail(1)['ma_20'])
        m80 = float(daily.tail(1)['ma_80'])
        ym20 = float(daily.shift(1).tail(1)['ma_20'])
        ym80 = float(daily.shift(1).tail(1)['ma_80'])
        #print(m20,m80,ym20,ym80)

        if (m20 > m80) and (ym20 <= ym80) : #五线向上的股票需要认真审阅，有宝
            arr_2lines.append(tscode)

    #Exception处理
    except (TimeoutError,ValueError,KeyError,TypeError) :
        continue

    finally:
        #pass
        print("done!")

#打印结果
print('20line金叉80line的股票：', arr_2lines)


#test stragety
# print('计算比较标的的获利情况： ')
# tushare_test_strategy.test_stragegy(['000300.SH'], end_dt,30, 0)
#
# print('计算突破2年新高的获利情况： ')
# if arr_500:
#     tushare_test_strategy.test_stragegy(arr_500, end_dt,30, 1)
#
# print('计算突破1年新高的获利情况： ')
# if arr_250:
#     tushare_test_strategy.test_stragegy(arr_250, end_dt,30, 1)
