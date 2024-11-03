#Main script for gather and parsing data

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

#Get the last used link
def getLastUrl():
    path = os.path.join(os.path.dirname(__file__), "link.txt")
    with open(path, "r") as f:
        link = f.readline()

    return link

#update the link file
def updateLastLink(url):
    path = os.path.join(os.path.dirname(__file__), "link.txt")
    with open(path, "w") as f:
        f.write(url)

#Return a list of items given the properties dictionary
def parseDictionary(info):
    dict_items = []
    for key in info:
        if key == "timestamp":
            time = info[key]
            time_items = time.split("T")
            clock_time = time_items[1].split("+")
            time_to_add = time_items[0] + " " + clock_time[0]
            dict_items.append(time_to_add)

        if key in DESIRED_VALUES:
            cur_item = info[key]
            if (cur_item["value"] == None):
                dict_items.append("null")

            else:
                dict_items.append(str(cur_item["value"]))

            dict_items.append(cur_item["qualityControl"])
    
    return dict_items

#Main
if __name__ == "__main__":
    argc = len(sys.argv)

    if argc == 1:
        print("Usage: weather.py csv_output link(optional)")
        sys.exit()
    elif argc == 2:
        output_name = sys.argv[1]
        weather_url = getLastUrl()
    else:
        output_name = sys.argv[1]
        weather_url = sys.argv[2]
        
    #Create output file if it doesn't exist.
    output_path = os.path.join(os.path.dirname(__file__), output_name)
    if not os.path.exists(output_path):
        prepOutput(output_path)
    
    response = requests.get(weather_url)
    content = response.json()

    #The webpages with different amounts of entries have different json structures, and need to be handled differently. 
    if "properties" in content:
        items = parseDictionary(content["properties"])
        addRow(output_path, items)
    else:
        features = content["features"]
        
        for i in range(len(features)):
            row_items = parseDictionary(features[i]["properties"])
            addRow(output_path, row_items)

    updateLastLink(weather_url)