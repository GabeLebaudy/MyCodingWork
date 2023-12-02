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
        self.mixedFlag = 0

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
    
    #Check the length of the match set
    def getLength(self):
        return len(self.allPairs)
    
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

    #Get the next question from the set
    def getQuestion(self):
        #Given Definition, Match Term
        if self.gamemode == 0:
            return self.allPairs[0][1]
        
        #Given Term, Match Definition
        elif self.gamemode == 1:
            return self.allPairs[0][0]

        #Mixed
        else:
            termOrDef = random.randint(0, 1)
            self.mixedFlag = termOrDef
            return self.allPairs[0][termOrDef]
        
    #Return if user was right, and the answer string
    def isRight(self, userAnswer):
        if self.gamemode == 0:
            wasRight = self.allPairs[0][0].lower() == userAnswer.lower()
            return wasRight, self.allPairs[0][0]
        elif self.gamemode == 1:
            wasRight = self.allPairs[0][1].lower() == userAnswer.lower()
            return wasRight, self.allPairs[0][1]
        else:
            tupleIndex = 1 if self.mixedFlag == 0 else 0
            wasRight = self.allPairs[0][tupleIndex].lower() == userAnswer.lower()
            return wasRight, self.allPairs[0][tupleIndex]
        
    #Function for if user answered correctly
    @log_start_and_stop
    def answeredCorrect(self):
        self.allPairs.pop(0)

    #Function for if the user answered incorrectly
    @log_start_and_stop
    def reshuffleQuestion(self):
        item = self.allPairs.pop(0)
        if len(self.allPairs) >= 1:
            newIndex = random.randint(1, len(self.allPairs))
            self.allPairs.insert(newIndex, item)

    #Game is completed, reset the match obj
    def resetGame(self):
        self.allPairs = []
        self.gamemode = 0
        self.mixedFlag = 0
        