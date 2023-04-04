
import pandas as pd
import numpy as np


class Correlation():
    
    def get_log_correlation(self, df:pd.DataFrame = pd.read_csv('./data/processing/cleaner_output.csv', index_col=0), min_correlation: float = 0.7) -> pd.DataFrame:
        
        corr_df = pd.DataFrame(self.__get_highest_df(self.__get_unstacked_df(self.__get_corr_df(self.__get_log_df(df))), min_correlation)).reset_index()
        corr_df.columns = ['Currency1', 'Currency2', 'Correlation']
        corr_df.to_csv('./data/processing/corr_output.csv', index=False)
        return corr_df
    
    def __get_log_df(self, df:pd.DataFrame) -> pd.DataFrame:
        return np.log(df.pct_change() + 1)

    def __get_corr_df(self, df:pd.DataFrame) -> pd.DataFrame:
        return df.corr()
    
    def __get_unstacked_df(self, df:pd.DataFrame) -> pd.DataFrame:
        return df.unstack().drop_duplicates()

    def __get_highest_df(self, df:pd.DataFrame, min_correlation:float) -> pd.DataFrame:
        return df[(df < 1) & (df >= min_correlation)]