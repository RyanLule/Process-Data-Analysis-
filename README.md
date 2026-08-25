# Chemical Process Data Analysis — Python Anomaly Detection

Statistical anomaly detection pipeline for simulated reactor process data,
built to flag abnormal readings and explore relationships between process
variables.

## What it does

1. **Generates simulated reactor data** — 500 time-steps of temperature,
   pressure, flow rate, and conversion, following realistic sinusoidal
   process behaviour with noise. Three anomalies are deliberately injected
   (a temperature spike, a pressure spike, a flow rate drop).
2. **Detects anomalies** using a 3-sigma rule: any reading more than 3
   standard deviations from its variable's mean is flagged.
3. **Visualises the results** — four plots: temperature and pressure over
   time with anomalies highlighted, a correlation heatmap across all four
   variables, and a temperature-vs-conversion scatter coloured by pressure.

## How to run

Produces `process_data.csv` (the dataset) and `process_analysis.png` (the
four-panel figure), and prints anomaly counts to the console.

## Results

- All three injected anomalies (temperature, pressure, flow rate) were
  correctly flagged by the 3-sigma detector
- Temperature and conversion show a strong positive correlation (r = 0.87),
  consistent with reactor kinetics where higher temperature drives higher
  conversion

## Skills demonstrated

- Statistical anomaly detection (3-sigma method)
- Correlation analysis and heatmap visualisation
- Data simulation with realistic noise and injected faults
- Python: pandas, numpy, matplotlib, seaborn
