#This file will be used to try out the functionality of a decorators

import time
import numpy as np

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

#Main Method
if __name__ == "__main__":
    curList = np.zeros(100000)
    curList[-1] = 100
    print(linearSearch(curList, 100))