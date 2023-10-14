#This will be an implementation of the stack data structure

#Imports

from collections import deque

class Stack:
    #Constructor
    def __init__(self):
        self.container = deque()
    
    def push(self, val):
        self.container.append(val)
    
    def pop(self):
        return self.container.pop()

    def peek(self):
        return self.container[-1]

    def is_empty(self):
        return len(self.container) == 0

    def size(self):
        return len(self.container)

#Main Method
if __name__ == "__main__":
    #Built In Example
    stack = deque()
    stack.append(10)
    stack.append(15)
    stack.append(20)
    stack.pop()

    #Stack Class
    s = Stack()
    s.push(4)

    print(s.size())
    print(s.peek())
    print(s.pop())
    print(s.is_empty())
    
