#Import modules
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
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
    #Constructor method
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Working with Layouts!")
        
        #Create color widgets
        self.blueWidget = Color('Blue')
        self.redWidget = Color('Red')
        self.greenWidget = Color('Green')
        
        self.layoutContainer = QHBoxLayout() #Create layout widget
        self.layout1 = QVBoxLayout() #Sub-layouts
        self.layout2 = QVBoxLayout() 
        
        self.layoutContainer.setContentsMargins(0, 0, 0, 0)
        self.layoutContainer.setSpacing(10)
        #Add colors to layout
        self.layout1.addWidget(self.blueWidget)
        self.layout1.addWidget(self.redWidget)
        self.layout1.addWidget(self.greenWidget)
        
        #Add first set of colors to layout container
        self.layoutContainer.addLayout(self.layout1)
        
        #Create second color mix layout
        self.layout2.addWidget(Color('Purple'))
        self.layout2.addWidget(Color('Brown'))
        
        self.layoutContainer.addLayout(self.layout2)
        
        container = QWidget()
        container.setLayout(self.layoutContainer)
        
        self.setCentralWidget(container)
        

#Main Script
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()