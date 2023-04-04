
import pandas as pd
from binance.client import Client

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
    
        
    def get_historical_data(self, timeframe:str='1h', interval:str='2 years ago') -> pd.DataFrame:
        hist_df = self.__set_data_merge(self.__get_multi_data(timeframe,interval))
        hist_df.to_csv('./data/raw/historical_data.csv', index=True)
        return hist_df
        

    def __get_multi_data(self, timeframe, interval) -> list:
        return [self.__get_single_data(symbol, timeframe, interval) for symbol in self.symbols]
    
    
    def __get_single_data(self, symbol, timeframe, interval) -> pd.DataFrame:
        frame = pd.DataFrame(self.client.get_historical_klines(
                            symbol, timeframe, f'{interval} UTC'))
        
        if len(frame) > 0:
            frame = frame.iloc[:,:5]
            frame.columns = ['Time','Open','High','Low','Close']
            frame = frame.set_index('Time')
            frame.index = pd.to_datetime(frame.index, unit='ms')
            frame = frame.astype(float)
            return frame   
             
    
    def __set_data_merge(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.concat(dict(zip(self.symbols,df)), axis=1)