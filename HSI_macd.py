from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import pandas as pd


# load the pandas dataframe
df =  pd.read_csv('Clean_HSI.csv')

HSI = df.iloc[:,:-2]

# set up strategy
class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


# Backtest here
bt = Backtest(HSI, SmaCross,
              cash=100000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
bt.plot()
