import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_decadal_nii_predictions():
    # Load historical events with NII scores
    try:
        events_df = pd.read_csv('data/skinwalker_nexus_combo_analysis.csv')
        climatology_df = pd.read_csv('data/skinwalker_climatology_with_nii.csv')
    except FileNotFoundError:
        print("Required datasets not found. Run scripts/fetch_climatology.py and scripts/calculate_nexus_combo.py first.")
        return

    events_df['ds'] = pd.to_datetime(events_df['ds'])
    climatology_df['ds'] = pd.to_datetime(climatology_df['ds'])
    
    # Define Prediction Window: June 2026 to June 2027
    prediction_start = datetime(2026, 6, 6)
    prediction_end = datetime(2027, 6, 6)
    future_dates = pd.date_range(start=prediction_start, end=prediction_end, freq='D')
    
    unique_sensor_ids = events_df['unique_id'].unique()
    
    # Use decadal climatology to derive the NII distribution
    nii_distribution = climatology_df['nexus_instability_index'].values
    mean_nii = nii_distribution.mean()
    std_nii = nii_distribution.std()
    threshold = mean_nii + (1.5 * std_nii)
    
    predictions = []

    print(f"--- Generating 10-Year Informed NII Forecast (2026-2027) ---")
    print(f"Decadal NII Baseline: {mean_nii:.2f} +/- {std_nii:.2f}")
    print(f"High-Strangeness Threshold: NII > {threshold:.2f}")

    for ds in future_dates:
        # Sample NII from decadal distribution (weighted by month if we wanted more precision)
        daily_nii = np.random.choice(nii_distribution)
        
        # Trigger anomalies based on historical NII thresholds
        is_high_strangeness = daily_nii > threshold
        
        for sensor_id in unique_sensor_ids:
            if is_high_strangeness:
                # Correlate predicted anomaly value with historical event levels for that sensor
                hist_y = events_df[events_df['unique_id'] == sensor_id]['y']
                if not hist_y.empty:
                    y_pred = hist_y.mean() * (1.0 + np.random.normal(0, 0.1))
                else:
                    y_pred = 1.0 # Fallback
                
                label = f"Predicted Anomaly Window (NII: {daily_nii:.2f})"
                predictions.append({
                    'ds': ds,
                    'unique_id': sensor_id,
                    'y': y_pred,
                    'label': label,
                    'type': 'Decadal-Triggered Anomaly',
                    'predicted_nii': daily_nii
                })
            else:
                # Normal baseline
                # Use median value from historical background (approximated)
                if 'GPS' in sensor_id: y_base = 1550 
                elif 'RAD_GAMMA' in sensor_id: y_base = 0.15
                elif 'MAG' in sensor_id: y_base = 45.0
                elif 'EM' in sensor_id: y_base = -100.0
                else: y_base = 0.0
                
                predictions.append({
                    'ds': ds,
                    'unique_id': sensor_id,
                    'y': y_base + np.random.normal(0, 0.05),
                    'label': 'Normal Baseline',
                    'type': 'Baseline Forecast',
                    'predicted_nii': daily_nii
                })

    forecast_df = pd.DataFrame(predictions)
    forecast_df.to_csv('data/skinwalker_2027_decadal_forecast.csv', index=False)
    
    anomalies_only = forecast_df[forecast_df['type'] == 'Decadal-Triggered Anomaly'].drop_duplicates('ds')
    print(f"\nForecast Complete. Identified {len(anomalies_only)} potential anomaly windows in the next year.")
    print(anomalies_only[['ds', 'label']].head(20).to_string(index=False))

if __name__ == "__main__":
    generate_decadal_nii_predictions()
