#This file will be used for the has map exercise 3 and 4

#Imports
import os

#Hash map class
class HashMap:
    #Constructor
    def __init__(self):
        self.MAX = 10
        self.hm = [None for i in range(self.MAX)]

    #Hash Function
    def hashValue(self, key):
        totalVal = 0
        for char in key:
            totalVal += ord(char)
        
        return totalVal % 10

    #Set Item
    def __setitem__(self, key, val):
        bucket = self.hashValue(key)
        
        #Bucket is Empty
        if self.hm[bucket] is None:
            self.hm[bucket] = [[key, 1]]

        #Bucket has at least one Item
        else:
            #Check if key already exists
            found = False
            for entry in self.hm[bucket]:
                if entry[0] == key:
                    entry[1] += 1
                    found = True
            
            #Word has not been entered yet
            if not found:
                self.hm[bucket].append([key, 1])


        



#Main Method
if __name__ == "__main__":
    #Question 3
    hm = HashMap()
    
    poemFilePath = os.path.join(os.path.dirname(__file__), 'dataFiles/poem.txt')
    with open(poemFilePath, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.rstrip()
        words = line.split(' ')
        for word in words:
            if word:
                hm[word] = 1

    print(hm.hm)
    

    
