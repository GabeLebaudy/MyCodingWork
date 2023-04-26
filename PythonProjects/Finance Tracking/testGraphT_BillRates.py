#The purpose of this file will be to test working with the csv file from the T-bill official website

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os

class TBillGraph(FigureCanvas):
    #Constructor
    def __init__(self, parent = None):    
        filePath = os.path.join(os.path.dirname(__file__), '2023TBIlldata.csv')
        self.TBillDf = pd.read_csv(filePath)

        self.TBillDf = self.TBillDf.sort_values(['Date'], ascending = 1)

        self.testFigure = plt.figure(figsize = (10, 6), dpi = 100)
        self.figAx = self.testFigure.add_axes([0.15, 0.15, 0.8, 0.8])
        
        self.graphLabels = ['4 Week Bank', '4 Week Coupon', '8 Week Bank', '8 Week Coupon', '13 Week Bank', '13 Week Coupon', '17 Week Bank', '17 Week Coupon', '26 Week Bank', '26 Week Coupon', '52 Week Bank', '52 Week']

        super(TBillGraph, self).__init__(self.testFigure)


    def drawGraph(self):
        self.figAx.set(title = 'T-Bill rates over time', xlabel = 'Date', ylabel = "Rate %")
        self.figAx.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])

        for i in range(1, len(self.TBillDf.iloc[0])):
            self.figAx.plot(self.TBillDf.iloc[:, 0], self.TBillDf.iloc[:, i], label = self.graphLabels[i - 1])
        
        self.figAx.legend(loc = 0, ncols = 2)
        self.figAx.grid(True)

    def disableAllCoupons(self):
        pass
        #TODO: Move data arrays into objects, that way I can also check the draw status If I want to link it any other functions in the future
    
    def enableAllCoupons(self):
        pass
        #TODO look up
        
    def disableTerm(self, item):
        pass
        #TODO: Pass in button text as param for item, disable the term length that button is press
    
    def enableTerm(self, item):
        pass
        #TODO same as above

    

