import pandas as pd
import os
path = os.path.dirname(__file__)


class Cleaner():

    def get_cleared_data(self, hist_df: pd.DataFrame) -> pd.DataFrame:
        
        cleared_df = self.__remove_young_currencies(
            self.__set_data_fill(self.__get_data_close(hist_df)))
        
        cleared_df.to_csv(os.path.join(path,'..','data/processing/cleaner_output.csv'))
        return cleared_df

    def __get_data_close(self, df: pd.DataFrame) -> pd.DataFrame:
        closes_df = df.loc[:, df.columns.get_level_values(1).isin(['Close'])]
        closes_df.columns = closes_df.columns.droplevel(1)
        return closes_df

    def __set_data_fill(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.fillna(method='ffill')

    def __remove_young_currencies(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna(how='any', axis=1)
