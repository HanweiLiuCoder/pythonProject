import backtrader as bt
import numpy as np
import pandas as pd

# 策略类的母类，主要是把一些策略类的共同处理集中起来编写，封装
class BtStrategy(bt.Strategy):
    """
    主策略程序
    """

    def log(self, txt, dt=None, do_print=True):
        """
        Logging function fot this strategy
        """
        if do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_trade(self, trade):
        """
        记录交易收益情况
        """
        self.bar_executed = len(self)

        if not trade.isclosed:
            return
        self.log(f"策略收益：毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}")

    # 记录交易执行情况（可省略，默认不输出结果）
    def notify_order(self, order):
        # 如果order为submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            # print('order.Submitted, order.Accepted')
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入-->  价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'卖出-->  价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}')
            self.bar_executed = len(self)
        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None

    def stop(self):
        self.log("最大回撤:-%.2f%%" % self.stats.drawdown.maxdrawdown[-1], do_print=True)
        # self.log("夏普比例:", self.results[0].analyzers.sharpe.get_analysis(), do_print=True)


# """
# 单均线策略，站上均线买入，跌破均线卖出
# 这个策略的关键点是找到上升趋势的股票，做波段
# """
class TestStragtegy(BtStrategy):
    """
    主策略程序
    """
    params = (("maperiod", 30),)  # 全局设定交易策略的参数

    def __init__(self):
        """
        初始化函数
        """
        self.data_close = self.datas[0].close  # 指定价格序列
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        # 添加移动均线指标
        self.wma = bt.indicators.SMA(self.datas[0])

    def next(self):
        """
        执行逻辑
        """
        if self.order:  # 检查是否有指令等待执行,
            return

        # 检查是否持仓
        if not self.position:  # 没有持仓
            if self.data_close[0] > self.wma[0]:  # 执行买入条件判断：收盘价格上涨突破20日均线
                self.order = self.buy(size=100)  # 执行买入
                # print('买入股票下单成功')
        else:
            if self.data_close[0] < self.wma[0]:  # 执行卖出条件判断：收盘价格跌破20日均线
                self.order = self.sell(size=100)  # 执行卖出
                # print('卖出股票下单成功')


# """
# 突破N日新高
# 这个策略的关键点是找到上升趋势的股票，做波段
# """
class BreakNDays(BtStrategy):
    """
    主策略程序
    """
    params = (("maperiod", 120),)  # 全局设定交易策略的参数

    def __init__(self):
        """
        初始化函数
        """
        self.data_close = self.datas[0].close  # 指定价格序列
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        # 添加移动均线指标
        self.hst = bt.indicators.Highest(self.datas[0], period=self.params.maperiod)
        self.ma5 = bt.indicators.SimpleMovingAverage(self.datas[0], period=5)
        # self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)

    def next(self):
        """
        执行逻辑
        """
        if self.order:  # 检查是否有指令等待执行,
            return

        # 检查是否持仓
        # if not self.position:  # 没有持仓
        if True:  # 没有持仓
            if self.data_close[0] >= self.hst[-1]:  # 执行买入条件判断：收盘价格上涨突破20日均线
                self.order = self.buy(size=5000)  # 执行买入
                print('剩余现金：', self.broker.get_cash())
                # print('买入股票下单成功')
        else:
            if self.data_close[0] < self.ma5[0]:  # 执行卖出条件判断：收盘价格跌破20日均线
                self.order = self.sell(size=100)  # 执行卖出
                # print('卖出股票下单成功')


# """
# 单均线策略，站上均线买入，跌破均线卖出
# 这个策略的关键点是找到上升趋势的股票，做波段
# """
class SingleMA(BtStrategy):
    """
    主策略程序
    """
    params = (("maperiod", 20),)  # 全局设定交易策略的参数

    def __init__(self):
        """
        初始化函数
        """
        self.data_close = self.datas[0].close  # 指定价格序列
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        # 添加移动均线指标
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)

    def next(self):
        """
        执行逻辑
        """
        if self.order:  # 检查是否有指令等待执行,
            return

        # 检查是否持仓
        if not self.position:  # 没有持仓
            if self.data_close[0] > self.sma[0]:  # 执行买入条件判断：收盘价格上涨突破20日均线
                self.order = self.buy()  # 执行买入
                # print('买入股票下单成功')
        else:
            if self.data_close[0] < self.sma[0]:  # 执行卖出条件判断：收盘价格跌破20日均线
                self.order = self.sell()  # 执行卖出
                # print('卖出股票下单成功')


