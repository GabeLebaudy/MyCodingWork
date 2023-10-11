#This file will be used for the second question on the 

class Node:
    #Constructor
    def __init__(self, data = None, next = None, prev = None):
        self.data = data
        self.next = next
        self.prev = prev

class LinkedList:
    #Constructor
    def __init__(self):
        self.head = None

    #Insert at beginning of the list
    def insertAtStart(self, data):
        node = Node(data, self.head, None)
        self.head = node

    #Insert at the end of the list
    def insertAtEnd(self, data):
        if self.head is None:
            self.head = Node(data, None, None)
            return

        x = self.head
        while x.next:
            x = x.next

        x.next = Node(data, None, x)

    #Insert entirely new values
    def insertValues(self, values):
        self.head = None
        for data in values:
            self.insertAtEnd(data)


    #Get the length of the list
    def get_length(self):
        counter = 0
        x = self.head
        while x:
            counter += 1
            x = x.next

        return counter
    
    #Remove item at specific index
    def removeItem(self, index):
        if index < 0 or index >= self.get_length():
            raise Exception("Not a valid index")
        
        if index == 0:
            self.head = self.head.next
            self.head.prev = None
            return
        
        count = 0
        x = self.head
        while x:
            if count == index - 1:
                x.next = x.next.next
                x.next.prev = x
                break
        
            x = x.next
            count += 1

    #Insert at specific index
    def insertAtIndex(self, index, data):
        if index < 0 or index > self.get_length():
            raise Exception("Index out of range.")
        
        if index == 0:
            self.insertAtStart(data)
            return
        
        counter = 0
        x = self.head
        while x:
            if counter == index - 1:
                node = Node(data, x.next, x.prev)
                x.next = node
                break

            x = x.next
            counter += 1

    #Print the list forward
    def printForward(self):
        if self.head is None:
            print("Linked List is empty")
            return
        
        x = self.head
        lstr = ''
        while x:
            lstr += str(x.data) + '<-->'
            x = x.next

        print(lstr)

    #Print the list backward
    def printBackward(self):
        if self.head is None:
            print("Linked list is empty.")
            return
        
        x = self.getLastNode()
        lstr = ''
        while x:
            lstr += str(x.data) + '<-->'
            x = x.prev

        print(lstr)
            

    #Get the last node in the list
    def getLastNode(self):
        x = self.head
        while x.next:
            x = x.next

        return x

#Main Method
if __name__ == "__main__":
    ll = LinkedList()
    ll.insertValues([0, 1, 2, 3, 4, 5])
    ll.printForward()
    ll.printBackward()
    
    