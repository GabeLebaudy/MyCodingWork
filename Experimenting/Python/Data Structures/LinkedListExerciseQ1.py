#This is an example exercise using linked list


#Classes
class Node:
    #Constructor
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next

class LinkedList:
    #Constructor
    def __init__(self):
        self.head = None

    #Insert at beginning of the list
    def insertAtStart(self, data):
        node = Node(data, self.head)
        self.head = node

    #Insert at the end of the list
    def insertAtEnd(self, data):
        if self.head is None:
            self.head = Node(data, None)
            return

        x = self.head
        while x.next:
            x = x.next

        x.next = Node(data, None)

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
            return
        
        count = 0
        x = self.head
        while x:
            if count == index - 1:
                x.next = x.next.next
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
                node = Node(data, x.next)
                x.next = node
                break

            x = x.next
            counter += 1

    #Insert after first occurance of a value
    def insertAfterValue(self, value, data):
        if self.head is None:
            return
        
        x = self.head
        while x:
            if x.data == value:
                node = Node(data, x.next)
                x.next = node
                break
            
            x = x.next

    #Remove the first item with the value passed in
    def removeValue(self, value):
        if self.head is None:
            return
        
        x = self.head
        i = 0
        while x:
            if x.data == value:
                self.removeItem(i)

            x = x.next
            i += 1

    #Print the List
    def print(self):
        if self.head is None:
            print("Linked List is Empty")
            return
        
        x = self.head
        lstr = ''
        while x:
            lstr += str(x.data) + '--->'
            x = x.next

        print(lstr)


#Main Method (Testing Functions)
if __name__ == "__main__":
    ll = LinkedList()
    ll.insertValues(["banana","mango","grapes","orange"])
    ll.print()
    ll.insertAfterValue("mango","apple") # insert apple after mango
    ll.print()
    ll.removeValue("orange") # remove orange from linked list
    ll.print()
    ll.removeValue("figs")
    ll.print()
    ll.removeValue("banana")
    ll.removeValue("mango")
    ll.removeValue("apple")
    ll.removeValue("grapes")
    ll.print()