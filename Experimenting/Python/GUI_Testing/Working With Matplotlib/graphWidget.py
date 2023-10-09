import sys
import matplotlib
matplotlib.use('QtAgg')

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from testGraphClass import testGraph
'''
#Creates canvas object, which also functions as a QWidget
class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig) #Turns figure object into a figure widget
        self.axes.plot([0,1,2,3,4], [10,1,20,3,40]) #Plot simple data
'''

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Testing out Matplotlib!")
        
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = testGraph(self) #Create new matplotlib object, 
        self.setCentralWidget(sc)

        self.show()

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    app.exec()