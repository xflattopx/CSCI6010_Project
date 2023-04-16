import requests
import pandas as pd
import plotly.express as px
import pytz 
from datetime import datetime, timedelta
import json 

def convert_timestamp_to_est(timestamp):
    converted_timestamp = int(timestamp)  # convert to integer
    # Convert timestamp to datetime object in UTC timezone
    utc_datetime = datetime.utcfromtimestamp(converted_timestamp)
    
    # Convert datetime object to Eastern Standard Time timezone
    est_timezone = pytz.timezone('US/Eastern')
    est_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(est_timezone)
    
    # Update the JSON object with the converted timestamp
    converted_timestamp = est_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    return converted_timestamp


def getAirNowSensorData(api_key):
    #

    url = 'https://www.airnowapi.org/aq/data/?startDate=2022-01-01T00&endDate=2022-12-31T23&parameters=PM25&BBOX=-78.647643,35.731814,-78.460876,35.941117&dataType=A&format=application/json&verbose=1&monitorType=0&includerawconcentrations=1&API_KEY='+ str(api_key)     # make the API request
    
    response = requests.get(url)

    if response.status_code == 200:

#         # parse the JSON response
        data_an = response.json()
        df = pd.json_normalize(data_an)
        

# reset the index to make the "UTC" column a regular column again
        df = df.reset_index()

# drop the rows with missing values (i.e. the first 23 rows)
        df = df.drop(['index', 'Latitude', 'Longitude', 'Parameter', 'Unit',
        'AQI', 'Category', 'SiteName', 'AgencyName',
       'FullAQSCode', 'IntlAQSCode'], axis = 1)
        df['Humidity']= 0
        df[['Date', 'Time']] = df['UTC'].str.split('T', expand=True)
        df = df.drop(df[df['RawConcentration'] == -999.0].index)
        #df["Time"] = df['Time'].apply(pd.to_numeric)
        df_mean = df.groupby('Date')['RawConcentration'].mean().reset_index()
        df.to_csv('raw')
# return the resulting dataframe
        return(df_mean)


       
        

airnow_api =  '1A90A9DF-368D-45C1-BF6B-14701DC449D1'

data = getAirNowSensorData(airnow_api)
print(data)


