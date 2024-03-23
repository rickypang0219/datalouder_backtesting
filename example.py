from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA
import pandas as pd

# Import the MACD function from TA-Lib or implement manually
try:
    from talib import MACD
except ImportError:
    print("You need to install TA-Lib to use this example.")
    # To install TA-Lib, you might need to install it from a wheel or compile it from source

# Your data should be a pandas DataFrame containing 'Open', 'High', 'Low', 'Close', and 'Volume' columns.
# Here's an example of how you might load it:
# data = pd.read_csv('path_to_your_data.csv', index_col=0, parse_dates=True)

# Define the MACD strategy
class MACDStrategy(Strategy):
    def init(self):
        # Initialize the MACD indicator
        self.macd, self.signal, self.hist = self.I(MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9)

    def next(self):
        # If MACD crosses above the signal line, buy
        if crossover(self.macd, self.signal):
            self.buy()

        # Else, if MACD crosses below the signal line, sell
        elif crossover(self.signal, self.macd):
            self.sell()


# load data
df = pd.read_csv('Clean_HSI.csv')
data = df.iloc[:,:-2]


# Backtest the strategy
backtest = Backtest(data, MACDStrategy, cash=100_000, commission=.002)
stats = backtest.run()
print(stats)

# Optionally plot the trades
backtest.plot()
