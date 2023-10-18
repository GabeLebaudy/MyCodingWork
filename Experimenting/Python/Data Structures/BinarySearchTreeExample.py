#This file will be used to show the binary search tree data structure

#BST Class
class Bst:
    #Constructor
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    #Add a child node to the structure
    def addChild(self, data):
        if data == self.data:
            return 
        
        if data < self.data:
            #Add data in the left sub-tree
            if self.left:
                self.left.addChild(data)
            else:
                self.left = Bst(data)

        else:
            #Add data in the right sub-tree
            if self.right:
                self.right.addChild(data)
            else:
                self.right = Bst(data)
        
    #Q1
    def findMin(self):
        node = self
        #Go to farthest left option
        while node.left:
            node = node.left

        return node.data
    
    #Q2
    def findMax(self):
        node = self
        #Go to furthest right leaf
        while node.right:
            node = node.right

        return node.data
    
    #Q3
    def calcSum(self):
        elements = self.inOrderTraversal()
        return sum(elements)
        

    #Gets all elements in sorted order
    def inOrderTraversal(self):
        elements = []
        #Visit Left Tree
        if self.left:
            elements += self.left.inOrderTraversal()
        
        #Visit base node
        elements.append(self.data)

        #Visit right tree
        if self.right:
            elements += self.right.inOrderTraversal()

        return elements
    
    #Gets all elements by going through the tree one element at a time, and finding each of its sub-elements
    def preOrderTraversal(self):
        elements = []

        #Start with the current node
        elements += [self.data]

        #Go Through left tree first
        if self.left:
            elements +=  self.left.preOrderTraversal()
        
        #Go Through right tree
        if self.right:
            elements += self.right.preOrderTraversal()

        return elements

    #Gets all elements in reverse order, starting with the left leaves, then the right leaves, and then the root
    def postOrderTraversal(self):
        elements = []

        #Go Through left tree first
        if self.left:
            elements +=  self.left.postOrderTraversal()
        
        #Go Through right tree
        if self.right:
            elements += self.right.postOrderTraversal()
        
        #If no more branches, add the data
        elements += [self.data]
        
        return elements

    
    #Search for if specific value is in the tree
    def search(self, data):
        if self.data == data:
            return True
        
        if data < self.data:
            if self.left:
                return self.left.search(data)
            else:
                return False

        if data > self.data:
            if self.right:
                return self.right.search(data)
            else:
                return False
            
    #Delete an element from the tree
    def delete(self, val):
        if val < self.data:
            if self.left:
                self.left = self.left.delete(val)

        elif val > self.data:
            if self.right:
                self.right = self.right.delete(val)

        else:
            if self.left is None and self.right is None:
                return None

            if self.left is None:
                return self.right

            if self.right is None:
                return self.right

            '''
            #Use min value from the right sub-tree
            min = self.right.findMin()
            self.data = min
            self.right = self.right.delete(min)
            '''

            #Use the max value from the left sub-tree
            max = self.left.findMax()
            self.data = max
            self.left = self.left.delete(max)

        return self 

            
                

#Build the tree
def buildTree(elements):
    root = Bst(elements[0])

    for i in range(1, len(elements)):
        root.addChild(elements[i])

    return root

#Main Method
if __name__ == "__main__":
    numbers = [17, 4, 1, 20, 9, 23, 18, 34]
    numberTree = buildTree(numbers)
    print(numberTree.inOrderTraversal())
    print(numberTree.search(20))
    print(numberTree.search(21))

    #Questions
    print(numberTree.findMin())
    print(numberTree.findMax())
    print(numberTree.calcSum())
    print(numberTree.preOrderTraversal())
    print(numberTree.postOrderTraversal())

    #Deletion Test
    numberTree.delete(18)
    print("--------------")
    print(numberTree.inOrderTraversal())