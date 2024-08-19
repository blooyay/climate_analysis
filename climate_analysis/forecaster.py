from pmdarima import auto_arima
import pandas as pd

def forecast(col, n_steps=100):
    """
    Forecast value into future years
    """
    df = df.sort_index()

    # Fit the auto_arima model
    model = auto_arima(df[col], 
                    start_p=1, start_q=1,
                    max_p=5, max_q=5, m=1,
                    start_P=0, seasonal=False,
                    d=None, D=None,
                    trace=True,
                    error_action='ignore',
                    suppress_warnings=True,
                    stepwise=True)

    forecast_periods = n_steps
    forecast, conf_int = model.predict(n_periods=forecast_periods, return_conf_int=True)

    future_dates = pd.date_range(start=df.index[-1] + pd.DateOffset(years=1), periods=forecast_periods, freq='Y')

    forecast_df = pd.DataFrame(forecast, index=future_dates, columns=['Forecast'])
    conf_df = pd.DataFrame(conf_int, index=future_dates, columns=['Lower Bound', 'Upper Bound'])
    
    return forecast_df, conf_df

def bounds_at_year(conf_df, year=2050):
    """
    Return the upper and lower confidence bounds at specified year
    """
    return list(conf_df[conf_df.index.year == year].iloc[0])