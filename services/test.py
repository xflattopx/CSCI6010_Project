import requests
import pandas as pd
import plotly.express as px
import pytz 
from datetime import datetime, timedelta
import json 

def getAirNowSensorData(api_key):
    #

    url = 'https://www.airnowapi.org/aq/data/?startDate=2023-03-3T18&endDate=2023-04-01T19&parameters=PM25&BBOX=-78.647643,35.731814,-78.460876,35.941117&dataType=A&format=application/json&verbose=1&monitorType=0&includerawconcentrations=1&API_KEY='+ str(api_key)     # make the API request
    
    response = requests.get(url)

    if response.status_code == 200:

#         # parse the JSON response
        data_an = response.json()
        df = pd.json_normalize(data_an)
        

# reset the index to make the "UTC" column a regular column again
        df = df.reset_index()

# drop the rows with missing values (i.e. the first 23 rows)
        df = df.dropna()
# resample the dataframe by 24 hour intervals and compute the average of PM2.5 values
        
        print(df)
        

airnow_api =  '1A90A9DF-368D-45C1-BF6B-14701DC449D1'

getAirNowSensorData(airnow_api)

