## CSCI6010
## Team Dynasty
## Chase Moore, Denise Bruce, Adam Wade Foster

## Purple Air -> https://community.purpleair.com/t/making-api-calls-with-the-purpleair-api/180
## Air Now -> https://fire.airnow.gov/

import requests

def getPurpleAirSensorData(sensor_index, api_key):

  
    # Define the API endpoint for retrieving the X-API-Key
    key_url = 'https://api.purpleair.com/v1/sensors/'+ str(sensor_index)
    key_data = ""

    headers = {
        "X-API-Key": api_key
    }

    # Make the GET request to the API to retrieve the X-API-Key
    response = requests.get(key_url, headers = headers)
    
    # We successfully generated a token
    if response.status_code == 200:
        data = response.json()
        print("response: " + str(data))
    

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

##  MAIN
api_key = ""
getAllPurpleAirSensorData(api_key)