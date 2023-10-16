#This file will be used to demonstrate the general tree data structure

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
    def printTree(self):
        level = self.getLevel()
        if level > 0:
            print('  ' * level, end='')
            print('|--', end='')
        
        print(self.data)
        if len(self.children) > 0:
            for child in self.children:
                child.printTree()
        


def buildTree():
    root = TreeNode("Electronics")
    laptop = TreeNode("Laptop")
    cellphone = TreeNode("Cell Phone")
    tv = TreeNode("TV")

    laptop.addChild(TreeNode("Mac"))
    laptop.addChild(TreeNode("Dell"))
    
    cellphone.addChild(TreeNode("IPhone"))
    cellphone.addChild(TreeNode("Andriod"))
    
    tv.addChild(TreeNode("Samsung"))
    tv.addChild(TreeNode("HiSense"))

    root.addChild(laptop)
    root.addChild(cellphone)
    root.addChild(tv)

    return root

#Main method
if __name__ == "__main__":
    Tree = buildTree()
    Tree.printTree()