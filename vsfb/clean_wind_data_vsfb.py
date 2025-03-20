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

# Convert deployment time columns to datetime with mixed format
deployments['Deployed_time'] = pd.to_datetime(deployments['Deployed_time'], format='mixed')
deployments['Recovered_time'] = pd.to_datetime(deployments['Recovered_time'], format='mixed')

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
# Associate deployment_id with each wind record - using more efficient method
print("Associating wind data with deployment periods...")

# Create a subset of the deployments dataframe with only the columns we need
deployment_lookup = deployments[['deployment_id', 'wind_meter_name', 'Deployed_time', 'Recovered_time']]

# Get initial count of wind data records
initial_count = len(wind_data)

# More efficient approach using merge and conditional filtering
# First, create a copy of the wind data with just the columns we need for the join
wind_data_temp = wind_data[['time', 'wind_meter_name']].copy()

# Initialize deployment_id column as None
wind_data['deployment_id'] = None

# Process each deployment record
for idx, deployment in deployment_lookup.iterrows():
    # Filter wind data for this wind meter and time range
    mask = ((wind_data['wind_meter_name'] == deployment['wind_meter_name']) & 
            (wind_data['time'] >= deployment['Deployed_time']) & 
            (wind_data['time'] <= deployment['Recovered_time']))
    
    # Assign deployment_id to matching records
    wind_data.loc[mask, 'deployment_id'] = deployment['deployment_id']

# Get count of wind records with associated deployments
matched_count = wind_data['deployment_id'].notna().sum()
print(f"Associated {matched_count} of {initial_count} wind records with deployments ({matched_count/initial_count:.1%})")

# Print deployment summary
deployment_summary = wind_data[wind_data['deployment_id'].notna()].groupby('deployment_id').agg(
    record_count=('time', 'count'),
    start_time=('time', 'min'),
    end_time=('time', 'max')
).reset_index()

print("\nWind data records per deployment:")
print(deployment_summary)

# %%
# Add additional deployment information to wind data
# Get relevant columns from deployments
deployment_info = deployments[[
    'deployment_id', 'camera_name', 'height_m', 'horizontal_dist_to_cluster_m', 
    'view_direction', 'cluster_count', 'latitude', 'longitude'
]]

# Save processed wind data to CSV
# Filter to include only wind data with assigned deployment_id
wind_data_with_deployments = wind_data[wind_data['deployment_id'].notna()].copy()

# Join with deployment information
wind_data_with_deployments = wind_data_with_deployments.merge(
    deployment_info, 
    on='deployment_id',
    how='left'
)

# Select and order columns for output
columns_to_save = [
    # Deployment information
    'deployment_id', 'camera_name', 'wind_meter_name', 
    'height_m', 'horizontal_dist_to_cluster_m', 'view_direction', 'cluster_count',
    'latitude', 'longitude',
    # Wind data
    'time', 'speed', 'gust', 'direction', 'speed_mph', 'gust_mph', 'direction_category'
]
wind_data_with_deployments = wind_data_with_deployments[columns_to_save].sort_values(['deployment_id', 'time'])

# Save to CSV
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vsfb_wind_data.csv')
wind_data_with_deployments.to_csv(output_path, index=False)
print(f"Saved processed wind data to {output_path}")
print(f"Saved {len(wind_data_with_deployments)} records across {wind_data_with_deployments['deployment_id'].nunique()} deployments")

# Also save a deployment summary with date ranges and record counts
deployment_summary = wind_data_with_deployments.groupby('deployment_id').agg(
    camera_name=('camera_name', 'first'),
    wind_meter_name=('wind_meter_name', 'first'),
    record_count=('time', 'count'),
    start_time=('time', 'min'),
    end_time=('time', 'max'),
    latitude=('latitude', 'first'),
    longitude=('longitude', 'first')
).reset_index()

# Save summary to CSV
summary_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vsfb_wind_data_summary.csv')
deployment_summary.to_csv(summary_path, index=False)
print(f"Saved deployment summary to {summary_path}")

# %%

# %%
