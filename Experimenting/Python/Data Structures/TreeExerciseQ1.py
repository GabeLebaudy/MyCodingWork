#This file will be used for the first question of the general tree data structure exercises


#Tree Class
class Tree:
    #Constructor
    def __init__(self, name, designation):
        self.name = name
        self.designation = designation
        self.children = []
        self.parent = None

    #Add a child
    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    #Get the current level of the node
    def getLevel(self):
        counter = 0
        p = self.parent
        while p:
            p = p.parent
            counter += 1

        return counter
    
    #Print the Tree
    def printTree(self, type):
        outputString = ''
        if type == "name" or type == "both":
            outputString = self.name
        
        if type == "designation" or type == "both":
            designationString = self.designation
            if type == "both":
                designationString = ' (' + designationString + ')'

            outputString += designationString

        levelString = ''
        level = self.getLevel()
        if level > 0:
            levelString = '  ' * level + '|--'
        
        outputString = levelString + outputString
        print(outputString)

        if len(self.children) > 0:
            for child in self.children:
                child.printTree(type)


#Build the Tree
def buildTree():
    root = Tree("Gabe", "CEO")

    cto = Tree("Mike", "CTO")
    hr = Tree("Marc", "HR Head")

    infastructure = Tree("James", "Infastructure Head")
    application = Tree("Andres", "Application Head")

    infastructure.addChild(Tree("Steve", "Cloud Manager"))
    infastructure.addChild(Tree("Mary", "App Manager"))

    cto.addChild(infastructure)
    cto.addChild(application)
    
    hr.addChild(Tree("Peter", "Recruitment Manager"))
    hr.addChild(Tree("Ben", "Policy Manager"))

    root.addChild(cto)
    root.addChild(hr)

    return root

#Main Method
if __name__ == "__main__":
    tree = buildTree()
    tree.printTree("both")