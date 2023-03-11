## CSCI6010
## Team Dynasty
## Chase Moore, Denise Bruce, Adam Wade Foster

## Purple Air -> https://community.purpleair.com/t/making-api-calls-with-the-purpleair-api/180
## Air Now -> https://fire.airnow.gov/

import requests
import pandas as pd
import plotly.express as px


def inputData(inputDictionaryADB):
    sensor_index = list(inputDictionaryADB.values())
    return sensor_index


def getPurpleAirSensorData(sensor_index, api_key):
    # Define the API endpoint for retrieving the sensor data
    data_url = 'https://api.purpleair.com/v1/sensors/' + str(sensor_index)
    headers = {
        "X-API-Key": api_key
    }

    # Make the GET request to the API to retrieve the sensor data
    response = requests.get(data_url, headers=headers)

    # We successfully retrieved the sensor data
    if response.status_code == 200:
        data = response.json()
        return data['sensor']['stats']['pm2.5']

def getAirNowSensorData(api_key):

    # specify the latitude and longitude of Raleigh, NC
    lat = 35.7796
    lon = -78.6382

    # make the API request
    url = f'https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={lat}&longitude={lon}&distance=25&API_KEY={api_key}&parameter=PM2.5'
    response = requests.get(url)
    if response.status_code == 200:
        # parse the JSON response
        data = response.json()
        # print the data
        print(data)
    


##  MAIN
api_key_purple = "B276397E-A658-11ED-B6F4-42010A800007"
api_key_air = "625E165E-03E8-4317-B7F7-1BDB0290A448"
getAirNowSensorData(api_key_air)

# ADB_This will be an input on website rather than a dictionary.  For now it will be hard coded
inputDictionaryADB = {"NASA_AQCS_45":104950, "NASA_AQCS_36":47535, "NASA_AQCS_21":47497, "NASA_AQCS_87":47633,
                      "NASA_AQCS_17":47489, "NASA_AQCS_12":47479, "NASA_AQCS_19":47493, "NASA_AQCS_7":47469,
                      "NASA_AQCS_91":29257, "NASA_AQCS_55":47573}
input_sensors = inputData(inputDictionaryADB)

# Retrieve sensor data and store it in a dataframe
sensor_data = []
for sensor in input_sensors:
    pm25_value = getPurpleAirSensorData(sensor, api_key_purple)
    sensor_data.append({'Sensor ID': sensor, 'PM2.5 Value': pm25_value})

df = pd.DataFrame(sensor_data)
print(df)
# Display the data using a plotly scatter plot
fig = px.scatter(df, x='Sensor ID', y='PM2.5 Value', title='PurpleAir PM 2.5 Sensor Data')
fig.show()



"""Graveyard
def getAllPurpleAirSensorData(api_key):
    # Define the API endpoint for retrieving sensor metadata
    metadata_url = 'https://api.purpleair.com/v1/sensors?location=Raleigh,NC&location_type=0&fields=sensor_index,name,latitude,longitude,pm2.5'

    headers = {
        "X-API-Key": api_key
    }

    # Make the GET request to the API and include the headers
    response = requests.get(metadata_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Iterate through the list of sensors and retrieve the data for each sensor
        for sensor in data['data']:
            getPurpleAirSensorData(sensor[0], api_key)
    else:
        # Print an error message if the request was unsuccessful
        print("Failed to retrieve sensor metadata. Response code:", response.status_code)

"""