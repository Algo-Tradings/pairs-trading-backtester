import pandas as pd
import research
import os

class Updater():
    
    def __init__(self) -> None:
        self.hist_df = pd.DataFrame()
        self.useful_df = pd.DataFrame()
        self.corr_df = pd.DataFrame()
        self.coint_df = pd.DataFrame()
        self.final_df = pd.DataFrame()

    def update_all_data(self,timeframe:str ='1d',interval:str ='1 year ago', min_correlation:float=0.83) -> None:
        self.hist_df = research.Loader().get_historical_data(timeframe=timeframe, interval=interval)
        self.useful_df = research.Cleaner().get_useful_data(self.hist_df)
        self.corr_df = research.Correlation().get_log_correlation(self.useful_df, min_correlation=min_correlation)
        self.coint_df = research.Cointegration().get_cointegration(self.corr_df)
        self.final_df = research.Ratio().get_ratio(self.coint_df)
    
    def get_all_data(self, min_correlation:float=0.83):
        path = os.path.dirname(__file__)
        self.hist_df = pd.read_csv(os.path.join(path,"..", "data/raw/historical_data.csv"), header=[0, 1], index_col=0)
        self.useful_df = research.Cleaner().get_useful_data(self.hist_df)
        self.corr_df = research.Correlation().get_log_correlation(self.useful_df, min_correlation=min_correlation)
        self.coint_df = research.Cointegration().get_cointegration(self.corr_df)
        self.final_df = research.Ratio().get_ratio(self.coint_df)
        