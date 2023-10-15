#This file will be used to demonstrate the Queue data Structure

from collections import deque


#Queue Class
class Queue:
    #Constructor
    def __init__(self):
        self.q = deque()

    #Add value to queue
    def enqueue(self, val):
        self.q.appendleft(val)

    #Remove item from queue
    def dequeue(self):
        return self.q.pop()
    
    #Check if queue is empty
    def isEmpty(self):
        return (len(self.q) == 0)
    
    #Get the size of the queue
    def getSize(self):
        return len(self.q)

if __name__ == "__main__":
    #Using Built In Deque Examples
    q = deque()
    q.appendleft(5)
    q.appendleft(10)
    q.appendleft(15)
    print(q.pop())

    #Using Created Class
    que = Queue()
    que.enqueue(1)
    que.enqueue(2)
    que.enqueue(3)

    print(que.dequeue())
    print(que.isEmpty())


