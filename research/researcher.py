import pandas as pd
import research
import os

path = os.path.dirname(__file__)

class Researcher():
    
    def __init__(self) -> None:
        self.hist_df = pd.DataFrame()
        self.cleared_df = pd.DataFrame()
        self.corr_df = pd.DataFrame()
        self.coint_df = pd.DataFrame()
        self.researched_df = pd.DataFrame()
    
    def load_data(self) -> None:
        self.hist_df = pd.read_csv(os.path.join(path,"..", "data/raw/historical_data.csv"), header=[0, 1], index_col=0)
        self.cleared_df = pd.read_csv(os.path.join(path,"..", "data/processing/cleaner_output.csv"),index_col=0)
        self.corr_df = pd.read_csv(os.path.join(path,"..", "data/processing/corr_output.csv"))
        self.coint_df = pd.read_csv(os.path.join(path,"..", "data/processing/coint_output.csv"))
        self.researched_df = pd.read_csv(os.path.join(path,"..", "data/researched/research_output.csv"))

    def update_data(self,timeframe:str,interval:str, min_correlation:float) -> None:
        """
        :param timeframe: e.g. '1d', '4h', '3S', '15m' 
        :type: str
        
        :param interval: e.g. '1 year ago', '10days ago', 'datetime'
        :type: str
        
        :param min_correlation: e.g. '0.83' is 83%
        :type: float
        """
        self.hist_df = research.Loader().get_historical_data(timeframe=timeframe, interval=interval)
        self.cleared_df = research.Cleaner().get_cleared_data(self.hist_df)
        self.corr_df = research.Correlation().get_log_correlation(self.cleared_df, min_correlation=min_correlation)
        self.coint_df = research.Cointegration().get_cointegration(self.corr_df, self.cleared_df)
        self.researched_df = research.Ratio().get_ratio(self.coint_df, self.cleared_df)