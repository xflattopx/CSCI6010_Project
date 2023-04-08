
#####
## CSCI6010
## Team Dynasty
## Chase Moore, Denise Bruce, Adam Wade Foster

## Purple Air -> https://community.purpleair.com/t/making-api-calls-with-the-purpleair-api/180
## Air Now -> https://fire.airnow.gov/

## Todo 4/6 
#*Make a loop to implement the new API end point for historical data.  
#*Convert the timestamp from EPOCH time
#*get 365 days of data for all purple air sensors
#Send all retrieved data to a dataframe with columns for time stamp, PM2.5 concentration, and Humidity 
#create new data column and adjudt PM2.5 using the EPA approved correction factor 
#plot adjusted data for a given time period 
#call EPA monitor data 
#convert to Dataframe 
#Plot EPA monitor Data 
#Compare EPA Monitor Data with PM2.5 and Plot.
#Show a regression analysis and something like MadGans or whatever. 

import requests
import pandas as pd
import plotly.express as px
import pytz 
from datetime import datetime, timedelta
import calendar
import json 
from json import json_normalize




#User start date converted from month day year 
def user_start_time( ):
    start_year= int(input ("Enter the Start year: ")) 
    start_month= int(input("Enter Start Month: "))
    start_day= int(input("Enter Start Day: "))
    
    dt = datetime(start_year, start_month, start_day, 0, 0, 0)
    epoch_time = int(dt.timestamp())
    return (epoch_time)
   

    
    

def get_start_time(time_stamp):
    # Convert time_stamp to a datetime object
    dt = datetime.fromtimestamp(time_stamp)

    # Subtract 24 hours from the datetime object
    dt_24hrs_ago = dt - timedelta(hours=24)

     # Convert the datetime object back to a time stamp
    time_stamp_24hrs_ago = int(dt_24hrs_ago.timestamp())

    return time_stamp_24hrs_ago

def convert_timestamp_to_est(timestamp):
    converted_timestamp = timestamp
    # Convert timestamp to datetime object in UTC timezone
    utc_datetime = datetime.utcfromtimestamp(converted_timestamp)
    
    # Convert datetime object to Eastern Standard Time timezone
    est_timezone = pytz.timezone('US/Eastern')
    est_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(est_timezone)
    
    # Update the JSON object with the converted timestamp
    converted_timestamp = est_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    return converted_timestamp



def inputData(inputDictionaryADB):
    sensor_index = list(inputDictionaryADB.values())
    return sensor_index


def getPurpleAirSensorData(sensor, api_key, start_timestamp):
    # Define the API endpoint for retrieving the sensor data
    data_url =  'https://api.purpleair.com/v1/sensors/' + str(sensor) + '/history?start_timestamp=' + str(start_timestamp) + '&fields=humidity%2Cpm2.5_atm'
    ##'https://api.purpleair.com/v1/sensors/history?start_timestamp=1646189608&fields=humidity%2Cpm2.5_atm'+ str(sensor_index) + 
    headers = {
        "X-API-Key": api_key
    }
    # Make the GET request to the API to retrieve the sensor data
    response = requests.get(data_url, headers=headers)

    # We successfully retrieved the sensor data
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data)
        return data

def getAirNowSensorData(api_key):

    # specify the latitude and longitude of Raleigh, NC
    lat = 35.7796
    lon = -78.6382

    # make the API request
    url = f'https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={lat}&longitude={lon}&distance=25&API_KEY={api_key}&parameter=PM2.5'
    url2 = f'https://www.airnowapi.org/aq/data/?startDate=2023-03-02T00&endDate=2023-03-22T01&parameters=PM25&BBOX=-78.931785,35.588992,-78.214927,36.052221&dataType=B&format=application/json&verbose=1&monitorType=0&includerawconcentrations=1&API_KEY=' + api_key
    response = requests.get(url2)
    if response.status_code == 200:
        # parse the JSON response
        print (data)
        #print(data)

    


##  MAIN
api_key_purple = "B276397E-A658-11ED-B6F4-42010A800007"
api_key_air = "625E165E-03E8-4317-B7F7-1BDB0290A448"
#getAirNowSensorData(api_key_air)


#sensor = 104950
# ADB_This will be an input on website rather than a dictionary.  For now it will be hard coded
inputDictionaryADB = {"NASA_AQCS_45":104950, "NASA_AQCS_36":47535, "NASA_AQCS_21":47497, "NASA_AQCS_87":47633,
                      "NASA_AQCS_17":47489, "NASA_AQCS_12":47479, "NASA_AQCS_19":47493, "NASA_AQCS_7":47469,
                      "NASA_AQCS_91":29257, "NASA_AQCS_55":47573}
input_sensors = inputData(inputDictionaryADB)

# Retrieve sensor data and store it in a dataframe
sensor_data = []
#Can be any date and time in EPOCH time. 
starttime = user_start_time()
day = 0
#Increase to 366 
while day < 7: 
     for sensor in input_sensors:
            print(starttime)
            data = getPurpleAirSensorData(sensor, api_key_purple, starttime)
            #df = pd.read_json(data, orient ='index')
            print(df.head())
     starttime  += 3 * 24 * 60 * 60
     day = day + 3

    
       
        #'time_stamp': convert_timestamp_to_est(pm25_value[1]), 
        #start_time': convert_timestamp_to_est(pm25_value[2])})
        #print(pm25_value[1] - pm25_value[2])
        #print(pm25_value)
   
#df = pd.DataFrame(sensor_data)
#print(df)
# Display the data using a plotly scatter plot
#fig = px.line(df, x=time_stamp, y='PM2.5 Value', title='PurpleAir PM 2.5 Sensor Data')
#fig.show()


