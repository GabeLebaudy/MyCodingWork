#Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os

class testGraph(FigureCanvas):
    #Constructor
    def __init__(self, parent=None):
        
        self.xValues = np.linspace(0, 10, 10)
            
        #Y is a function of x where y = x^2 + 3 y = f(x)
        self.yValues = self.xValues ** 2 + 3
            
        #Z is a function of x where z = x^3 - 2*x
        #zArray = xArray ** 3 - 2 * xArray

        filePath = os.path.join(os.path.dirname(__file__), 'exampleDatabase.csv')
        df = pd.read_csv(filePath)
            
        df = df.sort_values(by='Temperature')

        # Convert from Pandas data frame to NumPy array
        npArray = df.values

        # Get x & y values and put in array (2D matrix)
        xArray2 = npArray[:,0]
        yArray2 = npArray[:,1]

            #Create figure and axes, label title and axis, and plot data.
        figure_5 = plt.figure(figsize=(6,4))
        axes_6 = figure_5.add_axes([0.1,0.1,0.8,0.8])
        super().__init__(figure_5)
        self.setParent(parent)
        axes_6.set_title('Ice Cream Sales vs. Temperature')
        axes_6.set_xlabel('Temperature')
        axes_6.set_ylabel('Ice Cream Sales')
        axes_6.plot(xArray2, yArray2)
            
        #Add arrow on the chart
        axes_6.annotate("Best Month!", xy=(81, 543), xytext=(60, 540), arrowprops=dict(facecolor="black", shrink = 0.05))
            
        plt.bar(xArray2, yArray2)

    