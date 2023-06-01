#******* import package *********
import pandas as pd
import numpy as np
import datetime
import time
import os
import akshare as ak

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


#全部上市企业一览
#stock_code_list = list(ak.stock_zh_a_spot_em()['代码'])
stock_code_list = ['002825','002542','000002','000007','002232']
total = len(stock_code_list)  #股票代码个数

# 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
start_dt = '20210507'
time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
end_dt = time_temp.strftime('%Y%m%d')


#******  循环获取单个股票的日线行情
for i in range(len(stock_code_list)):
#for i in range(1,500):
    tscode = str(stock_code_list[i])  #当前处理的股票代码

    #因为积分不够，每分钟只能读取500次的限制，所以让程序休眠
    #if i > 0 and i%500 == 0:
    #    time.sleep(60)

    #****** 读取日线数据
    try:
        # 打印进度信息
        print('Processing ','Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + tscode)

        daily = ak.stock_zh_a_hist(symbol=tscode, period="daily", start_date=start_dt, \
                                                end_date=end_dt, adjust="qfq")
        #print(daily)

        #Empty Framedata 取得一个空数据列的时候跳过
        if daily.empty:
            print('empty!')
            continue

        #计算量能的离散系数  经过测试，一般离散系数大于1.2的属于波动比较剧烈
        vol_std = daily['成交量'].std()
        vol_mean = daily['成交量'].mean()
        efvar = vol_std/vol_mean
        print(tscode, '的量能系数为',efvar)
    #Exception处理
    #except (TimeoutError,ValueError,KeyError,TypeError) :
    except ():
        continue

    finally:
        #pass
        print("done!")

