from sklearn.preprocessing import MinMaxScaler 
import pandas as pd
import backtrader as bt 
import numpy as np
import os

from research import Researcher

path = os.path.dirname(__file__)

class Backtester(bt.Cerebro): 
    
    def __init__(self) -> None:
        super().__init__()
        self.hist_df = pd.DataFrame()
        self.cleared_df = pd.DataFrame()
        self.corr_df = pd.DataFrame()
        self.coint_df = pd.DataFrame()
        self.researched_df = pd.DataFrame()
        self.backtested_df = pd.DataFrame()
        
    def read_data(self, best_coins: Researcher) -> None:
        self.hist_df = best_coins.hist_df
        self.cleared_df = best_coins.cleared_df
        self.corr_df = best_coins.corr_df
        self.coint_df = best_coins.coint_df
        self.researched_df = best_coins.researched_df
        
    def run_backtest(self) -> None:
        
        np.vectorize(lambda  currency1, currenc2, ratio: 
            self.__run_backtest(currency1, currenc2, ratio)
            )(self.researched_df.Currency1, self.researched_df.Currency2, self.researched_df.Ratio)
        
        self.backtested_df.drop_duplicates(inplace=True)
        self.backtested_df.to_csv(os.path.join(path,"..", "data/backtested/backtester_output.csv"))     
        
        
    def __run_backtest(self, currency1, currency2, ratio) -> None:
        df = self.__transform_data(currency1, currency2, ratio)
        output = self.__run_analyzer(df,currency1, currency2)
        returns_df = self.__get_returns(output)
        returns_df['currency1'] = currency1
        returns_df['currency2'] = currency2
        returns_df['ratio'] = ratio
        self.backtested_df = pd.concat([self.backtested_df, returns_df]) 
        # 
        
    def __transform_data(self, currency1, currency2, ratio) -> pd.DataFrame: 
            df = self.hist_df[currency1] - self.hist_df[currency2] * ratio
            
            df[df.columns] = MinMaxScaler().fit_transform(df[df.columns])
            df.index = pd.to_datetime(df.index)
            return df    
        
    def __run_analyzer(self, df,currency1, currency2) -> bt.Cerebro:
        self.strats.clear()
        self.datas.clear()
        feed = bt.feeds.PandasData(dataname=df, name=f'{currency1}/{currency2}')
        self.adddata(feed)
        self.addstrategy(Bbands)
        self.broker.setcommission(commission=0.0008)
        self.broker.set_cash(cash=1000)
        self.addsizer(bt.sizers.FixedSize,stake=1000)
        self.addanalyzer(bt.analyzers.AnnualReturn, _name='areturn')
        self.addanalyzer(bt.analyzers.Returns, _name='returns')
        self.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')
        output = self.run()
        return output
    
    def __get_returns(self, output) -> pd.DataFrame:
        returns = dict()
        trade = output[0].analyzers.trade.get_analysis()

        returns['n_trades'] = trade.total.closed
        returns['won'] = trade.won.total
        returns['win_rate'] = round(trade.won.total / trade.total.closed * 100, 2)
        returns['roi']  = round(output[0].analyzers.returns.get_analysis()['rtot'] * 100, 2)
        returns['sharperatio'] = round(output[0].analyzers.sharpe.get_analysis()['sharperatio'], 2)
        returns['drawdown'] = round(output[0].analyzers.drawdown.get_analysis().drawdown, 2)
        returns_df = pd.DataFrame(returns,index=[0])
        return returns_df
    
    def plot_backtest(self, currency1:str, currency2:str, ratio:float) -> None:
        self.strats.clear()
        self.datas.clear()
        df = self.__transform_data(currency1, currency2, ratio)
        feed = bt.feeds.PandasData(dataname=df, name=f'{currency1}/{currency2}')
        self.adddata(feed)
        self.addstrategy(Bbands)
        self.broker.setcommission(commission=0.0008)
        self.broker.set_cash(cash=1000)
        self.addsizer(bt.sizers.FixedSize,stake=1000)
        self.run()
        # self.plot(volume=False, iplot=False, style='bar', barup='green', bardown='red', width=20, height=10, dpi=300, tight=True, use=None, savefig=os.path.join(path,"..", "data/backtested/backtester_output.png"))
        self.plot(volume=False, iplot=True)


class Bbands(bt.Strategy):

    def __init__(self) -> None:
        self.pos = 0
        self.bbands = bt.indicators.BollingerBands(period=20, devfactor=2)


    def next(self) -> None:
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
