import akshare as ak
import numpy as np
import pandas as pd
import datetime
import time


#获取当前日期
end_dt = datetime.date.today().strftime('%Y%m%d')

# 读取Excel文件
excel_file = 'D:\\Investment\\DailyCheck\\stockspool.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(excel_file, dtype={0: str}, sheet_name="pressure")

# 将数据存储为字典
data_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

# 打印字典数据
#print(data_dict)


while True:
    nowtime = datetime.datetime.now()
    nowtime = str(nowtime.hour) + ":" + str(nowtime.minute)
    #print(nowtime)

    #if nowtime in ['10:00','10:30','11:00',"11:30",'13:30','14:00','14:30',"14:45","22:4"]:
    if True:
        # 储存结果
        tupo = []

        #当前涨幅超过5%的股票代码
        # 获取股票数据
        stock_data = ak.stock_zh_a_spot_em()
        # 筛选涨幅超过5%的股票代码
        filtered_stocks = stock_data[stock_data["涨跌幅"] > 5.0]["代码"].unique()

        #实时行情
        realprices = ak.stock_zh_a_spot_em()
        #print(realprices)
        #print(realprices.loc[realprices['代码']=='301337',['最新价','涨跌幅']])

        #循环实时检查股价是否突破压力线
        for code in filtered_stocks:
            try:
                print("checking ", code)
                spotprice = realprices[realprices['代码'] == code]['最新价'].values[0]
                if spotprice >= data_dict[code]:
                    tupo.append(code)
                    print(code,"股价突破压力线")
            except (IndexError, ValueError, KeyError, TypeError):
                print('Exception happened')
            finally:
                print('')


        print("\n----------------------\n")
        #print final result
        for i in tupo:
            print(i, "突破压力线")


    time.sleep(300)