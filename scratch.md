
I would like help adapting the code below. Essentially what it does is load in a bunch of sqlite databases in the correct way and makes some transformations. I don't want this code exactly as it is, but I provide as a helpful framework. 

Ideally, we can create a function that we can import into either the pismo or vsfb project. Which files to load will depend on the project, but all the sqlite databases will be in the same format. I want the function to be modular, with the logic of which files to load to be handled separately, either in a different function or the cleaning script itself.


```python
direction_categories = [22.5, 45.0, 67.5, 90.0, 112.5, 135.0, 157.5,
                        180.0, 202.5, 225.0, 247.5, 270.0, 292.5, 315.0, 337.5, 360.0]

def load_wind_data(folder_path):
    s3db_file_paths = glob.glob(os.path.join(folder_path, "*.s3db"))

    df_list = []

    for s3db_file_path in tqdm(s3db_file_paths, desc="Loading wind data"):
        sensor = os.path.splitext(os.path.basename(s3db_file_path))[0]

        conn = sqlite3.connect(s3db_file_path)

        df = pd.read_sql_query("SELECT * FROM Wind", conn,
                               dtype={"speed": float, "gust": float, "direction": int, "time": str})

        df['speed_mph'] = round(df['speed'] * 2.23694, 1)
        df['gust_mph'] = round(df['gust'] * 2.23694, 1)

        df["sensor"] = sensor

        df_list.append(df)

        conn.close()

    combined_df = pd.concat(df_list)

    # Meaningless info once db's are combined.
    combined_df = combined_df.drop('id', axis=1)

    combined_df['time'] = pd.to_datetime(combined_df['time'])

    # Assigns a heading based on the 16 point resolution of the sensor.
    # Can't use direction directly as this is the averaged wind direction during the monitoring period.
    # A special case of rounding up to 360 is made here, as a 0 direction in the data indicates bad reading
    combined_df['direction_category'] = combined_df['direction'].apply(lambda x: min(
        direction_categories, key=lambda d: abs((d - x) % 360) if abs((d - x) % 360) <= 11.25 else abs((d - x) % 360 - 360)))

    return combined_df
```