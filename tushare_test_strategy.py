#******* import package *********
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import tushare as ts
import os

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

#token 认证
ts.set_token('d65a77709e16a01f2ab84cee8040922ad06df5fe4c65993ff3f7d2cf') #18513603069
pro = ts.pro_api()


def test_stragegy(stockpool_list, start_date, b_days, flag):
    #stock_pool = ['600011.SH', '600106.SH', '600458.SH']
    stock_pool = stockpool_list

    # 获取交易所交易日历的list cal_date
    list_calendar = list(pro.trade_cal(exchange='', start_date=start_date)['cal_date'])
    print(list_calendar)

    #start_dt = datetime.date(2021,12,3)  #买入的日期
    start_dt = datetime.datetime.strptime(start_date, "%Y/%m/%d")  # 买入的日期
    end_dt = start_dt + datetime.timedelta(days=b_days)  #卖出的日期 计算这个期间的获利情况

    start_dt = start_dt.strftime("%Y%m%d")
    end_dt = end_dt.strftime("%Y%m%d")
    print('验证的日期期间date: from', start_dt, ' to ', end_dt)

    total = len(stock_pool)  #股票代码个数
    result = pd.DataFrame() #初始化储存结果的Dataframe

    print('开始计算每只股票的模拟买入卖出的获利')

    #开始计算每只股票的模拟买入卖出的获利
    for i in range(total):
        tscode = str(stock_pool[i])  #当前处理的股票代码
        # 打印进度信息
        print('Processing ', 'Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + tscode)

        #因为积分不够，每分钟只能读取500次的限制，所以让程序休眠
        if i > 0 and i%500 == 0:
            time.sleep(60)

        #****** 读取日线数据
        try:
            if flag == 1:
                daily = pro.daily(ts_code=tscode, start_date=start_dt)
            else:
                daily = pro.index_daily(ts_code=tscode, start_date=start_dt)
            #daily = ts.pro_bar(ts_code=tscode, start_date=start_dt, end_date=end_dt)

            # 调整日期顺序（因为取到的数据是逆序排列的，所以需要倒序处理）
            daily.sort_values(by="trade_date",axis=0,ascending=True,inplace=True)
            daily.index = range(len(daily.index))

            #收集买入N天之后的收盘价，以及买入之后的涨幅
            #print(daily)

            buy = daily[daily.trade_date == start_dt][['ts_code','trade_date','close']]

            #如果取到的结果为空，说明该日期不可交易，顺次后移日期
            while buy.empty:
                start_dt = datetime.datetime.strptime(start_dt,'"%Y%m%d"')
                start_dt = start_dt + datetime.timedelta(days=1)
                start_dt = start_dt.strftime("%Y%m%d")
                print('调整买入日期为：',start_dt)
                buy = daily[daily.trade_date == start_dt][['ts_code', 'trade_date', 'close']]

            buy.columns = ['ts_code','trade_date_b','close_b']
            #print('buy', buy)

            sold = daily[daily.trade_date == end_dt][['ts_code','trade_date','close']]
            #如果取到的结果为空，说明该日期不可交易，顺次后移日期
            while sold.empty:
                end_dt = datetime.datetime.strptime(end_dt,"%Y%m%d")
                end_dt = end_dt + datetime.timedelta(days=1)
                end_dt = end_dt.strftime("%Y%m%d")
                print('调整卖出日期为：', end_dt)
                sold = daily[daily.trade_date == end_dt][['ts_code','trade_date','close']]

            sold.columns = ['ts_code','trade_date_s','close_s']
            #print('sold',sold)

            after = pd.merge(buy,sold, how='inner', on='ts_code', left_index=False, right_index=False)

            #合并所有的结果
            result = pd.concat([result,after],ignore_index=True)
            #print('result',result)

            #result['new_close'] = float(daily[daily.trade_date == end_dt]['close'])

            #pd.concat([result, daily[daily.trade_date == start_dt][['ts_code','trade_date','close']]], axis=0)

            #print(result)
            #print(daily)
            #print(daily[['ts_code','close']].tail(1))

        #Exception处理
        except KeyError:
            continue

        finally:
            pass
            #print("done!")

    result['获利'] = (result['close_s'] - result['close_b']) / result['close_b'] * 100
    mean_income = result['获利'].mean(0)
    print('各支股票的获利情况',result.sort_values(by='获利').tail(20))
    print('平均获利: ',mean_income,"%")
