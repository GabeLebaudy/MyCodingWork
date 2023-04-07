#Import modules
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
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
        
        self.setWindowTitle("Working with grid layouts!")
        
        self.layout = QGridLayout() #Create Grid object
        
        #Add color widgets: First param is the widget, second and third are coordinates. Note that if one row or column is completely empty it does not display
        self.layout.addWidget(Color('Red'), 0, 0)
        self.layout.addWidget(Color('Blue'), 1, 1)
        self.layout.addWidget(Color('Green'), 0, 1)
        self.layout.addWidget(Color('Yellow'), 1, 0)
        
        container = QWidget()
        container.setLayout(self.layout) #Container obj to set as central widget, contains previous layouts
        
        self.setCentralWidget(container)
        
        
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()