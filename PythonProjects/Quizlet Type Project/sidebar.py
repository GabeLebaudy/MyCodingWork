#Used for storing the widgets, layouts and signals on the side bar

#Imports

#Node Class
class Node:
    #Constructor
    def __init__(self, titleLabel, editBtn, delBtn, setLayout):
        self.titleLabel = titleLabel
        self.editBtn = editBtn
        self.delBtn = delBtn
        self.setLayout = setLayout
        
    #Getters
    def getTitle(self):
        return self.titleLabel
    
    def getEditBtn(self):
        return self.editBtn
    
    def getDelBtn(self):
        return self.delBtn
    
    def getSetLayout(self):
        return self.setLayout
    
    #Delete the node
    def deleteWidgets(self):
        self.titleLabel.deleteLater()
        self.editBtn.deleteLater()
        self.delBtn.deleteLater()
        self.setLayout.deleteLater()
        
#Side Bar class
class SideBar:
    #Constructor
    def __init__(self):
        self.items = []
        
    #Add a pair to the set
    def addNode(self, title, edit, delete, layout):
        newNode = Node(title, edit, delete, layout)
        self.items.append(newNode)
        
    #Remove a node with a given index
    def removeNode(self, index):
        self.items[index].delWidgets()
        del self.items[index]

    #Get the length of the set
    def getLength(self):
        return len(self.items)    
    