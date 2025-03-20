import os
import sqlite3
import pandas as pd
import glob
from tqdm import tqdm

# Default direction categories - 16-point compass rose
DEFAULT_DIRECTION_CATEGORIES = [22.5, 45.0, 67.5, 90.0, 112.5, 135.0, 157.5,
                                180.0, 202.5, 225.0, 247.5, 270.0, 292.5, 315.0, 337.5, 360.0]

def load_wind_data_from_sqlite(file_paths, direction_categories=None, convert_to_mph=True):
    """
    Load wind data from SQLite databases and perform basic transformations.
    
    Parameters:
    -----------
    file_paths : list
        List of paths to .s3db files containing wind data
    direction_categories : list, optional
        List of direction angles for categorizing wind direction.
        Defaults to 16-point compass rose if None.
    convert_to_mph : bool, optional
        Whether to convert wind speed from m/s to mph. Default is True.
        
    Returns:
    --------
    pandas.DataFrame
        Combined dataframe with all wind data
    """
    if direction_categories is None:
        direction_categories = DEFAULT_DIRECTION_CATEGORIES
    
    df_list = []

    for s3db_file_path in tqdm(file_paths, desc="Loading wind data"):
        # Extract sensor name from filename
        sensor = os.path.splitext(os.path.basename(s3db_file_path))[0]

        # Connect to SQLite database
        conn = sqlite3.connect(s3db_file_path)

        # Load data from Wind table
        df = pd.read_sql_query("SELECT * FROM Wind", conn,
                              dtype={"speed": float, "gust": float, "direction": int, "time": str})

        # Add sensor name as column
        df["sensor"] = sensor
        
        # Convert wind speeds to mph if requested
        if convert_to_mph:
            df['speed_mph'] = round(df['speed'] * 2.23694, 1)
            df['gust_mph'] = round(df['gust'] * 2.23694, 1)

        df_list.append(df)
        conn.close()

    # Combine all dataframes
    if not df_list:
        raise ValueError("No data loaded - check file paths")
        
    combined_df = pd.concat(df_list, ignore_index=True)

    # Remove ID column as it's meaningless once databases are combined
    combined_df = combined_df.drop('id', axis=1)

    # Convert time strings to datetime objects
    combined_df['time'] = pd.to_datetime(combined_df['time'])

    # Categorize wind direction based on direction categories
    # Special case for 360/0 degrees
    combined_df['direction_category'] = combined_df['direction'].apply(
        lambda x: min(direction_categories, 
                      key=lambda d: abs((d - x) % 360) if abs((d - x) % 360) <= 11.25 
                      else abs((d - x) % 360 - 360)))

    return combined_df


def get_wind_files(folder_path, file_pattern="*.s3db", exclude_list=None):
    """
    Get list of wind data files from a folder based on pattern.
    
    Parameters:
    -----------
    folder_path : str
        Path to folder containing wind data files
    file_pattern : str, optional
        Glob pattern to match files. Default is "*.s3db"
    exclude_list : list, optional
        List of filenames to exclude
        
    Returns:
    --------
    list
        List of file paths matching the pattern
    """
    file_paths = glob.glob(os.path.join(folder_path, file_pattern))
    
    if exclude_list:
        file_paths = [f for f in file_paths 
                     if os.path.basename(f) not in exclude_list]
    
    return file_paths