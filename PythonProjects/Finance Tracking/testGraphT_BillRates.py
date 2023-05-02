#The purpose of this file will be to test working with the csv file from the T-bill official website

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from TermObject import TermObj
import os
class TBillGraph(FigureCanvas):
    #Constructor
    def __init__(self, parent = None):
        folderDir = os.path.join(os.path.dirname(__file__), 'TBillData')
        filePath = os.path.join(folderDir, 'TBill2023.csv')
        
        self.TBillDf = pd.read_csv(filePath)

        self.TBillDf = self.TBillDf.sort_values(['Date'], ascending = 1)
        self.termObjArray = self.createObjects(self.TBillDf)

        self.testFigure = plt.figure(figsize = (10, 6), dpi = 100)
        self.figAx = self.testFigure.add_axes([0.15, 0.15, 0.8, 0.75])
        
        self.graphLabels = ['4 Week Bank', '4 Week Coupon', '8 Week Bank', '8 Week Coupon', '13 Week Bank', '13 Week Coupon', '17 Week Bank', '17 Week Coupon', '26 Week Bank', '26 Week Coupon', '52 Week Bank', '52 Week']

        super(TBillGraph, self).__init__(self.testFigure)

    def createObjects(self, df):
        objArr = []
        for i in range(1, len(df.iloc[0])):
            if i % 2 == 1:
                bc = True
            else:
                bc = False
            
            curObj = TermObj(df.iloc[:, i].copy(), bc)
            objArr.append(curObj)

        return objArr

    def drawGraph(self):
        self.figAx.clear()
        
        self.figAx.set(title = 'T-Bill rates over time', xlabel = 'Date', ylabel = "Rate %")
        self.figAx.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])

        for i in range(1, len(self.TBillDf.iloc[0])):
            if self.termObjArray[i - 1].getDrawStatus() is True:
                self.figAx.plot(self.TBillDf.iloc[:, 0], self.termObjArray[i - 1].getData(), label = self.graphLabels[i - 1])
        
        self.figAx.legend(loc = 0, ncols = 2)
        self.figAx.grid(True)

    def disableAllCoupons(self):
        pass
        #TODO: Move data arrays into objects, that way I can also check the draw status If I want to link it any other functions in the future
    
    def enableAllCoupons(self):
        pass
        #TODO look up
        
    def disableTerm(self, term, bc):
        index = self.getIndex(term)
        if bc == 'Bank':
            sc = 0
        else:
            sc = 1
        self.termObjArray[index * 2 + sc].setDrawStatus(False)

    def enableTerm(self, term, bc):
        index = self.getIndex(term)
        if bc == 'Bank':
            sc = 0
        else:
            sc = 1
        self.termObjArray[index * 2 + sc].setDrawStatus(True)

    def getIndex(self, term):
        if term == 4:
            return 0
        elif term == 8:
            return 1
        elif term == 13:
            return 2
        elif term == 17:
            return 3
        elif term == 26:
            return 4
        elif term == 52:
            return 5
        
    def loadWholeYear(self, year):
        dataDir = os.path.join(os.path.dirname(__file__), 'TBillData')
        fileStr = "TBill%s.csv" % year
        newDataPath = os.path.join(dataDir, fileStr)
        
        self.TBillDf = pd.read_csv(newDataPath)
        self.termObjArray = self.createObjects(self.TBillDf)

    

