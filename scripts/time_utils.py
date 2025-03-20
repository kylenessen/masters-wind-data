import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def adjust_for_dst(df, time_column='time', forward=True, dst_hours=1):
    """
    Adjust timestamps for Daylight Saving Time.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing timestamp data
    time_column : str, optional
        Name of the column containing timestamps
    forward : bool, optional
        If True, adds time (spring forward)
        If False, subtracts time (fall back)
    dst_hours : int, optional
        Number of hours to adjust by, default is 1
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with adjusted timestamps
    """
    df = df.copy()
    adjustment = timedelta(hours=dst_hours) if forward else timedelta(hours=-dst_hours)
    df[time_column] = df[time_column] + adjustment
    return df


def identify_time_gaps(df, time_column='time', threshold_minutes=30, 
                       sensor_column='sensor'):
    """
    Identify gaps in time series data that exceed a threshold.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing time series data
    time_column : str, optional
        Name of the column containing timestamps
    threshold_minutes : int, optional
        Minimum gap size to identify, in minutes
    sensor_column : str, optional
        Name of the column containing sensor identifiers
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with gaps identified, containing columns:
        - sensor: sensor identifier
        - gap_start: start time of gap
        - gap_end: end time of gap
        - gap_duration_minutes: duration of gap in minutes
    """
    gaps = []
    
    # Process each sensor separately
    for sensor in df[sensor_column].unique():
        sensor_data = df[df[sensor_column] == sensor].sort_values(time_column)
        
        # Calculate time differences
        sensor_data['time_diff'] = sensor_data[time_column].diff()
        
        # Identify gaps
        gap_rows = sensor_data[sensor_data['time_diff'] > 
                               pd.Timedelta(minutes=threshold_minutes)]
        
        for _, row in gap_rows.iterrows():
            gap_start = row[time_column] - row['time_diff']
            gap_end = row[time_column]
            gap_duration = row['time_diff'].total_seconds() / 60  # convert to minutes
            
            gaps.append({
                'sensor': sensor,
                'gap_start': gap_start,
                'gap_end': gap_end,
                'gap_duration_minutes': gap_duration
            })
    
    if not gaps:
        return pd.DataFrame(columns=['sensor', 'gap_start', 'gap_end', 'gap_duration_minutes'])
    
    return pd.DataFrame(gaps)