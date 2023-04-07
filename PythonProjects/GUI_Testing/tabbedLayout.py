#Import Modules
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTabWidget, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

#Color class
class Color(QWidget):
    #Constructor method
    def __init__(self, color):
        super(Color, self).__init__()
        
        self.setAutoFillBackground(True)
        
        palette = self.palette() #Pull palette from widget
        palette.setColor(QPalette.ColorRole.Window, QColor(color)) #Use palette object to fill color
        self.setPalette(palette) #Set new palette to palette object
        
#Main Window Subclass
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Trying out tabs!")
        
        self.tabs = QTabWidget() #Create tab object (Imagine empty bar to be populated)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North) #Sets bar to the top of the window
        self.tabs.setMovable(False) #Doesn't allow tabs to be moved. (True does)
        
        for n,  color in enumerate(["red", "green", "blue", "yellow"]): #The enumerate function gets both the index: n and the color of the list
            self.tabs.addTab(Color(color), color) #Tabs are added by the first parameter - a color widget created by color. It is then given a text value of color, so that the tabs and their labels match the colors

        self.setCentralWidget(self.tabs)
            
        self.setCentralWidget(self.tabs)
        
#Main Script 
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()