# 创建双均线策略类
class SmaCross(BtStrategy):
    # 定义参数
    params = dict(
        fast_period=5,  # 快速移动平均期数
        slow_period=10)  # 慢速移动平均期数

    def __init__(self):
        # 定义快速移动平均线指标
        fastMA = bt.ind.MovingAverageSimple(period=self.params.fast_period)

        # 定义慢速移动平均线指标
        slowMA = bt.ind.MovingAverageSimple(period=self.params.slow_period)

        # 定义移动均线交叉信号指标
        self.crossover = bt.ind.CrossOver(fastMA, slowMA)
        self.order = None  # 设置订单引用，用于取消以往发出的尚未执行的订单

    def next(self):  # 每个新bar结束时触发调用一次，相当于其他框架的 on_bar()方法
        self.cancel(self.order)  # 取消以往未执行订单

        if not self.position:  # 还没有仓位，才可以买
            if self.crossover > 0:  # 金叉
                self.order = self.buy(size=100)  # 创建市价买单，该单会在次日开盘以开盘价成交
        # 已有仓位，才可以卖
        elif self.crossover < 0:  # 死叉
            self.order = self.sell(size=100)  # 创建市价卖单，该单会在次日开盘以开盘价成交

    def stop(self):
        """
        回测结束后输出结果
        """
        self.log("(长期MA均线： %2d日) (短期MA均线： %2d日) 期末总资金 %.2f" % (
        self.params.fast_period, self.params.slow_period, self.broker.getvalue()), do_print=True)



class MacdStrategy(BtStrategy):
    '''#平滑异同移动平均线MACD
        DIF(蓝线): 计算12天平均和26天平均的差，公式：EMA(C,12)-EMA(c,26)
        Signal(DEM或DEA或MACD) (红线): 计算macd9天均值，公式：Signal(DEM或DEA或MACD)：EMA(MACD,9)
        Histogram (柱): 计算macd与signal的差值，公式：Histogram：MACD-Signal
        period_me1=12
        period_me2=26
        period_signal=9
        macd = ema(data, me1_period) - ema(data, me2_period)
        signal = ema(macd, signal_period)
        histo = macd - signal

        macd, macdsignal, macdhist = talib.MACD(data.收盘.values)
        三个默认参数分别为短周期，长周期和信号的周期。
        返回值分别为macd值，macd信号值(macd的移动均线值)和离差图。
    '''

    def __init__(self):
        # sma源码位于indicators\macd.py
        # 指标必须要定义在策略类中的初始化函数中
        macd = bt.ind.MACD()
        self.macd = macd.macd
        self.signal = macd.signal
        self.histo = bt.ind.MACDHisto()
        self.macd_goldsignal = bt.ind.CrossUp(self.macd, self.signal)

        self.ma5 = bt.ind.SimpleMovingAverage(self.datas[0], period=5)
        self.ma13 = bt.ind.SimpleMovingAverage(self.datas[0], period=13)
        self.ma144 = bt.ind.SimpleMovingAverage(self.datas[0], period=144)

        self.dataclose = self.datas[0].close

        print(self.lines)

        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_cashvalue(self, cash, value):
        self.log('Cash %s Value %s' % (cash, value), do_print=True)

    def next(self):

        if self.order:  # 检查是否有指令等待执行,
            return

        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0], do_print=True)
        # Check if we are in the market
        if not self.getposition(self.datas[0]):

            # self.data.close是表示收盘价
            # 收盘价大于histo，买入
            # if self.macd > 0 and self.signal > 0 and self.histo > 0:
            if self.ma5 > self.ma13 > self.ma144:  # 5,13,144顺上
                if self.macd_goldsignal and self.macd > 0 and self.signal > 0 and self.dataclose > self.ma144 \
                        and self.macd[0] < 1.0:
                    self.log(
                        'BUY:  macd: {}, signal: {}, histo: {}'.format(self.macd[0], self.signal[0], self.histo[0]),
                        do_print=True)
                    self.log('BUY CREATE(MACD 金叉),{}'.format(self.dataclose[0]))
                    self.order = self.buy(self.datas[0])

                # DEA突破零轴买入
                if self.macd >= self.signal and self.signal[0] >= 0 and self.signal[
                    -1] < 0 and self.dataclose > self.ma144 \
                        and self.macd[0] < 1.0:
                    self.log(
                        'BUY:  macd: {}, signal: {}, histo: {}'.format(self.macd[0], self.signal[0], self.histo[0]),
                        do_print=True)
                    self.log('BUY CREATE(DEA 突破零轴),{}'.format(self.dataclose[0]))
                    self.order = self.buy(self.datas[0])

        else:

            # 收盘价小于等于histo，卖出
            if self.dataclose < self.ma13:
                self.log('SELL:  macd: {}, signal: {}, ma13: {}'.format(self.macd[0], self.signal[0], self.ma13[0]),
                         do_print=True)
                self.log('BUY CREATE,{}'.format(self.dataclose[0]))
                self.log('Pos size %s' % self.position.size)
                self.order = self.sell(self.datas[0])


