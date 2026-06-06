# Uinta Basin Nexus: Unified Anomaly Modeling at Skinwalker Ranch

This project implements a multi-factor physical model to analyze, verify, and predict localized physical anomalies at Skinwalker Ranch. It moves beyond standard time-series forecasting by integrating atmospheric electricity, soil conductivity, "Bowl" geometry, and geological mineralogy into a single **Nexus Instability Index (NII)**.

## The Nexus Combo Model
The core of this project is the hypothesis that the Uinta Basin acts as a natural physical resonator. Anomalies are not isolated events but the result of a "Combo Effect" involving:
1. **The Bowl Effect**: The basin's geometry traps and reflects electromagnetic waves (Atmospheric Ducting).
2. **Sky Electricity**: Atmospheric pressure drops and vapor pressure deficits create high electrical discharge potential.
3. **Ground Conductivity**: Soil moisture levels modulate the transport of subsurface energy.
4. **Geological Stress**: Quartz-rich sandstone mesas generate piezoelectric potentials under tectonic or mechanical stress.

## Mathematical Framework: The Nexus Instability Index (NII)
The **Nexus Instability Index (NII)**, or Unified Anomaly Factor (UAF), is calculated as:

$$NII = (C_{soil} \times P_{precip}) + E_{sky} + B_{trap} + G_{geo}$$

### Factor Breakdown
| Term | Name | Meaning | Calculation |
| :--- | :--- | :--- | :--- |
| **$C_{soil}$** | **Conductivity Factor** | Influence of ground moisture on energy transport. | $SoilMoisture / 0.4$ |
| **$P_{precip}$** | **Precipitation Multiplier** | Amplification of ground conductivity via active rainfall. | $1.0 + (Precip_{mm} \times 0.5)$ |
| **$E_{sky}$** | **Electrical Potential** | Atmospheric discharge potential based on pressure drops. | $(1013 - Pressure_{hPa}) / 10$ |
| **$B_{trap}$** | **Bowl Trap Factor** | EM wave confinement via Vapor Pressure Deficit & Reflectivity. | $VPD_{kPa} \times 0.85$ |
| **$G_{geo}$** | **Geological Constant** | Baseline potential from Quartz (20%) and Iron minerals (15%). | $0.20 + 0.15 = 0.35$ |

## Project Structure
- `data/`:
  - `skinwalker_historical_events.csv`: Verified ground-truth anomalies from scientific reports.
  - `skinwalker_historical_with_weather.csv`: Historical events merged with Open-Meteo API weather data.
  - `skinwalker_nexus_combo_analysis.csv`: The final dataset including NII scores for all historical events.
  - `skinwalker_2027_forecast.csv`: A probabilistic 12-month projection (June 2026 - June 2027).
- `scripts/`:
  - `assemble_historical_dataset.py`: Reconstructs the factual timeline from public reports.
  - `fetch_enhanced_weather.py`: Retrieves moisture, soil, and pressure data via API.
  - `calculate_nexus_combo.py`: Executes the NII mathematical model.
  - `verify_historical_events.py`: Cross-references events with physical constants (e.g., GPS timing/light speed).

## Analysis Summary (Historical Ground Truth)
The model identifies specific NII thresholds for documented anomaly classes:
- **RF Emissions (1.6 GHz)**: Typically manifest during stability windows (**NII 17.1 - 17.5**).
- **High-Strangeness Peaks**: The **July 10, 2023** Radiation Spike correlated with the highest recorded instability (**NII 20.88**).
- **GPS Collapses**: Frequently correlate with extreme atmospheric refractivity shifts (Modified Refractivity **M < 250**).

## Operational Workflow
1. **Reconstruct History**: `python3 scripts/assemble_historical_dataset.py`
2. **Retrieve Metrics**: `python3 scripts/fetch_enhanced_weather.py`
3. **Calculate Nexus**: `python3 scripts/calculate_nexus_combo.py`
4. **Predict Future**: `python3 scripts/predict_future_anomalies.py`
