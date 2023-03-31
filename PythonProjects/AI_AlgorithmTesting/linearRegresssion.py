#This file will be the main script for the linear regression algorithm

#import modules
import pandas as pd
import matplotlib.pyplot as plt
import os

#Define functions

#Loss function: Not needed just for math reference
def loss_function(m, b, dataPoints):
    #Initialize error var
    totalError = 0
    
    #Run for amount of dataPoints
    for i in range(0, len(dataPoints)):
        #Set x and y to values of current data point
        xVal = dataPoints.iloc[i].x
        yVal = dataPoints.iloc[i].y
        
        #Error is equal to actual yVal, subtracted by expected value squared to make all values positive
        totalError += (yVal - (m * xVal + b)) ** 2
    
    #Mean squared error is equal to total error divided by points    
    totalError /= float(len(dataPoints))
    return totalError


#Derivative of function above
def gradient_descent(m_now, b_now, dataPoints, L):
    #Set dE/dm and dE/db to 0, and n to number of points in dataSet
    m_gradient = 0
    b_gradient = 0
    n = len(dataPoints)
    
    #Run for how many points exist in database
    for i in range(n):
        #Set x and y to their values in each entry of the CSV file
        x = dataPoints.iloc[i].x
        y = dataPoints.iloc[i].y
        
        #Set dE/dm and dE/db to values based on current m and b, plus current x and y values
        m_gradient += -(2/n) * x * (y - (m_now * x + b_now)) 
        b_gradient += -(2/n) * (y - (m_now * x + b_now))
    
    #Move m and b in opposite direction of greatest ascent.   
    m = m_now - m_gradient * L
    b = b_now - b_gradient * L
    return m, b


#Main Script
if __name__ == "__main__":
    #Import data into the program
    randomData = pd.read_csv(r"c:\Users\Gabe\Documents\GitHub\MyCodingWork\PythonProjects\AI_AlgorithmTesting\results.csv")

    #Visualize the data
    '''
    plt.scatter(randomData.x, randomData.y)
    plt.show()
    '''
    #Run function many times and have the AI 'learn' over time
    m = 0 #Slope Value
    b = 0 #Y-intercept Value
    L = 0.0001 #Learning Rate: Larger numbers are faster but less accurate
    Iterations = 1000
    for i in range(Iterations): #AI to run function and improve m and b values each iteration
        if i % 50 == 0:
            print(f"Iteration: {i}")
        m , b = gradient_descent(m, b, randomData, L)
    
    #Print final m and b values
    print(m, b)
    
    #Visualize data with matplotlib
    plt.scatter(randomData.x, randomData.y, color="red")
    plt.plot(list(range(0, 15)), [m * x + b for x in range(0, 15)], color="black")
    plt.show()
    
    
    
    
    
    
    
    