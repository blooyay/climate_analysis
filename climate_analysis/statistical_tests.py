import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests
from scipy.stats import pearsonr
from statsmodels.tsa.stattools import ccf


def granger_causality(df, col1, col2):
    """
    Compute the Granger causality value between two columns
    """
    granger = grangercausalitytests(df[[col1, col2]], maxlag=1, verbose=False)
    return granger[1][0]['ssr_ftest'][1] 

def corr(col1, col2):
    """
    Compute the correlation coefficient between two columns
    """
    corr, p_value = pearsonr(col1, col2)
    return corr, p_value
    
def corr_step_delay(df, col1, col2, limit=20):
    """
    Return the number of steps which col2 is delayed in response to col1
    """
    cross_corr = ccf(df[col1], df[col2])[:limit]

    return cross_corr[np.argmax(cross_corr)]

def correlated_variables(df, thresh=0.8):
    """
    Return variables and their correlation coefficient that 
    have a correlation value above a given threshold
    """
    correlation_matrix = df.corr()
    correlated_pairs = correlation_matrix.unstack().reset_index()
    correlated_pairs.columns = ['Column1', 'Column2', 'Correlation']

    high_corr_pairs = correlated_pairs[
        (correlated_pairs['Correlation'].abs() > thresh) & 
        (correlated_pairs['Column1'] != correlated_pairs['Column2']) &
        (~correlated_pairs['Column1'].str.endswith('_scaled')) &
        (~correlated_pairs['Column2'].str.endswith('_scaled'))
    ]

    high_corr_pairs = high_corr_pairs.drop_duplicates(subset=['Correlation'])        
    return high_corr_pairs