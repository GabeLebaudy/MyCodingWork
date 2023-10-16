#This file will be used for the second exercise question for the general tree data structure

#Tree Class
class TreeNode:
    #Constructor
    def __init__(self, data):
        self.data = data
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
    def printTree(self, level):
        curLevel = self.getLevel()
        if curLevel <= level: 
            if curLevel > 0:
                print('  ' * curLevel, end='')
                print('|--', end='')
        
            print(self.data)
            if len(self.children) > 0:
                for child in self.children:
                    child.printTree(level)


#Build the Tree
def buildTree():
    root = TreeNode("Global")

    india = TreeNode("India")
    usa = TreeNode("USA")

    gujarat = TreeNode("Gujarat")
    karnataka = TreeNode("Karnataka")

    newJersey = TreeNode("New Jersey")
    california = TreeNode("California")

    gujarat.addChild(TreeNode("Ahmedabad"))
    gujarat.addChild(TreeNode("Baroda"))

    karnataka.addChild(TreeNode("Bangluru"))
    karnataka.addChild(TreeNode("Mysore"))

    newJersey.addChild(TreeNode("Princeton"))
    newJersey.addChild(TreeNode("Trenton"))

    california.addChild(TreeNode("San Francisco"))
    california.addChild(TreeNode("Mountain View"))
    california.addChild(TreeNode("Palo Alto"))

    india.addChild(gujarat)
    india.addChild(karnataka)

    usa.addChild(newJersey)
    usa.addChild(california)

    root.addChild(india)
    root.addChild(usa)

    return root


#Main Method
if __name__ == "__main__":
    tree = buildTree()
    tree.printTree(5)