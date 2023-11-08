#This file will be used for the Queue Class and Nodes for the Video Queue


#Node Class, Contains the data about the youtube video, and the queue item
class Node:
    #Constructor
    def __init__(self, url, label, removeButton, layout):
        self.url = url
        self.label = label
        self.removeButton = removeButton
        self.layout = layout

    #Getters
    def getURL(self):
        return self.url
    
    def getLabel(self):
        return self.label
    
    def getRemoveButton(self):
        return self.removeButton
    
    def getLayout(self):
        return self.layout

    #Compare Two Node Objects
    def __eq__(self, other):
        if self.url == other.url:
            return True
        return False
    
    #Remove Widgets from Memory
    def delWidgets(self):
        self.label.deleteLater()
        self.removeButton.deleteLater()
        self.layout.deleteLater()

#Queue Class, Standard Queue Class.
class Queue:
    #Constructor
    def __init__(self):
        self.videoQueue = []
    
    #Add a video item
    def enqueue(self, url, label, removeButton, layout):
        #Create new item node
        newVideo = Node(url, label, removeButton, layout)

        #Check if the video is present in the queue
        found = False
        for video in self.videoQueue:
            if newVideo == video:
                found = True
        
        if found:
            return False
        
        self.videoQueue.append(newVideo)
        return True

    #Get the item at the top of the queue
    def dequeue(self):
        return self.videoQueue.pop(0)

    #Remove a specific item from the queue
    def removeItem(self, ind):
        self.videoQueue[ind].delWidgets()
        del self.videoQueue[ind]

    #Get the length of the queue
    def getLength(self):
        return len(self.videoQueue)
    
    #Check if queue is empty
    def isEmpty(self):
        return len(self.videoQueue) == 0

    