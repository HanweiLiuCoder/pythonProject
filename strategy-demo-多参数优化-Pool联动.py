#成功しました。マルチ　パラメータのオプティマイズ
#addstrategy / optstrategy あと、グローバルのパラメータ定義も重要
#.S. 由于目前版本更新迭代频繁, 请在使用 AKShare 前先升级, 命令如下所示
#pip install akshare --upgrade -i https://pypi.org/simple


from datetime import datetime

import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import pandas as pd
import Strategy_Pool as spl

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置画图时的中文显示
plt.rcParams["axes.unicode_minus"] = False  # 设置画图时的负号显示


def main(code="300052", start_cash=1000000, stake=100, commission_fee=0.001):
    cerebro = bt.Cerebro()  # 创建主控制器
    cerebro.optstrategy(spl.SmaCross,fast_period=range(5,20,5),slow_period=range(10,120,10),printlog=True)  # 导入策略参数寻优

    # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
    stock_hfq_df = ak.stock_zh_a_hist(symbol=code, adjust="hfq", start_date='19910101', end_date='20210617').iloc[:, :6]
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
    start_date = datetime(2013, 1, 1)  # 回测开始时间
    end_date = datetime(2013, 12, 10)  # 回测结束时间
    data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 规范化数据格式
    cerebro.adddata(data)  # 将数据加载至回测系统
    cerebro.broker.setcash(start_cash)  # broker设置资金
    cerebro.broker.setcommission(commission=commission_fee)  # broker手续费
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake)  # 设置买入数量
    #print("期初总资金: %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)  # 用单核 CPU 做优化
    #print("期末总资金: %.2f" % cerebro.broker.getvalue())


if __name__ == '__main__':
    main(code="300015", start_cash=1000000, stake=100, commission_fee=0.001)