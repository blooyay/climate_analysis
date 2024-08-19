import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
from sklearn.preprocessing import MinMaxScaler

def load_data(surface_temp_path='data/annual_surface_temperature_change.csv', 
              climate_disasters_path='data/climate-related_disasters_frequency.csv', 
              air_pollution_path='data/air_pollution.csv', 
              ocean_ph_path='data/global_omi_health_carbon_ph_area_averaged_1985_P20230930.nc'):
    
    # annual 1961 - 2022, average surface temp deg C
    surface_temp = pd.read_csv(surface_temp_path)
    surface_temp = surface_temp[surface_temp['Country'] == 'United States']
    surface_temp = surface_temp.loc[:, surface_temp.columns.str.startswith('F')]
    surface_temp = surface_temp.transpose().reset_index()
    surface_temp.rename(columns={'index': 'date', 211: 'surface_temp'}, inplace=True)
    surface_temp['date'] = pd.to_datetime(surface_temp['date'], format='F%Y')
    surface_temp.sort_values(by='date', inplace=True)

    # annual 1980 - 2022, disaster count per category
    climate_disasters = pd.read_csv(climate_disasters_path)
    climate_disasters = climate_disasters[climate_disasters['Country'] == 'United States']
    climate_disasters['Indicator'] = climate_disasters['Indicator'].str.split(': ', expand=True)[1]
    climate_disasters = climate_disasters.loc[:, climate_disasters.columns.str.startswith('F') | (climate_disasters.columns == 'Indicator')]
    climate_disasters = climate_disasters.T.iloc[1:]
    climate_disasters.columns = ['d_drought', 'd_extreme temperature', 'd_flood', 'd_landslide', 'd_storm', 'd_total', 'd_wildfire']
    climate_disasters.reset_index(inplace=True)
    climate_disasters.rename(columns={'index': 'date'}, inplace=True)
    climate_disasters['date'] = pd.to_datetime(climate_disasters['date'], format='F%Y')
    climate_disasters.sort_values(by='date', inplace=True)
    climate_disasters.fillna(0, inplace=True)

    # monthly 1958-2023, world avg co2 ppm
    air_pollution = pd.read_csv(air_pollution_path)
    air_pollution['date'] = pd.to_datetime(air_pollution['Date'], format='%YM%m')
    air_pollution = air_pollution[air_pollution['Unit'] == 'Parts Per Million'][['date', 'Value']].sort_values(by='date')[:-1]
    air_pollution.rename(columns={'Value': 'pollution'}, inplace=True)

    # annual 1985 - 2022, average ocean ph level
    ds = xr.open_dataset(ocean_ph_path)
    ph = ds['ph']
    ph = ph.to_dataframe().rename(columns={'ph': 'ocean_ph'})
    ph.rename_axis('date', inplace=True)
    ph.index = ph.index.to_period('Y').start_time

    # combine data
    df = pd.merge(air_pollution, climate_disasters, on='date')
    df = pd.merge(df, surface_temp, on='date')
    df = pd.merge(df, ph, on='date')

    # create scaled columns for plotting
    scaler = MinMaxScaler()
    columns_to_scale = ['pollution', 'd_total', 'surface_temp', 'ocean_ph']
    renamed = [c + '_scaled' for c in columns_to_scale]
    scaler = MinMaxScaler()
    df[renamed] = scaler.fit_transform(df[columns_to_scale])
    df.set_index('date', inplace=True)
    
    return df