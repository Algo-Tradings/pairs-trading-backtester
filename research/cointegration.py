import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
import os
path = os.path.dirname(__file__)

class Cointegration():

    def get_cointegration(self, corr: pd.DataFrame, cleared_df: pd.DataFrame) -> pd.DataFrame:

        
        coint_df = self.__get_ts_coint_result(corr, cleared_df)
        coint_df.to_csv(os.path.join(
            path, '..', 'data/processing/coint_output.csv'), index=False)
        
        return coint_df

    def __get_ts_coint_result(self, corr: pd.DataFrame, cleared_df: pd.DataFrame) -> pd.DataFrame:
        self.cleared_df = cleared_df

        (cointegration, critical) = np.vectorize(self.__apply_ts_coint)(corr['Currency1'], corr['Currency2'])
        corr['Cointegration'] = cointegration
        corr['Criticals'] = critical  
                                 
        return corr[(corr['Cointegration'] < corr['Criticals'])]

    def __apply_ts_coint(self, currency1, currency2):  
        ts_coint = ts.coint(self.cleared_df[currency1], self.cleared_df[currency2])
        return ts_coint[0], ts_coint[2][0]
    