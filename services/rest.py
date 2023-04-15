
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
#*Send all retrieved data to a dataframe with columns for time stamp, PM2.5 concentration, and Humidity 
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
import json 


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


def getPurpleAirSensorData(sensor_index, api_key): #start_timestamp
    # Define the API endpoint for retrieving the sensor data
    data_url =  'https://api.purpleair.com/v1/sensors/'+ str(sensor_index) +'/history?start_timestamp=1641013200&end_timestamp=1672549140&average=1440&fields=humidity%2Cpm2.5_atm'
    headers = {
        "X-API-Key": api_key
    }
    # Make the GET request to the API to retrieve the sensor data
    response = requests.get(data_url, headers=headers)

    # We successfully retrieved the sensor data
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['data'], columns=['Time', 'Humidity', 'PM25'])
        df['sensor_index'] = sensor_index
        df['Time'] = df['Time'].apply(convert_timestamp_to_est)
        df[['Date', 'Time1']] = df['Time'].str.split(' ', expand=True)
        df = df.sort_values('Date')
        #print(df)
        return df

def plotSensorData(sensor_data):
    # Concatenate all dataframes into one
    df = pd.concat(sensor_data, ignore_index=True)
    # Add a new column to identify which sensor each row belongs to
    sensor_col = [f"Sensor {i+1}" for i in range(len(sensor_data)) for _ in range(len(sensor_data[i]))]
    sensor_index_col = [sensor_data[i]['sensor_index'][0] for i in range(len(sensor_data)) for _ in range(len(sensor_data[i]))]
    df['Sensor'] = sensor_col
    df['Sensor Index'] = sensor_index_col
    # Plot the data
    fig = px.line(df, x='Date', y='PM25', color='Sensor', title='PurpleAir PM 2.5 Sensor Data')
    fig.show()

# Define the sensor indices
sensor_indices = [104950, 47535,47497,47633,47489,47479,47493,47469,29257,47573] #purple air sensor indicies.
api_key_purple = "B276397E-A658-11ED-B6F4-42010A800007"
# Retrieve sensor data and store it in a list of dataframes
sensor_data = []
for sensor in sensor_indices:
    df = getPurpleAirSensorData(sensor, api_key_purple)
    sensor_data.append(df)

# Plot the data
plotSensorData(sensor_data)





#User start date converted from month day year 
# def user_start_time( ):
#     start_year= int(input ("Enter the Start year: ")) 
#     start_month= int(input("Enter Start Month: "))
#     start_day= int(input("Enter Start Day: "))
    
#     dt = datetime(start_year, start_month, start_day, 0, 0, 0)
#     epoch_time = int(dt.timestamp())
#     return (epoch_time)
   

    
    

# def get_start_time(time_stamp):
#     # Convert time_stamp to a datetime object
#     dt = datetime.fromtimestamp(time_stamp)

#     # Subtract 24 hours from the datetime object
#     dt_24hrs_ago = dt - timedelta(hours=24)

#      # Convert the datetime object back to a time stamp
#     time_stamp_24hrs_ago = int(dt_24hrs_ago.timestamp())

#     return time_stamp_24hrs_ago





# def inputData(inputDictionaryADB):
#     sensor_index = list(inputDictionaryADB.values())
#     return sensor_index


# def getPurpleAirSensorData(sensor_index, api_key, ): #start_timestamp
#     # Define the API endpoint for retrieving the sensor data
#     data_url =  'https://api.purpleair.com/v1/sensors/'+ str(sensor_index) +'/history?start_timestamp=1641013200&end_timestamp=1672549140&average=1440&fields=humidity%2Cpm2.5_atm'
#     ##'https://api.purpleair.com/v1/sensors/history?start_timestamp=1646189608&fields=humidity%2Cpm2.5_atm'+ str(sensor_index) + 
#     headers = {
#         "X-API-Key": api_key
#     }
#     # Make the GET request to the API to retrieve the sensor data
#     response = requests.get(data_url, headers=headers)


#     # We successfully retrieved the sensor data
#     if response.status_code == 200:
#         data = response.json()
        
#         keys = data.keys()
#         epoch_ts = []
#         humidity = []
#         pm25_atm = []
#         pm = data['sensor_index']
#         count = 0
#         for c1 in data['data'][0]:
#             #print(count)
#             if(count == 0):
#                 epoch_ts.append(c1)
#             elif(count == 1):
#                 humidity.append(c1)
#             elif(count == 2):
#                 pm25_atm.append(c1)
#             count += 1
#         count = 0
#         for c2 in data['data'][1]:
#             if(count == 0):
#                 epoch_ts.append(c2)
#             elif(count == 1):
#                 humidity.append(c2)
#             elif(count == 2):
#                 pm25_atm.append(c2)
#             count += 1
#         count = 0
#         for c3 in data['data'][2]:
#             if(count == 0):
#                 epoch_ts.append(c3)
#             elif(count == 1):
#                 humidity.append(c3)
#             elif(count == 2):
#                 pm25_atm.append(c3)
#             count += 1
#         start_time = get_start_time(data['start_timestamp'])
#         #print(keys)
#         #print(type(data['data']))
#         return data


