import os
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import ccf
import seaborn as sns

plot_vars = {'ocean_ph': 'Ocean ph', 
             'pollution': 'Pollution',
             'surface_temp': 'Surface Temp',
             'd_total': 'Total Disasters'}

def plot_normalized(df):
    plt.figure(figsize=(10, 6))  # Optional: set the figure size
    plt.plot(df.index, df['pollution_scaled'], linestyle='-', color='blue', label='Pollution')
    plt.plot(df.index, df['d_total_scaled'], linestyle='-', color='red', label='Total Disasters')
    plt.plot(df.index, df['surface_temp_scaled'], linestyle='-', color='green', label='Surface Temp')
    plt.plot(df.index, df['ocean_ph_scaled'], linestyle='-', color='orange', label='Ocean ph')

    plt.xlabel('Date')
    plt.ylabel('Normalized Values')
    plt.title('Pollution, Total Disasters, Global Surface Temperature, and Ocean ph')
    plt.legend() 
    if not os.path.exists('output/'):
        os.makedirs('output/')
    plt.savefig('output/normalized_vars_over_time.png')
    
    
def plot_cross_corr(col1, col2):
    """
    Plot the cross correlation between two columns of a pd.DataFrame
    """
    cross_corr = ccf(col1, col2)[:20]

    plt.figure(figsize=(10, 6))
    plt.stem(cross_corr)
    plt.title(f'Cross-Correlation Function between {plot_vars[col1.name]} and {plot_vars[col2.name]}')
    plt.xlabel('Lag')
    plt.ylabel('Cross-Correlation')
    if not os.path.exists('output/'):
        os.makedirs('output/')
    plt.savefig(f'output/cross_corr_{col1.name}_{col2.name}.png')
    
    
def plot_forecast(df, forecast_df, conf_df, var_name):

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[var_name], label='Historical')
    plt.fill_between(forecast_df.index, 
                    conf_df['Lower Bound'], 
                    conf_df['Upper Bound'], 
                    color='pink', alpha=0.3, label='Confidence Interval')
    plt.xlabel('Date')
    plt.ylabel(plot_vars[var_name])
    plt.title(f'{plot_vars[var_name]} Forecast')
    plt.legend()
    if not os.path.exists('output/'):
        os.makedirs('output/')
    plt.savefig(f'output/forecast_{var_name}.png')
    
def correlation_matrix(df):
    """
    Plot the correlation matrix heat map
    """
    # Create a heatmap
    correlation_matrix = df.corr()
    plt.figure(figsize=(15, 15))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix')
    if not os.path.exists('output/'):
        os.makedirs('output/')
    plt.savefig('output/correlation.png')