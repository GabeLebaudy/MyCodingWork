#Import modules
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout
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

#Main Window SubClass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Working with Stacked layouts!")
        
        self.layout = QStackedLayout() #Create layout obj
        
        #Add widgets to obj
        self.layout.addWidget(Color('Red'))
        self.layout.addWidget(Color('Blue'))
        self.layout.addWidget(Color('Green'))
        self.layout.addWidget(Color('Yellow'))
        
        self.layout.setCurrentIndex(2)
        
        container = QWidget()
        container.setLayout(self.layout)
        
        self.setCentralWidget(container)
        
#Main Script
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()