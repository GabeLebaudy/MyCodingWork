#Import modules
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

#Main Window Subclass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Working with Widgets!")
        
        self.label = QLabel("This is a label!") #Create widget label
        
        #Alternate image example
        #self.label.setPixmap(QPixmap(r"c:\Users\Gabe\Documents\GitHub\MyCodingWork\PythonProjects\GUI_Testing\widgetsDemos\exampleImage.jpg"))
        
        #Pull font from label, then edit the object, then push it back. 
        font = self.label.font()
        font.setPointSize(30)
        self.label.setFont(font)
        
        #Determines where the text is placed. (First param aligns Horizontally, second aligns vertically)
        '''
        Horizontal Alignments: .AlignLeft - Left edge .AlignRight - Right edge .AlignHCenter - Center .AlignJustify - Justifies text given available space
        Vertical Alignments: .AlignTop - Top of the page .AlignBottom - Bottom of page .AlignVCenter - Center
        .AlignCenter (Centers Horizontally and Vertically)
        '''
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter) #| Character separates horizontal and vetical commands
        
        self.setCentralWidget(self.label)
        
        
#Main Method
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()