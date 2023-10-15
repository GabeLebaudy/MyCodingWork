#This file will be used for the Queue data structure exercises

#Imports
from collections import deque
import threading
import time

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
    
#Place Order Thread
class placeThread(threading.Thread):
    #Constructor
    def __init__(self, queue, orders):
        super(placeThread, self).__init__()
        self.queue = queue
        self.orders = orders

    #Place Order Method
    def run(self):
        for order in self.orders:
            time.sleep(0.5)
            self.queue.enqueue(order)


#Serve Order Thread
class serveThread(threading.Thread):
    #Constructor
    def __init__(self, queue):
        super(serveThread, self).__init__()
        self.queue = queue

    #Serve Order Thread
    def run(self):
        while not(self.queue.isEmpty()):
            time.sleep(2)
            order = self.queue.dequeue()
            print(order)


#Main Method
if __name__ == "__main__":
    orders = ['pizza','samosa','pasta','biryani','burger']
    q = Queue()
    placeOrder = placeThread(q, orders)
    serveOrder = serveThread(q)

    placeOrder.start()
    time.sleep(1)
    serveOrder.start()

    #Question 2:
    for i in range(1, 11):
        binaryNum = str(bin(i))
        print(binaryNum[2:])
