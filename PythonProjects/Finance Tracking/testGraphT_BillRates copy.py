#The purpose of this file will be to test working with the csv file from the T-bill official website

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os

if __name__ == "__main__": 
    filePath = os.path.join(os.path.dirname(__file__), '2023TBIlldata.csv')
    TbillDf = pd.read_csv(filePath)

    TbillDf = TbillDf.sort_values(['Date'], ascending = 1)

    testFigure = plt.figure(figsize = (10, 6), dpi = 100)
    figAx = testFigure.add_axes([0.15, 0.15, 0.8, 0.8])
    figAx.set(title = 'T-Bill rates over time', xlabel = 'Date', ylabel = "Rate %")
    figAx.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])

    graphLabels = ['4 Week Bank', '4 Week Coupon', '8 Week Bank', '8 Week Coupon', '13 Week Bank', '13 Week Coupon', '17 Week Bank', '17 Week Coupon', '26 Week Bank', '26 Week Coupon', '52 Week Bank', '52 Week']
    for i in range(1, len(TbillDf.iloc[0])):
        figAx.plot(TbillDf.iloc[:, 0], TbillDf.iloc[:, i], label = graphLabels[i - 1])
            
    figAx.legend(loc = 0, ncols = 2)
    figAx.grid(True)

    plt.show()


        



