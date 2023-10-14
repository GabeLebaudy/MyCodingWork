#This file will be used for stack exercises 


#Deque import
from collections import deque
#Exercise Functions

#Reverse the order of a string, and print it out
def reverseString(string):
    s = Stack()
    for char in string:
        s.push(char)

    revStr = ''
    while not(s.is_empty()):
        revStr += s.pop()

    print(revStr)

def checkMatch(char1, char2):
    dictionary = {
        ')' : '(',
        '}' : '}',
        ']' : '['
    }

    return dictionary[char1] == char2

#Check if the parenthases in a string are balanced
def isBalanced(string):
    s = Stack()
    for char in string:
        if char == '(' or char == '[' or char == '{':
            s.push(char)

        if char == ')' or char == ']' or char == '}':
            if s.size() == 0:
                return False
            
            if not checkMatch(char, s.pop()):
                return False
    
    return(s.size() == 0)
    


#Stack Class
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
    reverseString("emirP hcaoC")

    print(isBalanced("({a+b})"))
    print(isBalanced("))((a+b}{"))
    print(isBalanced("((a+b))"))
    print(isBalanced("((a+g))"))
    print(isBalanced("))"))
    print(isBalanced("[a+b]*(x+2y)*{gg+kk}"))