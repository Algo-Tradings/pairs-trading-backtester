import pandas as pd
from backtesting import Updater
from sklearn.preprocessing import MinMaxScaler 
import backtrader as bt 
import os

class Results():
    
    def get_and_save_results(self, currency1, currency2, ratio):
        
        df = self.__transform_data(currency1, currency2, ratio)

        returns = Cerebro().analyse_returns(Cerebro().run_cerebro(df))
        path = os.path.dirname(__file__)
        returns.to_csv(os.path.join(path, '..', f'data/backtested/{currency1.lower()}-{currency2.lower()}.csv'), index=False)
        
        
    def __transform_data(self, currency1, currency2, ratio):
            all_data = Updater()
            all_data.get_all_data(min_correlation=0.83)
            df = all_data.hist_df[currency1] - all_data.hist_df[currency2] * ratio
            df[df.columns] = MinMaxScaler().fit_transform(df[df.columns])
            df.index = pd.to_datetime(df.index)
            return df
        
class Cerebro():
    
    def run_cerebro(self, df):
        feed = bt.feeds.PandasData(dataname=df, name='df1')
        cerebro = bt.Cerebro()
        cerebro.adddata(feed)
        cerebro.addstrategy(Bband)
        cerebro.broker.setcommission(commission=0.0008)
        # cerebro.broker.setcommission(margin=True, commission=0.0008, leverage=20)
        cerebro.broker.set_cash(cash=1000)
        # cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
        cerebro.addsizer(bt.sizers.FixedSize,stake=1000)
        cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='areturn')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')
        
        return cerebro.run()

    def analyse_returns(self, output):
        returns = dict()
        trade = output[0].analyzers.trade.get_analysis()
        returns['n_trades'] = trade.total.closed
        returns['won'] = trade.won.total
        returns['hit_rate'] = round(trade.won.total / trade.total.closed * 100, 2)
        returns['return']  = round(output[0].analyzers.returns.get_analysis()['rtot'] * 100, 2)
        returns['sharperatio'] = round(output[0].analyzers.sharpe.get_analysis()['sharperatio'], 2)
        returns['drawdown'] = round(output[0].analyzers.drawdown.get_analysis().drawdown, 2)
        returns_df = pd.DataFrame(returns,index=[0])
        return returns_df
         
class Bband(bt.Strategy):

    def __init__(self):
        self.pos = 0
        self.bbands = bt.indicators.BollingerBands(period=20, devfactor=2)


    def next(self):
        values = (self.data.high, self.data.low,
                self.data.close, self.data.open)
        
        max_value = max(*values)
        min_value = min(*values)

        if not self.pos and min_value < self.bbands.bot:
            self.pos = 1
            self.buy() 

        elif self.pos == 1 and max_value > self.bbands.mid:
            self.pos = 0
            self.close() 

        if not self.pos and max_value > self.bbands.top:
            self.pos = -1
            self.sell() 

        elif self.pos == -1 and min_value < self.bbands.mid:
            self.pos = 0
            self.close() 
