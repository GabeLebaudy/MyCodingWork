#This file will be used to test out unit tests in python. This file will be the functions to be tested

from math import pi

def getArea(r):
    if type(r) not in [int, float]:
        raise TypeError("The radius must be a non-negative real number.")
    
    if r < 0:
        raise ValueError("Radius cannot be a negative number")
    
    return pi * (r**2)
