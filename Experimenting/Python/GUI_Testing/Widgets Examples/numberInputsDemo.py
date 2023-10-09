#Import Modules
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt 

#Main Window Subclass
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.intWidget = QDoubleSpinBox()
        # Or: widget = QSpinBox() for integer values

        #Sets min and max values that the widget can contain
        self.intWidget.setMinimum(-10)
        self.intWidget.setMaximum(10)
        # Or: widget.setRange(-10,3)

        #Annotate the value
        self.intWidget.setPrefix("$") 
        self.intWidget.setSuffix("c")
        self.intWidget.setSingleStep(0.5)  # Or e.g. 0.5 for QDoubleSpinBox (Amount value changes each time arrow is pressed)
        
        self.intWidget.valueChanged.connect(self.value_changed) #Send signal when value changes
        self.intWidget.textChanged.connect(self.value_changed_str) #Send signal when text value changes
        
        #self.intWidget.lineEdit().setReadOnly(True) #Makes it so that only controls are allowed

        self.setCentralWidget(self.intWidget)

    def value_changed(self, i): #I is the value of the new number
        print(i)

    def value_changed_str(self, s): #S is the text contained in the widget box
        print(s)

#Main Script
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()