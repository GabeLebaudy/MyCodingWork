#This file will be used for the match game.

#Imports
import random
from decorators import log_start_and_stop

#Match Class
class Match:
    #Constructor
    def __init__(self):
        self.allPairs = []
        self.gamemode = 0

    #Getter methods
    def getAllPairs(self):
        return self.allPairs
    
    def getPair(self, index):
        return self.allPairs[index]
    
    #Setter methods
    def setGamemode(self, mode):
        self.gamemode = mode
    
    #Check if set is empty
    def isEmpty(self):
        return len(self.allPairs) == 0
    
    #Construct the main storage of the match game
    def addMatchPair(self, term, definition):
        self.allPairs.append((term, definition))

    #Randomize the set
    @log_start_and_stop
    def shuffle(self):
        temp = []
        while not self.isEmpty():
            randomInd = random.randint(0, len(self.allPairs) - 1)
            temp.append(self.allPairs[randomInd])
            del self.allPairs[randomInd]
        
        self.allPairs = temp
        print(self.allPairs)
        