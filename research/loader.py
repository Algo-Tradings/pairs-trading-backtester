
import pandas as pd
from binance.client import Client
import os
import datetime

import ccxt


path = os.path.dirname(__file__)
class Loader():
    
    def __init__(self) -> None:
        self.client = Client()
        self.symbols = self.__get_symbols()
    
        
    def __get_symbols(self,) -> list:
        info = self.client.get_exchange_info()
        unused_coins = ['UPUSDT','DOWNUSDT','BEAR','BULL','USDC','PAX','TUSD','BUSD','USDP']
        
        return [s['symbol'] for s in info['symbols'] if s['symbol'].endswith('USDT') and 
                                                            s['status'] == 'TRADING' and 
                                                            all(coin not in s['symbol'] for coin in unused_coins)]
    
        
    def get_historical_data(self, timeframe:str, interval:str , end_date:str = None) -> pd.DataFrame:
        """
        :param timeframe: e.g. '1d', '4h', '3S', '15m' 
        :type: str
        
        :param interval: e.g. '1 year ago', '10days ago', 'datetime'
        :type: str
        """
        hist_df = self.__set_data_merge(self.__get_multi_data(timeframe,interval, end_date))
        hist_df.to_csv(os.path.join(path,'..', 'data/raw/historical_data.csv'), index=True)
        return hist_df
        

    def __get_multi_data(self, timeframe, interval, end_date) -> list:
        return [self.__get_single_data(symbol, timeframe, interval, end_date) for symbol in self.symbols]
    
    
    def __get_single_data(self, symbol, timeframe, interval, end_date) -> pd.DataFrame:
        frame = pd.DataFrame(self.client.get_historical_klines(
                            symbol, timeframe, interval, end_date))
        
        if len(frame) > 0:
            frame = frame.iloc[:,:5]
            frame.columns = ['Time','Open','High','Low','Close']
            frame = frame.set_index('Time')
            frame.index = pd.to_datetime(frame.index, unit='ms')
            frame = frame.astype(float)
            return frame   
             
    
    def __set_data_merge(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.concat(dict(zip(self.symbols,df)), axis=1)