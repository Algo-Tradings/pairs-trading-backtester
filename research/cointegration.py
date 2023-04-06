
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
import os
path = os.path.dirname(__file__)


class Cointegration():

    def get_cointegration(self, corr: pd.DataFrame, cleared_df: pd.DataFrame
                          ) -> pd.DataFrame:

        ts_coint = self.__get_ts_coint(corr, cleared_df)
        ts_coint.to_csv(os.path.join(path,'..','data/processing/coint_output.csv'), index=False)
        return ts_coint

    def __get_ts_coint(self, corr: pd.DataFrame, cleared_df: pd.DataFrame) -> pd.DataFrame:
        coint_series = corr.apply(lambda corr_row: ts.coint(cleared_df[corr_row['Currency1']],
                                                            cleared_df[corr_row['Currency2']]), axis=1)

        corr['Cointegration'] = np.vectorize(lambda x: x[0])(coint_series)
        corr['Criticals'] = np.vectorize(lambda x: x[2][0])(coint_series)

        return corr[(corr['Cointegration'] < corr['Criticals'])]
