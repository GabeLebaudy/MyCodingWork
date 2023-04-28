#This file will be used to create a term object class is created

#Class
class TermObj():
    #Constructor
    def __init__(self, data, doDraw):
        self.rateData = data
        self.doDraw = doDraw

    #Getters
    def getData(self):
        return self.rateData
    
    def getDrawStatus(self):
        return self.doDraw
    
    #Setters
    def setData(self, dataArr):
        self.rateData = dataArr

    def setDrawStatus(self, status):
        self.doDraw = status