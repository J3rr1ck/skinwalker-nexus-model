import pandas as pd
import numpy as np

def calculate_nexus_combo():
    # Load historical events and enhanced weather
    events_df = pd.read_csv('data/skinwalker_historical_events.csv')
    weather_df = pd.read_csv('data/historical_weather_enhanced.csv')
    
    # Load full climatology baseline
    climatology_df = pd.read_csv('data/skinwalker_climatology_baseline.csv')
    
    events_df['ds'] = pd.to_datetime(events_df['ds'])
    weather_df['ds'] = pd.to_datetime(weather_df['ds'])
    climatology_df['ds'] = pd.to_datetime(climatology_df['ds'])
    
    # Merge events with anomaly weather
    merged_events = pd.merge_asof(
        events_df.sort_values('ds'),
        weather_df.sort_values('ds'),
        on='ds',
        direction='nearest'
    )
    
    # Constants
    QUARTZ_VOL_FRACTION = 0.20
    BASIN_REFLECTIVITY_COEFF = 0.85
    IRON_MINERAL_INDEX = 0.15
    GEO_POTENTIAL = QUARTZ_VOL_FRACTION + IRON_MINERAL_INDEX
    
    def calculate_nii(row):
        moisture_factor = row['soil_moisture'] / 0.4
        pressure_instability = (1013 - row['pressure_hpa']) / 10
        moisture_precip = 1.0 + (row['precipitation_mm'] * 0.5)
        bowl_trap_factor = row['vpd_kpa'] * BASIN_REFLECTIVITY_COEFF
        return (moisture_factor * moisture_precip) + pressure_instability + bowl_trap_factor + GEO_POTENTIAL

    merged_events['nexus_instability_index'] = merged_events.apply(calculate_nii, axis=1)
    climatology_df['nexus_instability_index'] = climatology_df.apply(calculate_nii, axis=1)
    
    # Save datasets
    merged_events.to_csv('data/skinwalker_nexus_combo_analysis.csv', index=False)
    climatology_df.to_csv('data/skinwalker_climatology_with_nii.csv', index=False)
    
    print("--- Uinta Basin Nexus: Combo Analysis Summary ---")
    print(f"Historical Events NII calculated. Mean: {merged_events.nexus_instability_index.mean():.2f}")
    print(f"Climatology Baseline NII calculated. Mean: {climatology_df.nexus_instability_index.mean():.2f}")


if __name__ == "__main__":
    calculate_nexus_combo()
