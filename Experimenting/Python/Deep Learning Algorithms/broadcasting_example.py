#This file will be used to demonstrate the broadcasting technique used to simplify code

#Imports
import numpy as np

#Main Method
if __name__ == "__main__":
    #Create sample matrix
    A = np.array(
        [
            [56, 0, 4.4, 68],
            [1.2, 104, 52, 8],
            [1.8, 135, 99, 0.9],
        ]
    )
    print(A)
    print()

    #Sum vertically, and store result in an array
    calories = A.sum(axis=0)
    print(calories)
    print()

    #Get a matrix containing the percentage of total calories each row takes up.
    pm = 100*(A / calories.reshape(1, 4)) #The reshape function turns calories into a 1x4 matrix(It's already a 1x4 matrix, but this is just a demonstration)
    print(pm)
    print()