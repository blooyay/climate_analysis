from climate_analysis.plotter import plot_normalized, plot_cross_corr, plot_forecast, correlation_matrix
from climate_analysis.data_loader import load_data
from climate_analysis.statistical_tests import granger_causality, corr, corr_step_delay, correlated_variables
from climate_analysis.forecaster import forecast, bounds_at_year

if __name__ == '__main__':
    # Load the data
    df = load_data()
    
    # Create a plot of the normalized data to visualize relationships
    plot_normalized(df)
    
    # Plot the cross correlation between pollution and surface temperature 
    plot_cross_corr(df['pollution'], df['surface_temp'])
    
    # Ocean ph value forecasting and confidence interval in 2050
    forecast_df, conf_df = forecast(df['ocean_ph'])
    plot_forecast(df, forecast_df, conf_df, 'ocean_ph')
    bounds = bounds_at_year(conf_df)
    print("\n\nYear 2050 Ocean ph confidence interval: ", bounds)
    
    # Pollution value forecasting and confidence interval in 2050
    forecast_df, conf_df = forecast(df['pollution'])
    plot_forecast(df, forecast_df, conf_df, 'pollution')
    bounds = bounds_at_year(conf_df)
    print("\n\nYear 2050 Pollution (CO2 ppm) confidence interval: ", bounds)
    
    # get the delay in years that maximizes the correlation between two variables
    delay = corr_step_delay(df, 'pollution', 'surface_temp', limit=10)  
    print('Years that surface temp follows pollution: ', delay)
    
    # Get the individual correlation and associated correlation test p value 
    correlation, p = corr(df['pollution'], df['surface_temp'])
    print('Correlation between pollution and surface temp: ', correlation, end='')
    print(' with p=', p)
    
    # Compute the Granger Causality with a lag of 1 year
    granger = granger_causality(df, 'pollution', 'surface_temp')
    print('\n\nGranger Causality between Pollution and Surface Temp: ', granger)
    
    # Find which variable pairs have high correlation
    thresh = 0.8
    corr_vars = correlated_variables(df, thresh=thresh)
    print(f'\n\nThese variable pairs have a correlation above {thresh}: \n', corr_vars.values)
    
    # Plot the correlation matrix
    correlation_matrix(df)
    print('\n\nSaved correlation matrix')
    
    
    
