In vsfb/clean_wind_data_vsfb.py, I would like you to load in the sqlite data for the wind meters that occur in the deployments dataframe. I've copied the head of that dataframe below. I'm looking for wind_meter_name. 


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fid</th>
      <th>camera_name</th>
      <th>wind_meter_name</th>
      <th>Deployed_time</th>
      <th>Recovered_time</th>
      <th>notes</th>
      <th>height_m</th>
      <th>horizontal_dist_to_cluster_m</th>
      <th>view_direction</th>
      <th>cluster_count</th>
      <th>deployment_id</th>
      <th>status</th>
      <th>photo_interval_min</th>
      <th>monarchs_present</th>
      <th>youtube_url</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>ECHO</td>
      <td>NaN</td>
      <td>2023/11/19 15:40:01.032</td>
      <td>2023/12/03 08:55:00</td>
      <td>Makeshift camera to catch butterflies during l...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>30</td>
      <td>NaN</td>
      <td>SC3</td>
      <td>Complete</td>
      <td>10</td>
      <td>True</td>
      <td>NaN</td>
      <td>34.631341</td>
      <td>-120.618064</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>NOVA</td>
      <td>OakTrust</td>
      <td>2023/12/03 11:20:00.603</td>
      <td>2023/12/20 12:20:00.555</td>
      <td>Not much activity when setting up, but easy sp...</td>
      <td>6.8</td>
      <td>5.0</td>
      <td>280</td>
      <td>10.0</td>
      <td>SLC6_1</td>
      <td>Complete</td>
      <td>10</td>
      <td>False</td>
      <td>https://youtu.be/XnDkDjUaAwk</td>
      <td>34.584678</td>
      <td>-120.628789</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>WASP</td>
      <td>MoonTide</td>
      <td>2023/12/03 13:02:00.913</td>
      <td>2024/01/05 13:02:00.942</td>
      <td>Hoping butterflies show up</td>
      <td>7.5</td>
      <td>7.6</td>
      <td>20</td>
      <td>0.0</td>
      <td>SLC6_2</td>
      <td>Complete</td>
      <td>10</td>
      <td>True</td>
      <td>https://youtu.be/r8f3oCAFK9k</td>
      <td>34.584490</td>
      <td>-120.629131</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>ZEST</td>
      <td>StarDust</td>
      <td>2023/12/03 14:30:00.855</td>
      <td>2024/01/05 14:30:00.003</td>
      <td>Guess on count. Check end time</td>
      <td>5.6</td>
      <td>6.3</td>
      <td>335</td>
      <td>750.0</td>
      <td>SC4</td>
      <td>Complete</td>
      <td>10</td>
      <td>True</td>
      <td>https://youtu.be/RW91J3HMm_4</td>
      <td>34.631283</td>
      <td>-120.618134</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>APEX</td>
      <td>PugSnore</td>
      <td>2023/12/03 16:30:00.183</td>
      <td>2024/01/31 19:40:00.314</td>
      <td>No monarchs here, but usually a reliable site....</td>
      <td>8.3</td>
      <td>5.7</td>
      <td>320</td>
      <td>0.0</td>
      <td>SC5</td>
      <td>Complete</td>
      <td>10</td>
      <td>False</td>
      <td>https://youtu.be/1LG6O86pPvU</td>
      <td>34.631501</td>
      <td>-120.617561</td>
    </tr>
  </tbody>
</table>
</div>