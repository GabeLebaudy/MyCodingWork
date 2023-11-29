#This file will be used for the match game.

#Imports

#Match Class
class Match:
    #Constructor
    def __init__(self):
        self.allPairs = []
        self.indexCounter = 0

    #Getter methods
    def getAllPairs(self):
        return self.allPairs
    
    def getPair(self, index):
        return self.allPairs[index]
    
    def getIndexCounter(self):
        return self.indexCounter
    
    def setIndexCounter(self, ind):
        self.indexCounter = ind
    
    #Construct the main storage of the match game
    def addMatchPair(self, term, definition):
        self.allPairs.append((term, definition, self.indexCounter))
        self.indexCounter += 1
