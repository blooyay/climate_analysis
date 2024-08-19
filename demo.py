from climate_analysis.plotter import plot_normalized
from climate_analysis.data_loader import load_data
from climate_analysis.statistical_tests import granger_causality, corr, corr_step_delay
from climate_analysis.forecaster import forecast

if __name__ == '__main__':
    df = load_data()
    
    plot_normalized(df)

    print(corr(df, 'pollution', 'surface_temp'))