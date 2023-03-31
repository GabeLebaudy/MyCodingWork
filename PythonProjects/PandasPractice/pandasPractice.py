#This file should have a standard reference for the pandas library
#This isn't a complete tutorial, just a overview of the library

#Import pandas module
import pandas as pd

#Main Script
if __name__ == "__main__":
    #Read data file and store it in object memory
    pokemonData = pd.read_csv(r"c:\Users\Gabe\Documents\GitHub\MyCodingWork\PythonProjects\PandasPractice\pokemon_data.csv")
    
    #Print first three rows of data
    print(pokemonData.head(3))
    
    #Print last three rows of data
    print(pokemonData.tail(3))
    
    '''
    How to import files from excel
    df = pd.read_excel(filename)
    Text files (Separated by tabs)
    df = pd.read_csv(filename, delimeter = "\t")
    '''    
    
    #Prints out the names of all the columns (Read headers)
    print(pokemonData.columns)
    
    #Print out entire columns
    print(pokemonData[['Name', 'Type 1', 'HP']] [0:5]) #Second brackets are similar to string slicing 'start index:end index' 'x:' = x to end ':x' = start to x
    
    #Print out entire row
    print(pokemonData.iloc[1:4]) #Prints out second row to fourth row similar index system to printing columns
    
    #Print out specific index, (Row, Column)
    print(pokemonData.iloc[2, 1]) #Row 3 (index 2) Column 2 (index 1)
    
    #Loop through dataset row by row
    for index, row in pokemonData.iterrows():
        print(index, row['Name'])
    