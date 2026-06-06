import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_nii_based_predictions():
    # Load historical ground truth with NII scores
    try:
        df = pd.read_csv('data/skinwalker_nexus_combo_analysis.csv')
    except FileNotFoundError:
        print("Historical combo analysis not found. Run scripts/calculate_nexus_combo.py first.")
        return

    df['ds'] = pd.to_datetime(df['ds'])
    
    # Define Prediction Window: June 2026 to June 2027
    prediction_start = datetime(2026, 6, 6)
    prediction_end = datetime(2027, 6, 6)
    future_dates = pd.date_range(start=prediction_start, end=prediction_end, freq='D')
    
    unique_ids = df['unique_id'].unique()
    
    # Statistical parameters from historical NII
    mean_nii = df['nexus_instability_index'].mean()
    std_nii = df['nexus_instability_index'].std()
    
    predictions = []

    print(f"--- Generating NII-Driven Anomaly Forecast (June 2026 - June 2027) ---")
    print(f"Baseline Nexus Instability Index (NII): {mean_nii:.2f} +/- {std_nii:.2f}")

    for ds in future_dates:
        # Simulate a daily NII value based on historical variance
        # In a production environment, this would ingest real-time weather forecasts
        daily_nii = np.random.normal(mean_nii, std_nii)
        
        # Trigger anomalies based on historical NII thresholds
        # Threshold: NII > (Mean + 1.5 * STD)
        is_high_strangeness = daily_nii > (mean_nii + 1.5 * std_nii)
        
        for sensor_id in unique_ids:
            if is_high_strangeness:
                # High NII event: Correlate with historical anomaly types
                if 'RAD_GAMMA' in sensor_id:
                    y_pred = 0.5 + np.random.exponential(1.5)
                    label = f"Predicted Gamma Burst (NII: {daily_nii:.2f})"
                elif 'EM_1_6GHZ' in sensor_id:
                    y_pred = -40 + np.random.normal(0, 10)
                    label = f"Predicted RF Emission (NII: {daily_nii:.2f})"
                elif 'GPS_ALT' in sensor_id:
                    y_pred = -100 - np.random.exponential(150)
                    label = f"Predicted GPS Collapse (NII: {daily_nii:.2f})"
                else:
                    y_pred = df[df['unique_id'] == sensor_id]['y'].mean() * 1.5
                    label = f"Nexus Instability Event (NII: {daily_nii:.2f})"
                
                predictions.append({
                    'ds': ds,
                    'unique_id': sensor_id,
                    'y': y_pred,
                    'label': label,
                    'type': 'NII-Triggered Anomaly',
                    'nii': daily_nii
                })
            else:
                # Normal baseline prediction
                y_base = df[df['unique_id'] == sensor_id]['y'].median()
                predictions.append({
                    'ds': ds,
                    'unique_id': sensor_id,
                    'y': y_base + np.random.normal(0, abs(y_base)*0.01),
                    'label': 'Normal Baseline',
                    'type': 'Baseline Forecast',
                    'nii': daily_nii
                })

    forecast_df = pd.DataFrame(predictions)
    forecast_df.to_csv('data/skinwalker_2027_nii_forecast.csv', index=False)
    
    # Filter only the predicted anomalies for the report
    anomalies_only = forecast_df[forecast_df['type'] == 'NII-Triggered Anomaly'].drop_duplicates('ds')
    print(f"\nForecast Complete. Identified {len(anomalies_only)} High-Strangeness Windows based on NII thresholds.")
    print(anomalies_only[['ds', 'label']].to_string(index=False))

if __name__ == "__main__":
    generate_nii_based_predictions()
