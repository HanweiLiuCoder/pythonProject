import akshare as ak
import pandas as pd
import talib as ta
import datetime
import os


pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

def dapan(date="20201227", type="1"):
    #根据各种因子的得分对大盘形式进行总的判断
    #SMA5  30/10
    #SMA10  20/10
    #SMA50  10 / -50
    #MACD >0 金叉 30 死叉 10  <0 金叉 10 死叉 -50 顶背离 底背离
    #KDJ 低位金叉+30 高位死叉-30  金叉20 死叉-20
    #BOLL
    #RSI
    score = 0

    today = datetime.date.today().strftime("%Y-%m-%d")
    print(today)

    #日线级别的大盘形式判断
    if type == "1": #日线级别
        #获取大盘日线数据
        df_daily = ak.stock_zh_index_daily(symbol="sh000001", )

        #计算大盘MACD
        df_daily['DIF'],df_daily['DEA'],df_daily['MACD'] = ta.MACD(df_daily.close,fastperiod=12,
                                                                   slowperiod=26, signalperiod=9)

        #计算大盘5日均线，10日均线
        df_daily['MA5']=ta.SMA(df_daily.close,timeperiod=5)
        df_daily['MA10']=ta.SMA(df_daily.close,timeperiod=10)
        df_daily['MA50']=ta.SMA(df_daily.close,timeperiod=50)

        df_daily['slowk'], df_daily['slowd'] = ta.STOCH(\
        			            df_daily.high, \
        			            df_daily.low,  \
        			            df_daily.close,\
                                fastk_period=9,\
                                slowk_period=3,\
                                slowk_matype=0,\
                                slowd_period=3,\
                                slowd_matype=0)
        df_daily['slowj'] = 3 * df_daily['slowk'] - 2 * df_daily['slowd']

        list_today = df_daily.tail(1)
        open_today = float(list_today['open'])
        close_today = float(list_today['close'])
        high_today = float(list_today['high'])
        low_today = float(list_today['low'])
        ma5_today = float(list_today['MA5'])
        ma10_today = float(list_today['MA10'])
        ma50_today = float(list_today['MA50'])
        k_today = float(list_today['slowk'])
        d_today = float(list_today['slowd'])
        j_today = float(list_today['slowj'])
        dif_today = float(list_today['DIF'])
        dea_today = float(list_today['DEA'])
        macd_today = float(list_today['MACD'])

        print(list_today)

        if ma5_today > ma10_today:
            score += 30
            print('5日均线 金叉 10日均线，大胆做多')
        else:
            score -= 20
            print('5日均线 死叉 10日均线，注意控制风险')


        if close_today > ma5_today:
            score += 30
            print('5日均线之上，强势')
        else:
            score += 10
            print('跌破5日均线，市场有分歧')

        if close_today > ma10_today:
            score += 20
            print('10日均线之上，适当减仓')
        else:
            score += 10
            print('跌破10日均线，建议空仓或者观察性参与')

        if close_today > ma50_today:
            score += 10
            print('50日均线之上，长期趋势向好')
        else:
            score -= 50
            print('跌破50日均线，请空仓！')

        if dif_today> 0 and dea_today > 0 and dif_today > dea_today: #水上金叉
            score += 30
            print('MACD水上金叉，满仓操作')
        if dif_today> 0 and dea_today > 0 and dif_today < dea_today: #水上死叉
            score += 15
            print('MACD水上死叉，适当减仓！')
        if dif_today< 0 and dea_today < 0 and dif_today > dea_today: #水下金叉
            score += 5
            print('MACD水下金叉，适量参与')
        if dif_today< 0 and dea_today < 0 and dif_today < dea_today: #水下死叉
            score -= 50
            print('MACD水下死叉，马上空仓')

        #北向资金的监测
        north_net = ak.stock_em_hsgt_north_net_flow_in(indicator="沪股通")
        north_net_yesterday = float(north_net.tail(1)['value'])
        #print(north_net)

        if north_net_yesterday > 0:
            score += 10   #北向资金流入
        else:
            score += -10 #北向资金流出
        print('北向资金监测：{}'.format(north_net_yesterday))

        print('大盘得分为：{}'.format(score))
        #print(list_today.close)

        #北向资金增持的板块 #看了一下实际的数据，感觉意义不大，个人感觉资金流的参考意义极其有限
