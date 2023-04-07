#Import Modules
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt 

#Main Window Subclass
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QSlider(Qt.Orientation.Horizontal)

        #Set max and min values of slider
        widget.setMinimum(-10)
        widget.setMaximum(10)
        # Or: widget.setRange(-10,3)

        widget.setSingleStep(2) #Not sure what this does

        widget.valueChanged.connect(self.value_changed) #Sends signal when value changes
        widget.sliderMoved.connect(self.slider_position) #Sends signal when the slider is moving
        widget.sliderPressed.connect(self.slider_pressed) #Sends signal when the slider is clicked
        widget.sliderReleased.connect(self.slider_released) #Sends signal when slider is released

        self.setCentralWidget(widget)

    def value_changed(self, i): #Prints Values of slider
        if i % 2 != 0:
            i = i + 1 if i > 0 else i - 1
            self.centralWidget().setValue(i) # Set the slider's value to the nearest even value

        print(i)

    def slider_position(self, p): #Prints Position: Value
        print("position", p)

    def slider_pressed(self): 
        print("Pressed!")

    def slider_released(self):
        print("Released")


#Main Script
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()