class ssa_index_ind(bt.Indicator):
    lines = ('ssa',)

    def __init__(self, ssa_window):
        self.params.ssa_window = ssa_window
        # 这个很有用，会有 not maturity生成
        self.addminperiod(self.params.ssa_window * 2)

    def get_window_matrix(self, input_array, t, m):
        # 将时间序列变成矩阵
        temp = []
        n = t - m + 1
        for i in range(n):
            temp.append(input_array[i:i + m])
        window_matrix = np.array(temp)
        return window_matrix

    def svd_reduce(self, window_matrix):
        # svd分解
        u, s, v = np.linalg.svd(window_matrix)
        m1, n1 = u.shape
        m2, n2 = v.shape
        index = s.argmax()  # get the biggest index
        u1 = u[:, index]
        v1 = v[index]
        u1 = u1.reshape((m1, 1))
        v1 = v1.reshape((1, n2))
        value = s.max()
        new_matrix = value * (np.dot(u1, v1))
        return new_matrix

    def recreate_array(self, new_matrix, t, m):
        # 时间序列重构
        ret = []
        n = t - m + 1
        for p in range(1, t + 1):
            if p < m:
                alpha = p
            elif p > t - m + 1:
                alpha = t - p + 1
            else:
                alpha = m
            sigma = 0
            for j in range(1, m + 1):
                i = p - j + 1
                if i > 0 and i < n + 1:
                    sigma += new_matrix[i - 1][j - 1]
            ret.append(sigma / alpha)
        return ret

    def SSA(self, input_array, t, m):
        window_matrix = self.get_window_matrix(input_array, t, m)
        new_matrix = self.svd_reduce(window_matrix)
        new_array = self.recreate_array(new_matrix, t, m)
        return new_array

    def next(self):
        data_serial = self.data.get(size=self.params.ssa_window * 2)
        self.lines.ssa[0] = self.SSA(data_serial, len(data_serial), int(len(data_serial) / 2))[-1]


# Create a Stratey
class MySSA_Strategy(bt.Strategy):
    params = (
        ('ssa_window', 15),
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.ssa = ssa_index_ind(ssa_window=self.params.ssa_window, subplot=False)
        # bt.indicator.LinePlotterIndicator(self.ssa, name='ssa')
        self.sma = bt.indicators.SimpleMovingAverage(period=self.params.maperiod)

    def start(self):
        print("the world call me!")

    def prenext(self):
        print("not mature 尚未成熟")

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.ssa[0]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.ssa[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def stop(self):
        print("death")

# 创建双均线策略类
class TwoStopStrategy(BtStrategy):
    # 定义参数
    params = dict(
        fast_period=5,  # 快速移动平均期数
        slow_period=10)  # 慢速移动平均期数

    def __init__(self):
        #Lines初期化
        self.data_close = self.datas[0].close  # 指定价格序列
        self.pctchg = self.datas[0].openinterest  # 指定价格序列
        self.ma10 = bt.ind.MovingAverageSimple(period=5)
        self.ma20 = bt.ind.MovingAverageSimple(period=20)
        self.order = None  # 设置订单引用，用于取消以往发出的尚未执行的订单

    def next(self):  # 每个新bar结束时触发调用一次，相当于其他框架的 on_bar()方法
        self.cancel(self.order)  # 取消以往未执行订单

        if not self.position:  # 还没有仓位，才可以买
            juli = round((self.data_close - self.ma20) / self.ma20,3)
            exist_zhangting = (self.pctchg[-1] >= 9.95 or
                               self.pctchg[-2] >= 9.95 or
                               self.pctchg[-3] >= 9.95 or
                               self.pctchg[-4] >= 9.95 or
                               self.pctchg[-5] >= 9.95 or
                               self.pctchg[-6] >= 9.95 or
                               self.pctchg[-7] >= 9.95 or
                               self.pctchg[-8] >= 9.95 or
                               self.pctchg[-9] >= 9.95 )
            #print('date:{} close:{} ma13:{} juli:{} pct_chg:{} '.format(self.datas[0].datetime.date(0), self.data_close[0], self.ma13[0],juli,
            #                                                            self.pctchg[0]))
            if 0<juli<=0.025 and exist_zhangting:  # 金叉
                self.order = self.buy(size=100)  # 创建市价买单，该单会在次日开盘以开盘价成交
        # 已有仓位，才可以卖
        elif (self.data_close < self.ma10 and len(self) >= (self.bar_executed + 3)) or self.data_close < self.ma20:  # 死叉
            self.order = self.sell(size=100)  # 创建市价卖单，该单会在次日开盘以开盘价成交

    def stop(self):
        """
        回测结束后输出结果
        """
        #self.log("(长期MA均线： %2d日) (短期MA均线： %2d日) 期末总资金 %.2f" % (
        #self.params.fast_period, self.params.slow_period, self.broker.getvalue()), do_print=True)

