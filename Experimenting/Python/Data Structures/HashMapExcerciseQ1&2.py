#This file will be used for the hash map data structure exercise

#Imports
import os

if __name__ == "__main__":
    #Set up
    weatherFilePath = os.path.join(os.path.dirname(__file__), 'dataFiles/nyc_weather.csv')
    with open(weatherFilePath, 'r') as file:
        data = file.readlines()

    data = data[1:]

    weatherDict = {}
    for entry in data:
        entry = entry.rstrip()
        items = entry.split(',')
        weatherDict[items[0]] = int(items[1])
    
    #Question 1.
    print('Q1')
    # i. Find average temperature in first week of January
    totalTemp = 0
    for item in weatherDict:
        days = item.split(' ')
        if int(days[1]) < 8:
            totalTemp += weatherDict[item]

    totalTemp /= 7
    print("The average temperature in the first week of January was %.2f degrees." % totalTemp)

    # ii.
    maxTemp = 0
    for item in weatherDict:
        if weatherDict[item] > maxTemp:
            maxTemp = weatherDict[item]
    
    print("The maximum temperature during the first 10 days of January was %d degrees." % maxTemp)
    
    print('\nQ2')
    #Question 2.

    # i.
    print("The temperature on January 9th was %d degrees." % weatherDict['Jan 9'])

    # ii.
    print("The temperature on January 4th was %d degrees." % weatherDict['Jan 4'])
    