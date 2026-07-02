import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. Generate realistic chemical process data ──────────────────────────────
np.random.seed(42)
n = 500

time = np.arange(n)
temperature = 350 + 10 * np.sin(2 * np.pi * time / 100) + np.random.normal(0, 2, n)
pressure    = 5 + 0.5 * np.sin(2 * np.pi * time / 100 + 1) + np.random.normal(0, 0.1, n)
flow_rate   = 100 + 5 * np.cos(2 * np.pi * time / 100) + np.random.normal(0, 3, n)
conversion  = 0.85 + 0.05 * np.sin(2 * np.pi * time / 100) + np.random.normal(0, 0.01, n)
conversion  = np.clip(conversion, 0, 1)

# Inject anomalies
temperature[100:105] += 30
pressure[250:255]    += 2
flow_rate[400:405]   -= 40

df = pd.DataFrame({
    'Time':        time,
    'Temperature': temperature,
    'Pressure':    pressure,
    'Flow_Rate':   flow_rate,
    'Conversion':  conversion
})

df.to_csv('process_data.csv', index=False)
print("Dataset created:", df.shape)
print(df.describe().round(2))

# ── 2. Anomaly detection (3-sigma rule) ──────────────────────────────────────
def detect_anomalies(series):
    mean, std = series.mean(), series.std()
    return (series - mean).abs() > 3 * std

anomalies = {col: detect_anomalies(df[col])
             for col in ['Temperature', 'Pressure', 'Flow_Rate']}

for col, mask in anomalies.items():
    print(f"{col}: {mask.sum()} anomalies detected")

# ── 3. Visualisations ────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Chemical Process Data Analysis', fontsize=16, fontweight='bold')

# Plot 1 — Temperature over time with anomalies highlighted
ax = axes[0, 0]
ax.plot(df['Time'], df['Temperature'], color='steelblue', linewidth=0.8, label='Temperature')
ax.scatter(df['Time'][anomalies['Temperature']],
           df['Temperature'][anomalies['Temperature']],
           color='red', zorder=5, label='Anomaly', s=40)
ax.set_title('Reactor Temperature Over Time')
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Temperature (K)')
ax.legend()

# Plot 2 — Pressure over time with anomalies highlighted
ax = axes[0, 1]
ax.plot(df['Time'], df['Pressure'], color='darkorange', linewidth=0.8, label='Pressure')
ax.scatter(df['Time'][anomalies['Pressure']],
           df['Pressure'][anomalies['Pressure']],
           color='red', zorder=5, label='Anomaly', s=40)
ax.set_title('System Pressure Over Time')
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Pressure (bar)')
ax.legend()

# Plot 3 — Correlation heatmap
ax = axes[1, 0]
corr = df[['Temperature', 'Pressure', 'Flow_Rate', 'Conversion']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax, linewidths=0.5)
ax.set_title('Process Variable Correlation Heatmap')

# Plot 4 — Temperature vs Conversion scatter
ax = axes[1, 1]
sc = ax.scatter(df['Temperature'], df['Conversion'],
                c=df['Pressure'], cmap='viridis', alpha=0.6, s=15)
plt.colorbar(sc, ax=ax, label='Pressure (bar)')
ax.set_title('Temperature vs Conversion (coloured by Pressure)')
ax.set_xlabel('Temperature (K)')
ax.set_ylabel('Conversion')

plt.tight_layout()
plt.savefig('process_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("Plot saved as process_analysis.png")
