import os
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import ccf


def plot_normalized(df):
    plt.figure(figsize=(10, 6))  # Optional: set the figure size
    plt.plot(df.index, df['pollution_scaled'], linestyle='-', color='blue', label='Pollution')
    plt.plot(df.index, df['d_total_scaled'], linestyle='-', color='red', label='Total Disasters')
    plt.plot(df.index, df['surface_temp_scaled'], linestyle='-', color='green', label='Surface Temp')
    plt.plot(df.index, df['ocean_ph_scaled'], linestyle='-', color='orange', label='Ocean ph')

    plt.xlabel('Date')
    plt.ylabel('Normalized Values')
    plt.title('Pollution, Total Disasters, and Global Surface Temperature')
    plt.legend() 
    if not os.path.exists('output/'):
        os.makedirs('output/')
    plt.savefig('output/normalized_vars_over_time.png')
    
    
def plot_cross_corr(df, col1, col2):
    """
    Plot the cross correlation between two columns of a pd.DataFrame
    """
    cross_corr = ccf(df[col1], df[col2])[:20]

    plt.figure(figsize=(10, 6))
    plt.stem(cross_corr)
    plt.title('Cross-Correlation Function between Pollution and Surface Temperature')
    plt.xlabel('Lag')
    plt.ylabel('Cross-Correlation')
    if not os.path.exists('output/'):
        os.makedirs('output/')
    plt.savefig(f'output/cross_corr_{col2}_{col2}.png')
    
    
def plot_forecast(df, forecast_df, conf_df, var_name):

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[var_name], label='Historical')
    plt.fill_between(forecast_df.index, 
                    conf_df['Lower Bound'], 
                    conf_df['Upper Bound'], 
                    color='pink', alpha=0.3, label='Confidence Interval')
    plt.xlabel('Date')
    plt.ylabel(var_name)
    plt.title(f'{var_name} Forecast')
    plt.legend()
    if not os.path.exists('output/'):
        os.makedirs('output/')
    plt.savefig('output/cross_corr_col2_col2.png')