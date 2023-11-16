#This file will be used to follow along in the vectorization video from coursera

#Imports
import numpy as np
import time

#Decorator Function
def timer(f):
    def wrapper(*args, **kwargs):
        st = time.time()
        func = f(*args, **kwargs)
        ft = time.time()
        print(f.__name__)
        tt = (ft - st) * 1000
        print('Total time:', tt, 'ms')
        return func
    return wrapper

#Vectorization Function
@timer
def vectorization_function(l1, l2):
    return np.dot(l1, l2)
    

@timer 
def for_loop(l1, l2):
    d = 0
    for i in range(1_000_000):
        d += l1[i] * l2[i]

#Main method
if __name__ == "__main__":
    a = np.random.rand(1_000_000)
    b = np.random.rand(1_000_000)

    vectorization_function(a, b)
    for_loop(a, b)