#引入:
import matplotlib.pyplot as plt
import datetime
import time
import easyquotation
import pandas as pd

#选择 源头
quotation = easyquotation.use('tencent')  # ['jsl'] # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

#持仓股票一览
cd_list = ['300640','600883','000001']
pd_show = pd.DataFrame()

while True:
    for cd in cd_list:
        #单只股票 实时行情
        sdata = quotation.real(cd)  # 支持直接指定前缀，如 'sh000001'
        df = pd.DataFrame(data = sdata)
        pd_show = pd.concat([pd_show, df], axis=1, join='outer')
        #print('-------------------------------------------')

    print('现在时刻', datetime.datetime.now())
    print(pd_show.loc[['name', 'now', '涨跌(%)', '量比', 'high', 'low']])
    pd_show = pd.DataFrame() #再次初始化结果集

    time.sleep(60)

#打印合集

