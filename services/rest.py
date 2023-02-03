## CSCI6010
## Team Dynasty
## Chase Moore, Denise Bruce, Adam Wade Foster

## Purple Air -> https://community.purpleair.com/t/making-api-calls-with-the-purpleair-api/180
## Air Now -> https://fire.airnow.gov/

import requests

def getPurpleAirSensorData(sensor_index):

    # Define the API endpoint for retrieving the X-API-Key
    key_url = "https://api.purpleair.com/v1/keys"
    api_key = ""
    key_data = ""

    # Make the GET request to the API to retrieve the X-API-Key
    key_response = requests.get(key_url)

    # We successfully generated a token
    if key_response.status_code == 200:
        key_data = key_response.json()
        api_key = key_data['key']
    
    print("key -> " + str(api_key))
    # Define the API endpoint
    data_url =  "https://api.purpleair.com/v1/sensors/:" + sensor_index

    

    # Define the headers with the X-API-Key parameter
    headers = {
        "X-API-Key": api_key
    }

    # Make the GET request to the API and include the headers
    data_response = requests.get(data_url, headers=headers)

    # Check if the request was successful
    if data_response.status_code == 200:
        # Parse the JSON data from the response
        data = data_response.json()

        # Extract the desired information from the data
        for sensor in data['results']:
            print("Sensor index:", sensor['sensor_index'])
            print("Sensor Icon:", sensor['icon'])
            print("Sensor Name:", sensor['name'])
            print("Location:", sensor['location_type'])
            print("---")
    else:
        # Print an error message if the request was unsuccessful
        print("Failed to retrieve data. Response code:", data_response.status_code)



##  MAIN
sensor_index = '31619'
getPurpleAirSensorData(sensor_index)