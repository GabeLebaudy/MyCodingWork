#Import Modules
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt 


#Main Window Subclass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.checkbox = QCheckBox()
        self.checkbox.setCheckState(Qt.CheckState.Checked) #Sets default value to checked
        
        #Tri-state (3 states of being) 
        #self.checkbox.setCheckState(Qt.PartiallyChecked) Doesn't work
        #self.checkbox.setTristate(True) #Does work: Rotates through 3 options
        self.checkbox.stateChanged.connect(self.boxChanged)#Send signal out when checkbox changes
        
        self.setCentralWidget(self.checkbox)
        
    def boxChanged(self, s):
        print(s == Qt.CheckState.Checked)
        print(s)
        
#Main Script
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()