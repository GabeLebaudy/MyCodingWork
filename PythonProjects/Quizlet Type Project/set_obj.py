#This file will be used to store the widgets for the current set object. 

#Imports
import logging
from decorators import log_start_and_stop

#Logging
LOGGER = logging.getLogger('Main Logger')

#Node class
class Node:
    #Constructor
    def __init__(self, termWid, defWid, layout, removeBtn):
        self.termWid = termWid
        self.defWid = defWid
        self.pairLay = layout
        self.removeBtn = removeBtn
        
    #Getters
    def getTermWid(self):
        return self.termWid
    
    def getDefWid(self):
        return self.defWid
    
    def getLayout(self):
        return self.pairLay
    
    def getBtn(self):
        return self.removeBtn
    
    def getVals(self):
        return self.termWid.toPlainText(), self.defWid.toPlainText()
    
    #Delete widgets for the pair
    def delWidgets(self):
        self.termWid.deleteLater()
        self.defWid.deleteLater()
        self.removeBtn.deleteLater()
        self.pairLay.deleteLater()

    #Check if pair is empty 0:Completely empty, 1:At least one term is missing a definition pair 2: All good
    def checkEmpty(self):
        if not self.termWid.toPlainText() and not self.defWid.toPlainText():
            return 0
        if not self.termWid.toPlainText() or not self.defWid.toPlainText():
            return 1
        else: return 2

    
#Set Class
class Set:
    #Constructor
    def __init__(self):
        self.items = []
        
    #Add a pair to the set
    def addNode(self, term, definition, layout, removeBtn):
        newNode = Node(term, definition, layout, removeBtn)
        self.items.append(newNode)
        
    #Remove a node with a given index
    def removeNode(self, index):
        self.items[index].delWidgets()
        del self.items[index]

    #Get the length of the set
    def getLength(self):
        return len(self.items)
    
    #Check if the set is empty
    def isEmpty(self):
        return len(self.items) == 0
    
    #Check if set is ready to be created - 0:Completely empty, 1:At least one term is missing a definition pair 2: All good
    @log_start_and_stop
    def isPairsEmpty(self):
        flag = False
        ce = 0
        for i in range(len(self.items)):
            code = self.items[i].checkEmpty()
            if code == 1:
                flag = True
            if code == 2:
                ce = 2

        if not flag:
            return ce
        else:
            return 1
        
    #Return Dictionary of Set Pairs
    @log_start_and_stop
    def getPairData(self):
        finalList = {}
        for i in range(self.getLength()):
            termText, defText = self.items[i].getVals()
            finalList[termText] = defText

        return finalList






