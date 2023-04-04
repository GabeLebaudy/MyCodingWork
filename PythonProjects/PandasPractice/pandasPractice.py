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
    #print(pokemonData.columns)
    
    #Print out entire columns
    #print(pokemonData[['Name', 'Type 1', 'HP']] [0:5]) #Second brackets are similar to string slicing 'start index:end index' 'x:' = x to end ':x' = start to x
    
    #Print out entire row
    print(pokemonData.iloc[1:4]) #Prints out second row to fourth row similar index system to printing columns
    
    #Print out specific index, (Row, Column)
    print(pokemonData.iloc[2, 1]) #Row 3 (index 2) Column 2 (index 1)
    
    #Loop through dataset row by row
    '''
    for index, row in pokemonData.iterrows():
        print(index, row['Name'])
    '''
    
    #Print all rows with Type 1 column having a value of Fire
    #print(pokemonData.loc[pokemonData['Type 1'] == 'Fire'])
    
    #Print Features of data. I.E. Mean Standard Deviation Etc.
    #print(pokemonData.describe())
    
    #Sort Data Entries by Alphabetical order of name
    #print(pokemonData.sort_values(['Type 1', 'HP'], ascending=[1,0])) #1 means that Type 1 will be sorted in ascending order and 0 means it will be sorted in descending order
    
    #Make New column thats calculated based on other values
    #pokemonData['Total_Stats'] = pokemonData['HP'] + pokemonData['Attack'] + pokemonData['Defense'] + pokemonData['Sp. Atk'] + pokemonData['Sp. Def'] + pokemonData['Speed']
    #print(pokemonData.head(3))
    
    #Drop column from dataset
    #df = pokemonData.drop(columns=['Total_Stats'])
    #print(df.head(3))
    
    #Another way to add total stats column
    #df['Total_Stats'] = df.iloc[:, 4:10].sum(axis=1)
    #print(df.head(3))
    
    #Moves the total stats column to the middle
    #ols = list(df.columns)
    #df = df[cols[0:4] + [cols[-1]] + cols[4:12]]
    
    #print(df.head(3))
     