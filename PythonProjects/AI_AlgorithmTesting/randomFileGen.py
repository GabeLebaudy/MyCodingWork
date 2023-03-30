#This file will be used to generate a file with random values between 0-100, and 0-10
#I want it to generate some sort of trend, so as the file goes on the results will be tweaked a little bit to trend upward as x increases y increases etc.
#0-10, will be x and 0 - 100 will be y

#Import modules
import random
import os

if __name__ == "__main__":
    #1. Open a new file to write to, start by writing the first line of x and y first
    firstLineString = "x,y"
    myFile = open(r"c:\Users\Gabe\Documents\GitHub\MyCodingWork\PythonProjects\AI_AlgorithmTesting\results.csv", "w")
    myFile.write(firstLineString)
    #2. Populate file with numbers, randomly generated. Want to add linear trend to data points
    x = 0
    y = 0
    x_max = 10
    y_max = 50
    numIterations = 50
    
    for i in range(0, numIterations):
        x = random.randint(int(x), int(x_max))
        y = random.randint(int(y), int(y_max))
        myFile.write('\n' + str(x) + ',' + str(y))
        x = (10/ numIterations) * i
        y = (50/ numIterations) * i
        y_max += (50/numIterations)
    myFile.close()

