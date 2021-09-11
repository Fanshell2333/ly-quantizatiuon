from datetime import datetime

import matplotlib.pyplot as plt
import backtrader as bt
import pandas as pd
import akshare as ak

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

class BollStrategy(bt.Strategy):

    params = (("maperiod", 20),)

    def __init__(self):
        self.data_close = self.datas[0].close

        self.order = None
        self.buy_price = None
        self.buy_comm = None

        self.boll_top = bt.indicators.BollingerBands(self.datas[0], period=26).top
        self.boll_bot = bt.indicators.BollingerBands(self.datas[0], period=26).bot


    def next(self):
        if self.order:
            return

        if not self.position:
            if self.data_close <= self.boll_bot:
                self.order = self.buy(size=1800)
        else:
            if self.data_close >= self.boll_top:
                self.order = self.sell(size=1800)

cerebro = bt.Cerebro()
start_date = datetime(2015, 7, 23)
end_date = datetime(2020, 7, 23)

data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)
cerebro.adddata(data)
cerebro.addstrategy(BollStrategy)

start_cash = 200000

cerebro.broker.set_cash(start_cash)
cerebro.broker.setcommission(commission=0.00025)
cerebro.run()

print( cerebro.broker.getvalue())






