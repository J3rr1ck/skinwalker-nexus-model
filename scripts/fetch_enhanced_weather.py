import pandas as pd
import requests
import time

def fetch_enhanced_weather():
    # Load historical events
    df = pd.read_csv('data/skinwalker_historical_events.csv')
    df['ds'] = pd.to_datetime(df['ds'])
    unique_dates = df['ds'].dt.date.unique()
    
    lat, lon = 40.257, -109.893
    weather_records = []
    
    print(f"Fetching Enhanced Meteorological Data (Moisture, Soil, Pressure)...")
    
    for date in unique_dates:
        date_str = date.strftime('%Y-%m-%d')
        # Adding precipitation, soil_moisture, and vapor_pressure_deficit (proxy for electrical potential/instability)
        url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
               f"&start_date={date_str}&end_date={date_str}"
               f"&hourly=temperature_2m,relative_humidity_2m,surface_pressure,dew_point_2m,"
               f"precipitation,soil_moisture_0_to_7cm,vapor_pressure_deficit")
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                hourly = data.get('hourly', {})
                for i in range(len(hourly.get('time', []))):
                    weather_records.append({
                        'ds': hourly['time'][i],
                        'temp_c': hourly['temperature_2m'][i],
                        'humidity': hourly['relative_humidity_2m'][i],
                        'pressure_hpa': hourly['surface_pressure'][i],
                        'precipitation_mm': hourly['precipitation'][i],
                        'soil_moisture': hourly['soil_moisture_0_to_7cm'][i],
                        'vpd_kpa': hourly['vapor_pressure_deficit'][i]
                    })
            else:
                print(f"  Failed: {date_str}")
        except Exception as e:
            print(f"  Error: {e}")
        time.sleep(1)

    enhanced_weather_df = pd.DataFrame(weather_records)
    enhanced_weather_df.to_csv('data/historical_weather_enhanced.csv', index=False)
    print("Enhanced weather data saved.")

if __name__ == "__main__":
    fetch_enhanced_weather()
