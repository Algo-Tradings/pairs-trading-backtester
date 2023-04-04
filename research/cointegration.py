
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts


class Cointegration():

    def get_cointegration(self, corr: pd.DataFrame = pd.read_csv('./data/processing/corr_output.csv'),
                          useful_df: pd.DataFrame = pd.read_csv('./data/processing/cleaner_output.csv')
                          )-> pd.DataFrame:

        ts_coint = self.__get_ts_coint(corr, useful_df)
        ts_coint.to_csv('./data/processing/coint_output.csv', index=False)
        return ts_coint

    def __get_ts_coint(self, corr: pd.DataFrame, useful_df: pd.DataFrame) -> pd.DataFrame:
        coint_series = corr.apply(lambda corr_row: ts.coint(useful_df[corr_row['Currency1']], 
                                                            useful_df[corr_row['Currency2']]), axis=1)

        corr['Cointegration'] = np.vectorize(lambda x: x[0])(coint_series)
        corr['Criticals'] = np.vectorize(lambda x: x[2][0])(coint_series)
        
        return corr[(corr['Cointegration'] < corr['Criticals'])]
