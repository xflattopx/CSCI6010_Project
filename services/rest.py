## Team Dynasty
## Chase Moore, Denise Bruce, Adam Wade Foster

## Purple Air -> https://community.purpleair.com/t/making-api-calls-with-the-purpleair-api/180
## Air Now -> https://fire.airnow.gov/
## Sensor List: 
import requests

#Todo: Add in call to Open AQ for sensor list

def inputData(inputDictionaryADB):
    sensor_index = list(inputDictionaryADB.values())
    return sensor_index
    
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
 

    

def getAllPurpleAirSensorData(api_key,input):
    # Define the API endpoint for retrieving sensor metadata
    metadata_url = "https://api.purpleair.com/v1/sensors/47535/history?start_timestamp=1646189608&fields=humidity%2Cpm2.5_atm"
    headers = {
        "X-API-Key": api_key
    }

    # Make the GET request to the API and include the headers
    response = requests.get(metadata_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Iterate through the list of sensors and re
        # trieve the data for each sensor
        data = input
        for sensor in data:  
            getPurpleAirSensorData(sensor, api_key)
    else:
        # Print an error message if the request was unsuccessful
        print("Failed to retrieve sensor metadata. Response code:", response.status_code)

##  MAIN
api_key = "B276397E-A658-11ED-B6F4-42010A800007"

# ADB_This will be an input on website rather than a dictionary.  For now it will be hard coded
inputDictionaryADB = {"NASA_AQCS_45":104950, "NASA_AQCS_36":47535, "NASA_AQCS_21":47497, "NASA_AQCS_87":47633,
 "NASA_AQCS_17":47489, "NASA_AQCS_12":47479, "NASA_AQCS_19":47493, "NASA_AQCS_7":47469, "NASA_AQCS_91":29257, "NASA_AQCS_55":47573}
input = inputData(inputDictionaryADB)
getAllPurpleAirSensorData(api_key, input)
