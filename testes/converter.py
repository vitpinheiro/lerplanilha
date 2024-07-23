import pandas as pd
from datetime import datetime


min_date= "2024-01-04 00:00:00"
min_date2= pd.to_datetime(min_date, format="%Y-%m-%d %H:%M:%S")
date_ini= "2024-01-03 00:00:00"
date_ini2= pd.to_datetime(date_ini, format="%Y-%m-%d %H:%M:%S")
date_fin= "2024-01-05 00:00:00"
date_fin2= pd.to_datetime(date_fin, format="%Y-%m-%d %H:%M:%S")

if (date_ini2 <= min_date2 and min_date2 <= date_fin2):
    print("true")
else:
    print("false")
        