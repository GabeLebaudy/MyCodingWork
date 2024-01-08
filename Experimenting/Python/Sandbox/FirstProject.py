#This file will be used to receive an input file from the command line, and output it to another file with a certain name

#Imports
import os
import sys

#Helpers
class Variable:
    #Constructor
    def __init__(self, name, data):
        self.name = name
        self.data = data
        
    #Getters
    def getName(self):
        return self.name
    
    def getData(self):
        return self.data

#Main Method
if __name__ == "__main__":
    #Create Main Storage
    var_storage = []
    
    #Checks to make sure that the user enters correct inputs
    if len(sys.argv) != 3: #Correct number of arguments
        print('Error: Exactly 2 arguments are needed for this script.')
        sys.exit()
    
    #Ensures input file is correct
    if not os.path.exists(sys.argv[1]):
        print('Error: Input file not found.')
        sys.exit()
    
    #Ensures input file is a txt file
    if sys.argv[1][-4:] != '.txt':
        print('Error: Input file must be a .txt file')
        sys.exit()
        
    #Ensures output file is in the csv format
    if sys.argv[2][-4:] != '.csv':
        print('Error: Output file must be in the .csv format')
        sys.exit()
    
    #Read Data from file
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)): 
            if not lines[i].rstrip():
                continue
            
            if ('=' not in lines[i]) or ('[' not in lines[i]) or (']' not in lines[i]):
                print('Formatting error on line {} in the source file.\nData from this line will not be included in the output file.'.format(i + 1))
                continue
            
            name_and_data = lines[i].split('=')
            name = name_and_data[0].strip()
            data = name_and_data[1][2:-3]
            data = data.split(',')
            var = Variable(name, data)
            var_storage.append(var)
    
    #Write Results to File
    with open(sys.argv[2], 'w') as f:
        f.write('var_name,array_no,array_val\n')
        for var in var_storage:
            var_name, var_data = var.getName(), var.getData()
            for i in range(len(var_data)):
                str_format = '{},{},{}\n'.format(var_name, i + 1, var_data[i].strip())
                f.write(str_format)
        