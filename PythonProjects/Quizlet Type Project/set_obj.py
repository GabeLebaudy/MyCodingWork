#This file will be used to store the widgets for the current set object. 

#Imports

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
    
    #Delete widgets for the pair
    def delWidgets(self):
        self.termWid.deleteLater()
        self.defWid.deleteLater()
        self.removeBtn.deleteLater()
        self.pairLay.deleteLater()
    
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
