#Import Modules
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt

#Main Window Subclass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Working with list widgets!")
        
        self.listWidget = QListWidget()
        self.listWidget.addItems(['Football', 'BasketBall', 'Soccer', 'Baseball'])
        
        self.listWidget.currentItemChanged.connect(self.itemChanged)
        self.listWidget.currentTextChanged.connect(self.textChanged)
        
        self.setCentralWidget(self.listWidget)
        
    def itemChanged(self, i):
        print(i.text()) #I is the item object, .text pulls text value
        
    def textChanged(self, s):
        print(s)
        
#Main Script
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()