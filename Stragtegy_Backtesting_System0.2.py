#matplotlib 报错处理的command
#pip uninstall matplotlib
#pip install matplotlib==3.2.2
# 必须使用如下命令安装pyfolio，这样安装的是最新版：
# pip install git+https://github.com/quantopian/pyfolio
# 不能使用pip install pyfolio来安装。很多人集成不了pyfolio，就是因为安装方式不对。
# self.bar_executed_close
# if len(self) >= (self.bar_executed + 5): 持有时间大于5天则卖出


from datetime import datetime
import backtrader as bt  # 升级到最新版
import backtrader.analyzers as btay
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import akshare as ak  # 升级到最新版
import pandas as pd
import Strategy_Pool
import numpy as np
#import pyfolio as pf

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def Strategy_back_test(tscode='000001'):
    #准备数据data
    # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
    stock_hfq_df = ak.stock_zh_a_hist(symbol=tscode, adjust="").iloc[:, :9]
    # 处理字段命名，以符合 Backtrader 的要求
    stock_hfq_df.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume','amount','updown_pct','openinterest'
    ]
    # 把 date 作为日期索引，以符合 Backtrader 的要求
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])

    #准备回测系统的准备
    cerebro = bt.Cerebro()  # 初始化回测系统

    start_date = datetime(2021, 10, 1)  # 回测开始时间
    end_date = datetime.today()  # 回测结束时间

    #print(stock_hfq_df)

    data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 加载数据
    #data = Strategy_Pool.MyPandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)
    # ---
    # Resampling and Replaying a data is possible and follows the same pattern:
    # data = bt.BacktraderCSVData(dataname='mypath.min', timeframe=bt.TimeFrame.Minutes)
    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Days)
    # --
    cerebro.adddata(data)  # 将数据传入回测系统

    #添加策略：
    #cerebro.addstrategy(Strategy_Pool.SmaCross)  # 将交易策略加载到回测系统中
    cerebro.addstrategy(Strategy_Pool.TwoStopStrategy)  # 将交易策略加载到回测系统中
    # ----
    # When optimizing the parameters have to be added as iterables. See the Optimization section for a detailed explanation. The basic pattern:
    # cerebro.optstrategy(MyStrategy, myparam1=range(10, 20))
    # Which will run MyStrategy 10 times with myparam1 taking values from 10 to 19 (remember ranges in Python are half-open and 20 will not be reached)
    # ----

    start_cash = 1000000
    cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
    cerebro.broker.setcommission(commission=0.002)  # 设置交易手续费为 0.2%

    # 每次固定交易数量
    cerebro.addsizer(bt.sizers.FixedSize, stake=50000)

    # 添加回撤观察器
    cerebro.addobserver(bt.observers.DrawDown)

    # 添加分析对象
    cerebro.addanalyzer(btay.SharpeRatio, _name = "sharpe")  #夏普比例
    #cerebro.addanalyzer(btay.AnnualReturn, _name = "AR") #年收益率
    cerebro.addanalyzer(btay.DrawDown, _name = "DD") #最大回撤
    cerebro.addanalyzer(btay.Returns, _name = "RE") #收益
    #cerebro.addanalyzer(btay.TradeAnalyzer, _name = "TA") #交易统计

    # 添加Pyfolio分析对象
    #cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

    results = cerebro.run()  # 运行回测系统

    #Pyfolio 分析表格生成
    #pyfoliozer = results[0].analyzers.getbyname('pyfolio')
    #returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    #pf.create_full_tear_sheet(returns[0])
    #pf.create_full_tear_sheet( \
    #     returns,\
    #     positions=positions,\
    #     transactions=transactions,\
    #     gross_lev=gross_lev,\
    #     live_start_date=start_date  # This date is sample specific
    #     round_trips=True
    #)

    port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
    pnl = port_value - start_cash  # 盈亏统计

    test_result = "净收益: {} 年間収益率：{}".format(pnl, results[0].analyzers.AR.get_analysis())
    print(test_result)

    #print(f"初始资金: {start_cash}\n回测期间： {start_date.strftime('%Y/%m/%d')} : {end_date.strftime('%Y/%m/%d')}")
    #print(f"总资金: {round(port_value, 2)}")
    print(f"净收益: {round(pnl, 2)}")

    # print("夏普比例:", results[0].analyzers.sharpe.get_analysis()["sharperatio"])
    # #print("年化收益率:", results[0].analyzers.AR.get_analysis())
    # print("最大回撤:%.2f，最大回撤周期%d" % (results[0].analyzers.DD.get_analysis().max.drawdown, results[0].analyzers.DD.get_analysis().max.len))
    # print("总收益率:%.2f" % (results[0].analyzers.RE.get_analysis()["rtot"]))
    # #results[0].analyzers.TA.print()

    #cerebro.plot(style='candlestick')  # 画图

if __name__ == '__main__':
    # 全部上市企业一览
    stock_code_list = list(ak.stock_zh_a_spot_em()['代码'])
    #stock_code_list = ['600804','300001']
    total = len(stock_code_list)  # 股票代码个数

    # ******  循环获取单个股票的日线行情
    for i in range(total):
    #for i in range(1, 2000):
        print('Processing {}...'.format(stock_code_list[i]))
        try:
            Strategy_back_test(stock_code_list[i])
        except(IndexError):
            print("Exceptions happened!")
        finally:
            continue
