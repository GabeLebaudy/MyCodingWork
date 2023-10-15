#This file will demonstrate the stack data structure without the deque class

#Stack Class
class Stack:
    #Constructor
    def __init__(self):
        self.storage = []

    #Push Method
    def push(self, val):
        self.storage.append(val)

    #View value at the top of the stack
    def peek(self):
        return self.storage[-1]
    
    #Get the top of the stack
    def pop(self):
        val = self.storage.pop()
        return val
    
    #Check if stack is empty
    def isEmpty(self):
        return (len(self.storage) == 0)
    
    #Get the size of the stack
    def getSize(self):
        return len(self.storage)
    
    #Print the stack
    def print(self):
        print(self.storage)
    
#Main Method
if __name__ == "__main__":
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    s.print()

    print(s.peek())

    s.pop()
    s.print()

    print(s.getSize())

    s.pop()
    print(s.isEmpty())

    s.pop()
    print(s.isEmpty())

    