#        print('-----------------------------------------------------------')
#        north_sec = ak.stock_em_hsgt_board_rank(symbol="北向资金增持行业板块排行", indicator="3日") #"今日", "3日", "5日", "10日", "1月", "1季", "1年"}
#        north_sec = north_sec[['名称','最新涨跌幅','北向资金今日增持估计-股票只数','今日增持最大股-市值','今日增持最大股-占股本比']].sort_values('最新涨跌幅',ascending=False).head(10) #调整显示的信息
#        print(north_sec)

        #板块资金流（东方财富）
        print('------------------------板块资金流向--------------------------')
        mn_sec_industry = ak.stock_sector_fund_flow_rank(indicator='今日',sector_type='行业资金流').head(10)
        mn_sec_industry = mn_sec_industry[['名称','今日涨跌幅','今日主力净流入-净额','今日超大单净流入-净额','今日主力净流入最大股']]
        print('行业板块资金流入监测：\n',mn_sec_industry)

        mn_sec_concept = ak.stock_sector_fund_flow_rank(indicator='今日',sector_type='概念资金流').head(10)
        mn_sec_concept = mn_sec_concept[['名称','今日涨跌幅','今日主力净流入-净额','今日超大单净流入-净额','今日主力净流入最大股']]
        print('概念板块资金流入监测：\n',mn_sec_concept)

        #mn_sec = ak.stock_sector_fund_flow_rank(indicator='今日',sector_type='地域资金流').head(10)
        #mn_sec = mn_sec[['名称','今日涨跌幅','今日主力净流入-净额','今日超大单净流入-净额','今日主力净流入最大股']]
        #print('地域板块资金流入监测：\n',mn_sec)

        #板块资金流（东方财富）
        print('------------------------热点板块监测--------------------------')
        em_conecept = ak.stock_board_concept_name_em().head(10)

        check_flg = input("你是否想查看每个板块的个股表现情况？ 按Y/N：")
        if check_flg in ['Y','y']:
            for sym in em_conecept['板块名称']:
                stocks_sec = ak.stock_board_concept_cons_em(symbol=sym).head(10)
                print(stocks_sec[['代码','名称','最新价','涨跌幅','成交量','振幅','换手率','市盈率-动态']])
                #os.system("pause")

        print('------------------------热点个股监测(30强)--------------------------')
        hot_stocks = ak.stock_wc_hot_rank(date="20211229")[0:30]
        print(hot_stocks)

        print('------------------------涨停监测--------------------------')
        stop_stocks = ak.stock_em_zt_pool(date='20211229').sort_values('首次封板时间')
        print(stop_stocks[['代码', '名称', '最新价', '涨跌幅', '换手率', '首次封板时间', '炸板次数', '涨停统计','连板数','所属行业']])

        print('------------------------炸板股池监测--------------------------')
        stop_stocks = ak.stock_em_zt_pool_zbgc(date='20211229').sort_values('涨跌幅')
        print(stop_stocks[['代码', '名称', '最新价', '涨跌幅', '换手率', '首次封板时间', '炸板次数','振幅','所属行业']])

