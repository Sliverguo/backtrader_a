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

        self.sma = bt.indicators.MovingAverageSimple(self.data0, period=20)

    def next(self):
        # print(type(self.position))
        print(self.position)
        if not self.position:
            print('not positon')
            if self.dataclose[0] > self.sma[0]:
                self.buy()
        else:
            print('positon is ok')
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

    def log(self,txt, dt=None, doprint=False):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(),txt))


class get_best_parameter:
    def __init__(self,dataframe,strategy):
        self.result = []
        self.cerebro = bt.Cerebro()
        # feed pandas data
        self.data_stock =bt.feeds.PandasData(dataname=dataframe, fromdate=dt.datetime(2018, 1, 1),
                                  todate=dt.datetime(2022, 8, 29), timeframe=bt.TimeFrame.Days)
        # add stock data into the cerebro
        self.cerebro.adddata(self.data_stock)
        # add strategy into the cerebro
        self.cerebro.addstrategy(strategy)
        # add analyzer into the cerebro
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
        self.cerebro.addanalyzer(bt.analyzers.PositionsValue, _name='PositionsValue')

    def set_cash_comm(self,cash,comm):
        self.cerebro.broker.setcash(cash)
        self.cerebro.broker.setcommission(commission=comm)

    def get_best_resut(self):
        big_value = 0.0
        best_size = 1
        for size in range(1,100):
            self.cerebro.addsizer(bt.sizers.PercentSizer, percents=size)
            result = self.cerebro.run()
            self.result.append(result)
            value_dict = result[0].analyzers.PositionsValue.get_analysis()
            last_day_value = value_dict[(list(value_dict.keys())[-1])]
            if(np.float_(last_day_value) > big_value):
                big_value = np.float_(last_day_value)
                best_size = size
            # print('夏普比率：', result[0].analyzers.SharpeRatio.get_analysis()['sharperatio'])
            # print('最大回撤：', result[0].analyzers.DrawDown.get_analysis()['max']['drawdown'])
            # print('最终净值：', result[0].analyzers.PositionsValue.get_analysis()[dt.date(2022, 8, 29)])

        print("最优的购买仓位比:%d" % best_size+"的最大净值是%f元" % big_value)
        return self.result

    def show(self):
        self.cerebro.plot()


if __name__ == '__main__':
    data = tgd.tushare_data('bt', 'token')
    dataframe = data.get_data_as_pandas('600089.SH', '20180101')
    gbp = get_best_parameter(dataframe,smastrategy)
    gbp.set_cash_comm(200000,0.0005)
    gbp.get_best_resut()
    gbp.show()


'''
    # dataframe = data.get_data_as_pandas('300223.SZ', '20180101')

    print(type(dataframe))
    data_tb = bt.feeds.PandasData(dataname=dataframe, fromdate=dt.datetime(2022, 1, 1),
                                  todate=dt.datetime(2022, 8, 29), timeframe=bt.TimeFrame.Days)
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
'''