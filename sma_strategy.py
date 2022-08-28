import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import tushare_get_data as tgd



class smastrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.data0.close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.MovingAverageSimple(self.data0, period=15)

    def next(self):
        # print("next")
        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.close()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm
                     )
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm
                     )
                )
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(
            'OPERATION PROFILE, GROSS %.2f, NET %.2f' %
            (trade.pnl, trade.pnlcomm)
        )

    def log(self,txt, dt=None, doprint=True ):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(),txt))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    data = tgd.tushare_data('bt', 'token')
    dataframe = data.get_data_as_pandas('600089.SH', '20180101')

    print(type(dataframe))
    data_tb = bt.feeds.PandasData(dataname=dataframe, fromdate=dt.datetime(2018, 1, 1),
                                  todate=dt.datetime(2022, 8, 28), timeframe=bt.TimeFrame.Days)
    cerebro.adddata(data_tb)

    cerebro.addstrategy(smastrategy)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio,_name= 'SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown,_name='DrawDown')

    cerebro.broker.setcash(200000.0)
    cerebro.broker.setcommission(commission=0.0005)

    cerebro.addsizer(bt.sizers.PercentSizer,percents=50)
    result = cerebro.run()

    print('夏普比率：',result[0].analyzers.SharpeRatio.get_analysis()['sharperatio'])
    print('最大回撤：',result[0].analyzers.DrawDown.get_analysis()['max']['drawdown'])
    cerebro.plot()