def bankuai(type=1,bk_name="毛发医疗"):
    #ak.stock_board_concept_name_em 查看东方财富-概念板块的所有概念代码
    if type==1: #概念板块
        bk_df = ak.stock_board_concept_hist_em(symbol=bk_name, adjust="hfq")

    if type==2: #行业板块
        bk_df = ak.stock_board_industry_hist_em(symbol=bk_name, adjust="hfq")

    bk_df.columns=['date','open','close','high','low','pctchg','mchg','volumn','amount','vib','turnover']

    #计算5日均线和10日均线
    #bk_df['MA5'] = ta.SMA(bk_df.close, timeperiod=5)
    #bk_df['MA10'] = ta.SMA(bk_df.close, timeperiod=10)

    #计算30日新高，60日新高， 90日新高， 120日新高
    bk_df['MAX30'] = bk_df.rolling(30, min_periods=1)['close'].max()
    bk_df['MAX60'] = bk_df.rolling(60, min_periods=1)['close'].max()
    bk_df['MAX90'] = bk_df.rolling(90, min_periods=1)['close'].max()
    bk_df['MAX120'] = bk_df.rolling(120, min_periods=1)['close'].max()

    ma30_list = list(bk_df['MAX30'])
    ma60_list = list(bk_df['MAX60'])
    ma90_list = list(bk_df['MAX90'])
    ma120_list = list(bk_df['MAX120'])

    comment = ''  #comment initialization

    try:
        if ma120_list[-1] > ma120_list[-2]:
            comment += ' | 突破120天新高'
        elif ma90_list[-1] > ma90_list[-2]:
            comment += ' | 突破90天新高'
#        elif ma60_list[-1] > ma60_list[-2]:
#            comment += ' | 突破60天新高'
#        elif ma30_list[-1] > ma30_list[-2]:
#            comment += ' | 突破30天新高'
    except ('IndexError'):
        print('Exception happended!')
    finally:
        pass

        #print(bk_df)

    #today = bk_df.tail(1)
    #today_ma5 = float(today['MA5'])
    #today_ma10 = float(today['MA10'])

    #if today_ma5 > today_ma10: #5日均线金叉10日均线
    #    comment += ' | 5日均线金叉10日均线'

    return comment

#----计算MACD数据（日线，周线，月线）
#period='daily'; choice of {'daily', 'weekly', 'monthly'}
#----------------------------
def cal_macd(zhouqi='daily', tscode="000001", start_dt='20000101', end_dt='20220108'):
    # ****** 读取日线数据
        # 取得后复权的历史行情数据 #东方财富接口
        df = ak.stock_zh_a_hist(symbol=tscode, period=zhouqi, start_date=start_dt,
                                   end_date=end_dt, adjust="")

        # Empty Framedata 取得一个空数据列的时候跳过
        if df.empty:
            return df

        df.columns = ['date', 'open', 'close', 'high', 'low', 'vol', 'amount', 'amplitude', 'pct_chg', 'apl_amt',
                         'turnover']
        df = df[['date', 'open', 'close', 'high', 'low', 'vol']]  # 只保留部分需要的数据
        df['date'] = pd.to_datetime(df['date'])  # 设置Datetime
        df.set_index('date', inplace=True)
        # print(df)

        # 如果当天的数据没有，则根据实时数据，追加到数据集里面
        dayOfWeek = datetime.datetime.now().isoweekday()  ###返回数字1-7代表周一到周日
        hours = int(datetime.date.today().strftime('%H'))
        # print('现在是几点？ ', hours)

        # # 周一到周五的15点~24点之间进行数据补足
        # if (dayOfWeek >= 1 and dayOfWeek <= 5) and (
        #         hours > 15 and hours <= 24):  # 15点以后到24点之间需要对当天的数据进行补足，因为0点之后akshare就可以提供当日的历史数据
        #     #print('当天数据缺失，进行补足')
        #     today = ak.stock_zh_a_hist_min_em(symbol=tscode, period='120', adjust='',
        #                                       start_date="2021-12-31 09:30:00",
        #                                       end_date="2022-01-07 15:00:00")
        #     today.columns = ['date', 'open', 'close', 'high', 'low', 'pct', 'pct_m', 'vol', 'amount', 'amplitude',
        #                      'turnover']
        #     today = today[['date', 'open', 'close', 'high', 'low', 'vol']]  # 只留取部分数据
        #     today['date'] = pd.to_datetime(today['date'])  # 设置Datetime
        #     today.set_index('date', inplace=True)
        #     # print(today)
        #
        #     #print(datetime.date.today())
        #     # 分时图转换为日线数据
        #     today = today.resample(rule='1D', base=0, label='left', closed='left').agg(
        #         {
        #             'open': 'first',
        #             'high': 'max',
        #             'low': 'min',
        #             'close': 'last',
        #             'vol': 'sum',
        #         }
        #     )
        #
        #     df = pd.concat([df, today])
            #print(df)

        # 计算MACD


        #df['MA250'] = ta.SMA(df.close, timeperiod=250)
        df['DIF'], df['DEA'], df['MACD'] = ta.MACD(df.close, fastperiod=12,
                                                            slowperiod=26, signalperiod=9)
        df['macd_flg'] = df['DIF'] >= df['DEA']
        df['vol_pct'] = df['vol'] / df['vol'].shift(1)
        df['pct_chg'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)

        return df
        #print(df)

