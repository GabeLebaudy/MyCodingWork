#Another way to try linear regression model.

#Import modules
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

#Main Script
if __name__ == "__main__":
    #noiseVal = 10 #Amount of variation in data
    
    #Populate X, Y data
    xVal = 4 * np.random.rand(100, 1) - 2
    yVal = 4 + 2 * xVal + 5 * (xVal ** 2) + np.random.randn(100, 1) # Y is sort of a function of x (4 + 2x + 5x^2 + 0-100) = 5x^2 + 2x + 4 + 0-100 (poloynomial)
    
    poly_features = PolynomialFeatures(degree = 2, include_bias=False)#Degree = (Similar to order of taylor poloynomial)
    X_poly = poly_features.fit_transform(xVal)

    #Fit linear regression model over the X, Y data points
    reg = LinearRegression()
    reg.fit(X_poly, yVal)
    
    X_Vals = np.linspace(-2, 2, 100).reshape(-1, 1) #Linear
    X_Vals_poly = poly_features.transform(X_Vals) #Polonomial Values
    
    Y_Vals = reg.predict(X_Vals_poly)
    
    #Use matplotlib to plot the data
    plt.scatter(xVal, yVal)
    plt.plot(X_Vals, Y_Vals, color="r")
    plt.show()