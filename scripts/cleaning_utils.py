import pandas as pd
import numpy as np

def identify_speed_outliers(df, column='speed_mph', method='iqr', threshold=1.5,
                           abs_max=None, sensor_column='sensor'):
    """
    Identify outliers in wind speed data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing wind speed data
    column : str, optional
        Name of the column containing speed values
    method : str, optional
        Method for outlier detection: 'iqr' (Interquartile Range) or 'zscore'
    threshold : float, optional
        Threshold for outlier detection
        For IQR method: values > Q3 + threshold*IQR or < Q1 - threshold*IQR
        For zscore method: absolute z-score > threshold
    abs_max : float, optional
        Absolute maximum value regardless of method
    sensor_column : str, optional
        Name of the column containing sensor identifiers
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with outlier flag column added ('is_outlier')
    """
    df = df.copy()
    df['is_outlier'] = False
    
    # Process each sensor separately
    for sensor in df[sensor_column].unique():
        sensor_mask = df[sensor_column] == sensor
        values = df.loc[sensor_mask, column]
        
        if method == 'iqr':
            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            outliers = (values < lower_bound) | (values > upper_bound)
            
        elif method == 'zscore':
            z_scores = (values - values.mean()) / values.std()
            outliers = abs(z_scores) > threshold
            
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Apply absolute maximum if provided
        if abs_max is not None:
            outliers = outliers | (values > abs_max)
            
        df.loc[sensor_mask, 'is_outlier'] = outliers
    
    return df


def remove_or_replace_outliers(df, outlier_column='is_outlier', method='remove',
                              replacement_method='median', sensor_column='sensor',
                              value_column='speed_mph'):
    """
    Remove or replace outliers in wind data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing wind data with outlier flags
    outlier_column : str, optional
        Name of the column containing outlier flags
    method : str, optional
        Method for handling outliers: 'remove' or 'replace'
    replacement_method : str, optional
        Method for replacement: 'median', 'mean', or 'interpolate'
    sensor_column : str, optional
        Name of the column containing sensor identifiers
    value_column : str, optional
        Name of the column containing values to replace
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with outliers handled according to method
    """
    df = df.copy()
    
    if method == 'remove':
        return df[~df[outlier_column]]
    
    elif method == 'replace':
        # Process each sensor separately
        for sensor in df[sensor_column].unique():
            sensor_mask = df[sensor_column] == sensor
            outlier_mask = sensor_mask & df[outlier_column]
            
            if replacement_method == 'median':
                replacement_value = df.loc[sensor_mask & ~df[outlier_column], value_column].median()
                df.loc[outlier_mask, value_column] = replacement_value
                
            elif replacement_method == 'mean':
                replacement_value = df.loc[sensor_mask & ~df[outlier_column], value_column].mean()
                df.loc[outlier_mask, value_column] = replacement_value
                
            elif replacement_method == 'interpolate':
                # Sort by time first
                temp_df = df[sensor_mask].sort_values('time')
                temp_df.loc[temp_df[outlier_column], value_column] = np.nan
                temp_df[value_column] = temp_df[value_column].interpolate(method='time')
                df.loc[sensor_mask, value_column] = temp_df[value_column].values
                
            else:
                raise ValueError(f"Unknown replacement method: {replacement_method}")
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return df