def cal_ma20(tscode="000001", start_dt='20000101', end_dt='20220108'):
    # ****** 读取日线数据
        # 取得后复权的历史行情数据 #东方财富接口
        df = ak.stock_zh_a_hist(symbol=tscode, period="daily", start_date=start_dt,
                                   end_date=end_dt, adjust="")

        # Empty Framedata 取得一个空数据列的时候跳过
        if df.empty:
            return df

        df.columns = ['date', 'open', 'close', 'high', 'low', 'vol', 'amount', 'amplitude', 'pct_chg', 'apl_amt',
                         'turnover']
        df = df[['date', 'open', 'close', 'high', 'low', 'vol','pct_chg',]]  # 只保留部分需要的数据
        df['date'] = pd.to_datetime(df['date'])  # 设置Datetime
        df.set_index('date', inplace=True)

        return df


def breakdays(df):
    print(df)
    days = [20,30,60,90,120,250,360]
    close_today = float(df['close'].tail(1))
    print(close_today)
    df = df.shift(1)
    for rd in days:
        df['max'+str(rd)] = df['close'].rolling(rd).max()

    print(df)

    last_record = df.tail(1)
    if close_today >= float(last_record['max360']):
        return 360
    elif close_today >= float(last_record['max250']):
        return 250
    elif close_today >= float(last_record['max120']):
        return 120
    elif close_today >= float(last_record['max90']):
        return 90
    elif close_today >= float(last_record['max60']):
        return 60
    elif close_today >= float(last_record['max30']):
        return 30
    elif close_today >= float(last_record['max20']):
        return 20
    else:
        return 0

#求收盘价突破了多少天的新高
def breakdays2(df):
    list_close = list(df['close'])

    days = 0
    listlen = len(list_close)
    today = list_close[listlen-1]
    i=1 #counter

    while i <= (listlen-2):
        maxclose  = max(list_close[listlen-2-i:listlen-2])
        if today >= maxclose:
            i = i+1
        else:
            return i

    return i


    days = [20, 30, 60, 90, 120, 250, 360]


if __name__ == '__main__':
    #大盘的系统风险监测
    # dapan()
    #
    # #概念板块
    # for bkname in ak.stock_board_concept_name_em()['板块名称']:
    #      result = bankuai(type=1, bk_name=bkname)
    #      if result: print(bkname, ' : ',result)
    #
    # #行业板块
    # for bkname in ak.stock_board_industry_name_em()['板块名称']:
    #      result = bankuai(type=2, bk_name=bkname)
    #      if result: print(bkname, ' : ',result)

    stock_hfq_df = ak.stock_zh_a_hist(symbol='002835',
                                      start_date='20200101', \
                                      end_date='20220108', \
                                      adjust="qfq").iloc[:, :6]
    # 处理字段命名，以符合 Backtrader 的要求
    stock_hfq_df.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume' ]

    tupo = breakdays2(stock_hfq_df)
    print(tupo)
