# %%
import sys
import os
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.wind_data_loader import load_wind_data_from_sqlite, get_wind_files
# %%
# Load deployment information
deployments = pd.read_csv('deployments2023.csv')
# %%
# Get list of wind meters used in deployments
wind_meters = deployments['wind_meter_name'].dropna().unique().tolist()
print(f"Wind meters used in deployments: {wind_meters}")

# %%
# Get paths to wind meter sqlite files
raw_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'raw_data')
wind_files = {}

for meter in wind_meters:
    file_path = os.path.join(raw_data_dir, f"{meter}.s3db")
    if os.path.exists(file_path):
        wind_files[meter] = file_path
    else:
        print(f"Warning: Could not find file for wind meter {meter}")

print(f"Found {len(wind_files)} wind meter files out of {len(wind_meters)} meters")

# %%
# Load wind data from sqlite files
wind_data = load_wind_data_from_sqlite(list(wind_files.values()))

# Add the wind meter name for easier matching with deployments
wind_data['wind_meter_name'] = wind_data['sensor']

print(f"Loaded {len(wind_data)} wind data records across {wind_data['wind_meter_name'].nunique()} meters")
# %%