# def getAirNowSensorData(api_key):

#     # specify the latitude and longitude of Raleigh, NC
#     lat = 35.7796
#     lon = -78.6382

#     # make the API request
#     url = 'https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={lat}&longitude={lon}&distance=25&API_KEY={api_key}&parameter=PM2.5'
#     url2 = 'https://www.airnowapi.org/aq/data/?startDate=2022-01-01T00&endDate=2022-12-31T01&parameters=PM25&BBOX=-78.931785,35.588992,-78.214927,36.052221&dataType=B&format=application/json&verbose=1&monitorType=0&includerawconcentrations=1&API_KEY=' + api_key
#     response = requests.get(url2)
#     print('in getAirNow ' + str(response))
#     if response.status_code == 200:

#         # parse the JSON response
#         data_an = response.json()
#         #print (data)
#         print(data_an)

    


# ##  MAIN
#api_key_purple = "B276397E-A658-11ED-B6F4-42010A800007"
# api_key_air = "625E165E-03E8-4317-B7F7-1BDB0290A448"
# getAirNowSensorData(api_key_air)


# #sensor = 104950
# # ADB_This will be an input on website rather than a dictionary.  For now it will be hard coded
# inputDictionaryADB = {"NASA_AQCS_45":104950, "NASA_AQCS_36":47535} #"NASA_AQCS_21":47497, "NASA_AQCS_87":47633,
#                     #    "NASA_AQCS_17":47489, "NASA_AQCS_12":47479, "NASA_AQCS_19":47493, "NASA_AQCS_7":47469,
#                     #    "NASA_AQCS_91":29257, "NASA_AQCS_55":47573}
# input_sensors = inputData(inputDictionaryADB)

# # Retrieve sensor data and store it in a dataframe
# sensor_data = []

# #Can be any date and time in EPOCH time. 
# #starttime = user_start_time()
# day = 0
# #Increments through a given set of days.
# #while day
# for sensor in input_sensors:
            
#     pm25_value = getPurpleAirSensorData(sensor, api_key_purple) #starttime)
#     print (sensor)
#     data = pm25_value
#     data2 =data['data']
#     df = pd.DataFrame(data2, columns= ['Time', "Humidity", "PM25"])
#     df["Time"] = df["Time"].apply(convert_timestamp_to_est)
#     df[['Date', 'Time1']] = df['Time'].str.split(' ', expand= True)

#     df = df.sort_values('Date')  
#     print(df)
#     fig = px.line(df, x='Date' , y='PM25',  title= str(sensor)+ ' PurpleAir PM 2.5 Sensor Data')
#     #fig2 = px.scatter(df, x='Date' , y='PM25', title= str(sensor)+ ' PurpleAir PM 2.5 Sensor Data')

#     #fig.update_xaxes(range=[0, 366], tickmode='array', tickvals=[2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92, 95, 98, 101, 104, 107, 110, 113, 116, 119, 122, 125, 128, 131, 134, 137, 140, 143, 146, 149, 152, 155, 158, 161, 164, 167, 170, 173, 176, 179, 182, 185, 188, 191, 194, 197, 200, 203, 206, 209, 212, 215, 218, 221, 224, 227, 230, 233, 236, 239, 242, 245, 248, 251, 254, 257, 260, 263, 266, 269, 272, 275, 278, 281, 284, 287, 290, 293, 296, 299, 302, 305, 308, 311, 314, 317, 320, 323, 326, 329, 332, 335, 338, 341, 344, 347, 350, 353, 356, 359, 362, 365])
#     fig.show()
    #fig2.show()

    #print(df.head(365)) 


            #if (len(pm25_value[1])!= 0):
                #print (pm25_value [1][0])
                #sensor_data.append({ 
                #'sensor_index': sensor,
                #'Epoch_Time_Stamp': (pm25_value[1]),
                #'Humidity': pm25_value[2],
                #'PM2.5': pm25_value[3],
                #'start_time': convert_timestamp_to_est(pm25_value[4])})
                #print(pm25_value[1] - pm25_value[2])
                #print(pm25_value)
            
     #starttime  += 3 * 24 * 60 * 60
     #day = day + 3

    #return pm, con, time_stamp, start_time
#thingy = []
#df = pd.DataFrame(sensor_data)
#df2 = df.explode(['Epoch_Time_Stamp', 'Humidity', "PM2.5"])
#df2["Epoch_Time_Stamp"] = df2["Epoch_Time_Stamp"].apply(convert_timestamp_to_est)
#print (df2)
# pm_25 = df['PM2.5']
# sTime = df['start_time']
# print(sTime)
# thingy = thingy.append({'pm_25': pm_25,'sTime': sTime})
# new_df = pd.DataFrame(thingy)
# Display the data using a plotly scatter plot


