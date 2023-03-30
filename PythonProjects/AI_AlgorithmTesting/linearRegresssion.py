#This file will be the main script for the linear regression algorithm

#import modules
import pandas as pd
import matplotlib.pyplot as plt
import os

#Define functions

#Loss function: Not needed just for math reference
def loss_function(m, b, dataPoints):
    totalError = 0
    for i in range(0, len(dataPoints)):
        xVal = dataPoints.iloc[i].x
        yVal = dataPoints.iloc[i].y
        totalError += (yVal - (m * xVal + b)) ** 2
    totalError /= float(len(dataPoints))
    return totalError


#Derivative of function above
def gradient_descent(m_now, b_now, dataPoints, L):
    m_gradient = 0
    b_gradient = 0
    n = len(dataPoints)
    for i in range(n):
        x = dataPoints.iloc[i].x
        y = dataPoints.iloc[i].y
        m_gradient += -(2/n) * x * (y - (m_now * x + b_now))
        b_gradient += -(2/n) * (y - (m_now * x + b_now))
        
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
    m = 0
    b = 0
    L = 0.0001
    Iterations = 1000
    for i in range(Iterations):
        if i % 50 == 0:
            print(f"Iteration: {i}")
        m , b = gradient_descent(m, b, randomData, L)
    
    print(m, b)
    
    plt.scatter(randomData.x, randomData.y, color="red")
    plt.plot(list(range(0, 15)), [m * x + b for x in range(0, 15)], color="black")
    plt.show()
    
    
    
    
    
    
    
    