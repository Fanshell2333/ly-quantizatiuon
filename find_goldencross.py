from datetime import datetime

import backtrader as bt
import pandas as pd
import akshare as ak


class FindGoldenCross(bt.Strategy):
    params = (
        ("maperiod1", 5),
        ("maperiod2", 13),
        ("maperiod3", 21),
        ("maperiod4", 34),
        ("maperiod5", 55),
        ("printlog", True),
        ("poneplot", False),
        ("pstake", 100000)
    )

    def log(self, txt, dt=None, doprint=False):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s,%s' % (dt.isoformat(), txt))

    def __init__(self):
        self.inds = dict()

        for i, d in enumerate(self.datas):
            #a = bt.indicators.SimpleMovingAverage(d.close, period=self.params.maperiod1)
            self.inds[d]['ma1'] = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod1)
            self.inds[d]['ma2'] = bt.indicators.SimpleMovingAverage(d, period=self.params.maperiod2)
            self.inds[d]['ma3'] = bt.indicators.SimpleMovingAverage(d, period=self.params.maperiod3)
            self.inds[d]['ma4'] = bt.indicators.SimpleMovingAverage(d, period=self.params.maperiod4)
            self.inds[d]['ma5'] = bt.indicators.SimpleMovingAverage(d, period=self.params.maperiod5)
            self.inds[d]['D1'] = bt.ind.CrossOver(self.inds[d]['ma5'], self.inds[d]['ma4'])
            # 交叉信号
            self.inds[d]['A1'] = bt.ind.CrossOver(self.inds[d]['ma1'], self.inds[d]['ma2'])
            # 交叉信号
            self.inds[d]['C1'] = bt.ind.CrossOver(self.inds[d]['ma2'], self.inds[d]['ma3'])

        print(self.datas[0])

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, CROSS %.2F, NET %2F' % (trade.pnl, trade.pnlcomm))

    def prenext(self):
        self.next()

    def next(self):
        date = self.datas[0].datetime.date(0)
        # 日期
        value = self.broker.getvalue()
        # 当天的value

        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size

            sig1 = ((self.inds[d]['D1'][-1]>0)
                    and (self.inds[d]['A1'][0]>0)) \
                    and (self.inds[d]['ma2'][0] >self.inds[d]['ma4'][0])\
                    and (self.inds[d]['ma4'][0] >self.inds[d]['ma4'][-1])

            sig2 = ((self.inds[d]['D1'][-1]>0) or (self.inds[d]['A1'][0]>0 ))\
                    and(self.inds[d]['ma2'][0] >self.inds[d]['ma2'][-1])\
                    and(d.close[0]/d.open[0]>1.05)\
                    and(d.volume[0] /d.volume[-1]>2)

            sig3 = ((self.inds[d]['D1'][-1]>0) or (self.inds[d]['A1'][0]>0 ))\
                    and(self.inds[d]['ma2'][0] >self.inds[d]['ma3'][0] )\
                    and(self.inds[d]['ma3'][0] >self.inds[d]['ma4'][0] )\
                    and(self.inds[d]['ma4'][0] >self.inds[d]['ma4'][-1] )

            sig4 = self.inds[d]['C1'][0]<0

            if not pos:
                if sig1 or sig2 and sig3: #金叉
                    self.log('%s, Goldencross appeared, %.2f ,%s' % (dt, d.close[0] ,d._name))

                elif sig4:
                    #self.close(data = d)
                    self.log('%s, Deadcross appeard, %.2f,%s' % (dt, d.close[0] ,d._name))


# 印花税
class stampDutyCommissionScheme(bt.CommInfoBase):
    params = (
        ('stamp_duty', 0.005),  # 印花税率
        ('percabs', True),
    )
    def _gotcommission(self, size, price, pseudoexec):
        if size > 0:  # 买入，不考虑印花税
            return size * price * self.p.commission
        elif size < 0:  # 卖出，考虑印花税
            return -size * price * (self.p.stamp_duty + self.p.commission)
        else:
            return 0

# 隆基
stock_hfq_df = ak.stock_zh_a_hist(symbol="601012", adjust='hfq').iloc[:, :6]
stock_hfq_df.columns = [
    'date',
    'open',
    "close",
    "high",
    'low',
    'volume'
]

stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])

cerebro = bt.Cerebro()
start_date = datetime(2020, 4, 23)
end_date = datetime(2020, 7, 23)

data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)
cerebro.adddata(data)
cerebro.addstrategy(FindGoldenCross)

start_cash = 200000

cerebro.broker.set_cash(start_cash)
cerebro.broker.setcommission(commission=0.00025)
cerebro.run()

print( cerebro.broker.getvalue())







