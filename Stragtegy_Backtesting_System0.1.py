# http://backtrader.com.cn/docu/#1002 中文版的文档集合
#matplotlib 报错处理的command
#pip uninstall matplotlib
#pip install matplotlib==3.2.2

# 用 AkShare 获取上证指数历史数据
# 上证指数的代码为 sh000001
# import akshare as ak
# stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000001")
# print(stock_zh_index_daily_df)

# 在cmd上使用“pip install talib”命令一般会报错，正确安装方法是，
# 进入https://www.lfd.uci.edu/~gohlke/pythonlibs/，
# 下拉选择TA_Lib-0.4.17-cp37-cp37m-win_amd64.whl

#talib 计算金融数据的技术指标
#SMA
#df['MA5']=ta.SMA(df.close,timeperiod=5)

#BOLL
#H_line,M_line,L_line=ta.BBANDS(df.close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
#df['H_line']=H_line
#df['M_line']=M_line
#df['L_line']=L_line

#MACD
#df['DIF'],df['DEA'],df['MACD'] = ta.MACD(df.close,fastperiod=12, slowperiod=26, signalperiod=9)
#官方默认参数 fastperiod=12, slowperiod=26,signalperiod=9
# MACD柱状图为红，即DIF 与 DEA 均为正值,即都在零轴线以上时，市场趋势属多头市场，若此时DIF 向上继续突破 DEA，即红色柱状越来越长，可作买入信号，该出手就出手。

#KDJ
# dw['slowk'], dw['slowd'] = talib.STOCH(
# 			df['high'].values,
# 			df['low'].values,
# 			df['close'].values,
#                         fastk_period=9,
#                         slowk_period=3,
#                         slowk_matype=0,
#                         slowd_period=3,
#                         slowd_matype=0)

#RSI
#df['RSI']=talib.RSI(df.close, timeperiod=12)     #RSI的天数一般是6、12、24


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime
import backtrader as bt  # 升级到最新版
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import akshare as ak  # 升级到最新版
import pandas as pd
import backtrader.analyzers as btanalyzers
import Strategy_Pool as stp

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


if __name__ == '__main__':
    # 获取    全部上市企业一览
    # ak.stock_info_a_code_name() 所有的交易所
    # stock_info_sh_name_code(indicator)  indicator="主板A股"; choice of {"主板A股", "主板B股", "科创板"}
    # stock_info_sz_name_code(indicator) indicator="A股列表"; choice of {"A股列表", "B股列表", "CDR列表", "AB股列表"}
    # stock_info_bj_name_code()
    #stock_code_list = list(ak.stock_info_sh_name_code(indicator="主板A股"  )['公司代码'])
    #stock_code_list =  ['688656', '002833', '605268', '605099', '603277']
    stock_code_list = ['300056','001216','688308','300572','600248','300284','601390']
    #stock_code_list =  ['002833']
    total = len(stock_code_list)  # 股票代码个数

    #设置策略
    my_strategy = stp.MacdStrategy

    #my_params = {'fast_period': 5, 'slow_period': 20}

    #设置回测起始时间
    start_date = datetime(2020, 1, 1)  # 回测开始时间
    end_date = datetime(2022, 1, 7)  # 回测结束时间

    # ******  循环回测每个股票（同一策略）
    for i in range(len(stock_code_list)):
    # for i in range(1,500):
        tscode = str(stock_code_list[i])  # 当前处理的股票代码

        # 打印进度信息
        print('Processing ','Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + tscode)

        # ****** 读取日线数据
        try:
            #准备数据data
            # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列

            stock_hfq_df = ak.stock_zh_a_hist(symbol=tscode,
                                              start_date=datetime.strftime(start_date,'%Y%m%d'), \
                                             end_date=datetime.strftime(end_date,'%Y%m%d'), \
                                              adjust="qfq").iloc[:, :6]

            if stock_hfq_df.empty:
                continue

            # 处理字段命名，以符合 Backtrader 的要求
            stock_hfq_df.columns = [
                'date',
                'open',
                'close',
                'high',
                'low',
                'volume',
            ]
            # 把 date 作为日期索引，以符合 Backtrader 的要求
            stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])

            print(stock_hfq_df)
            #continue

            #准备回测系统的准备
            cerebro = bt.Cerebro()  # 初始化回测系统

            data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 加载数据
            # ---
            # Resampling and Replaying a data is possible and follows the same pattern:
            # data = bt.BacktraderCSVData(dataname='mypath.min', timeframe=bt.TimeFrame.Minutes)
            # cerebro.resampledata(data, timeframe=bt.TimeFrame.Days)
            # --
            cerebro.adddata(data)  # 将数据传入回测系统

            #添加策略：
            cerebro.addstrategy(my_strategy)  # 将交易策略加载到回测系统中

            #设置profile
            start_cash = 1000000
            cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
            cerebro.broker.setcommission(commission=0.002)  # 设置交易手续费为 0.2%

            # 每次固定交易数量
            cerebro.addsizer(bt.sizers.FixedSize, stake=10000)

            #添加分析器，分析回测的各项指标
            # 添加回撤观察器
            cerebro.addobserver(bt.observers.DrawDown)

            # 添加分析对象
            cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")  # 夏普比例
            # cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name = "AR") #年收益率
            cerebro.addanalyzer(bt.analyzers.DrawDown, _name="DD")  # 最大回撤
            cerebro.addanalyzer(bt.analyzers.Returns, _name="RE")  # 收益
            # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name = "TA") #交易统计

            #开始执行回测
            results = cerebro.run(maxcpus=1)  # 运行回测系统 # 用单核 CPU 做优化
            strat = results[0]

            #计算回测结果
            port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
            pnl = port_value - start_cash  # 盈亏统计

            #输出结果
            print(f"初始资金: {start_cash}\n回测期间： {start_date.strftime('%Y/%m/%d')} : {end_date.strftime('%Y/%m/%d')}")
            print(f"总资金: {round(port_value, 2)}")
            print(f"净收益: {round(pnl, 2)}")

            #打印策略的测试指标
            print("夏普比例:", results[0].analyzers.sharpe.get_analysis()["sharperatio"])
            # print("年化收益率:", results[0].analyzers.AR.get_analysis())
            print("最大回撤:%.2f，最大回撤周期%d" % (results[0].analyzers.DD.get_analysis().max.drawdown, results[0].analyzers.DD.get_analysis().max.len))
            print("总收益率:%.2f" % (results[0].analyzers.RE.get_analysis()["rtot"]))
            # results[0].analyzers.TA.print()

            cerebro.plot(style='candlestick')  # 画图

        #Exception处理
        except (ValueError,KeyError,TypeError,IndexError) :
        #except ():，
            print('Exception happened!')
            continue

        finally:
            #pass
            print("done!")
