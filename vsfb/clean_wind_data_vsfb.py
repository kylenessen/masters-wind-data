# %%
from scripts.wind_data_loader import *
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# %%
deployments = pd.read_csv('deployments2023.csv')
# %%
