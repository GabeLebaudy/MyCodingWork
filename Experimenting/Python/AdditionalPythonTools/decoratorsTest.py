#This file will be used to try out the functionality of a decorators

import time
import numpy as np
from functools import wraps
from functools import cache

#Decorator Function
def timer(f):
    #Wrapper Method
    def wrapper(*args, **kwargs):
        #Runs code surrounding the method passed in, in this case taking a start and end time, and calls the function (f)
        startTime = time.time()
        result = f(*args, **kwargs)
        stopTime = time.time()
        totalTime = stopTime - startTime
        print("Total Time:", totalTime)
        #Returns result of function passed in
        return result
    return wrapper

#Prime Factorization Function
@timer
def linearSearch(list, n):
    index = 0
    for i in range(len(list)):
        if n == list[i]:
            return i
    
    return -1

#Wraps Method
def doNothing(f):
    @wraps(f)
    def inner(*args, **kwargs):
        return (f*args, f**kwargs)
    return inner

#Wraps Example
@doNothing
def sampleFunction():
    """A function that shows the details about it"""

#Fibonacci Sequence
@cache
def fib(n):
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"{n} is not a positive integer")
    
    if n == 1 or n == 2:
        return 1
    
    else:
        return fib(n - 1) + fib(n - 2)

@timer
def globFib(n):
    return fib(n)

#Main Method
if __name__ == "__main__":
    curList = np.zeros(100000)
    curList[-1] = 100
    #print(linearSearch(curList, 100))

    print()
    print(sampleFunction.__name__)
    print(sampleFunction.__doc__)

    print()
    print(globFib(100))