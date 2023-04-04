import pandas as pd


class Cleaner():

    def get_useful_data(self, df: pd.DataFrame = pd.read_csv('./data/raw/historical_data.csv', header=[0, 1], index_col=0)) -> pd.DataFrame:
        
        useful_df = self.__remove_young_currencies(
            self.__set_data_fill(self.__get_data_close(df)))
        
        useful_df.to_csv('./data/processing/cleaner_output.csv')
        return useful_df

    def __get_data_close(self, df: pd.DataFrame) -> pd.DataFrame:
        closes_df = df.loc[:, df.columns.get_level_values(1).isin(['Close'])]
        closes_df.columns = closes_df.columns.droplevel(1)
        return closes_df

    def __set_data_fill(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.fillna(method='ffill')

    def __remove_young_currencies(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna(how='any', axis=1)
