#Testing new stuff

#Imports
import os
import requests
import sys

#NOTE: Not included is maxTemperatureLast24hours, and minTemperatureLast24Hours since there's no quality control value. 
#NOTE: All values here are in the form as in the json file.
HEADER_CONTENT = [
                "timestamp", "temperature value", "temperature qualityControl", "dewpoint value", "dewpoint qualityControl", 
                  "windDirection value", "windDirection qualityControl", "windSpeed value", "windSpeed qualityControl", 
                  "windGust value", "windGust qualityControl", "barometricPressure value", "barometricPressure qualityControl",
                  "seaLevelPressure value", "seaLevelPressure qualityControl", "visibility value", "visibility qualityControl", 
                  "precipitationLastHour value", "precipitationLastHour qualityControl", "precipitationLast3Hours value", "precipitationLast3Hours qualityControl",
                  "precipitationLast6Hours value", "precipitationLast6Hours qualityControl", "relativeHumidity value", "relativeHumidity qualityControl",
                  "windChill value", "windChill qualityControl", "heatIndex value", "heatIndex qualityControl"
                ] 

DESIRED_VALUES = [
                "temperature", "dewpoint", "windDirection", "windSpeed", "windGust", "barometricPressure", "seaLevelPressure", 
                  "visibility", "precipitationLastHour", "precipitationLast3Hours", "precipitationLast6Hours", "relativeHumidity",
                  "windChill", "heatIndex"
                ]

#Populate CSV with the header row if needed.
def prepOutput(path):
    with open(path, 'w') as f:
        for i in range(len(HEADER_CONTENT) - 1):
            f.write("{},".format(HEADER_CONTENT[i]))

        f.write("{}\n".format(HEADER_CONTENT[-1]))

#Add row to csv file
def addRow(path, items):
    with open(path, 'a') as f:
        for i in range(len(items) - 1):
            f.write("{},".format(items[i]))
        
        f.write("{}\n".format(items[-1]))

#Main
if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "new_output.csv")
    if not os.path.exists(path):
        prepOutput(path)
    
    response = requests.get("https://api.weather.gov/stations/KRIV/observations?limit=200")
    content = response.json()
    for key in content:
        print(key)