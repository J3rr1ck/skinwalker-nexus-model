import pandas as pd
import numpy as np

def calculate_nexus_combo():
    # Load historical events and enhanced weather
    events_df = pd.read_csv('data/skinwalker_historical_events.csv')
    weather_df = pd.read_csv('data/historical_weather_enhanced.csv')
    
    events_df['ds'] = pd.to_datetime(events_df['ds'])
    weather_df['ds'] = pd.to_datetime(weather_df['ds'])
    
    # Merge
    merged_df = pd.merge_asof(
        events_df.sort_values('ds'),
        weather_df.sort_values('ds'),
        on='ds',
        direction='nearest'
    )
    
    # --- Geological & Physical Constants (The "Combo" Parameters) ---
    QUARTZ_VOL_FRACTION = 0.20
    GILSONITE_DENSITY_EST = 1.05 # g/cm3 (Hydrocarbon rich)
    BASIN_REFLECTIVITY_COEFF = 0.85 # The "Bowl" effect
    IRON_MINERAL_INDEX = 0.15 # Baseline iron-rich mineral presence
    
    # --- Nexus Instability Index (NII) Calculation ---
    # We model instability as a function of:
    # 1. Soil Conductivity (Moisture)
    # 2. Atmospheric Pressure Drops (Sky Electricity/Lightning Potential)
    # 3. Vapor Pressure Deficit (Ducting/Instability)
    # 4. Geological Piezoelectric potential (Quartz stress)
    
    def calculate_nii(row):
        # Normalize factors (approximate scales)
        moisture_factor = row['soil_moisture'] / 0.4 # Higher is more conductive
        pressure_instability = (1013 - row['pressure_hpa']) / 10 # Lower pressure = more discharge potential
        moisture_precip = 1.0 + (row['precipitation_mm'] * 0.5)
        
        # The "Bowl/Ducting" Combo
        # Higher VPD and specific pressure patterns trap EM waves in the basin
        bowl_trap_factor = row['vpd_kpa'] * BASIN_REFLECTIVITY_COEFF
        
        # Geological Constant (Stress-responsive quartz + iron minerals)
        geo_potential = QUARTZ_VOL_FRACTION + IRON_MINERAL_INDEX
        
        # Unified Anomaly Factor (UAF)
        uaf = (moisture_factor * moisture_precip) + pressure_instability + bowl_trap_factor + geo_potential
        return uaf

    merged_df['nexus_instability_index'] = merged_df.apply(calculate_nii, axis=1)
    
    # Save the combo dataset
    merged_df.to_csv('data/skinwalker_nexus_combo_analysis.csv', index=False)
    
    print("--- Uinta Basin Nexus: Combo Analysis Summary ---")
    print("High Instability Events (NII > 2.0):")
    high_nii = merged_df[merged_df['nexus_instability_index'] > 2.0]
    print(high_nii[['ds', 'label', 'nexus_instability_index', 'soil_moisture', 'precipitation_mm']].to_string(index=False))
    
    # Correlation with RF/Gamma
    print("\nRF/Gamma Anomaly Correlation with Nexus Index:")
    target_events = merged_df[merged_df['unique_id'].str.contains('RAD|EM')]
    for _, row in target_events.iterrows():
        print(f"  {row['ds']}: {row['label']} | NII: {row.nexus_instability_index:.2f}")

if __name__ == "__main__":
    calculate_nexus_combo()
