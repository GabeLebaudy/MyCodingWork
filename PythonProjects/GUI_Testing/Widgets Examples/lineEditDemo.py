#Import Modules
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt

#Main Window Subclass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        self.lineWidget = QLineEdit() #Create object
        self.lineWidget.setMaxLength(10) #Input cannot be longer than 10 characters
        self.lineWidget.setPlaceholderText("Enter your text") #Placeholder

        #widget.setReadOnly(True) # uncomment this to make readonly

        self.lineWidget.returnPressed.connect(self.return_pressed)
        self.lineWidget.selectionChanged.connect(self.selection_changed)
        #Not sure what this means but I guess it explains the difference
        '''
        There are also two edit signals, one for when the text in the box has been edited and one for when it has been changed. 
        The distinction here is between user edits and programmatic changes. 
        The textEdited signal is only sent when the user edits text.
        '''
        self.lineWidget.textChanged.connect(self.text_changed)
        self.lineWidget.textEdited.connect(self.text_edited)

        #self.lineWidget.setInputMask('000.000;_') #Allows series of 3 digit nums separated by a period
        self.setCentralWidget(self.lineWidget)


    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)
        
#Main Script
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()