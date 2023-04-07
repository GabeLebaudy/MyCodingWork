#Import Modules
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt

#Main Window Subclass
class MainWindow(QMainWindow):
    #Constructor Method
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Working with Drop Downs!")
        
        self.dropDown = QComboBox()
        self.dropDown.addItems(['Rare', 'Medium Rare', 'Medium', 'Medium Well', 'Well Done']) #Pass in list to add items
        
        self.dropDown.currentIndexChanged.connect(self.indexChanged) #Sends signal out when a different selection is made 1.
        self.dropDown.currentTextChanged.connect(self.textChanged) #Sends signal out when the text showing which item selected changes 2.
        
        self.dropDown.setEditable(True) #Allows user to edit the drop down menu
        '''
        .No Insert - Doesn't insert .InsertAtTop - Inserts as first item? .InsertAtCurrent - Inserts at current index - 
        .InsertAtBottom - Inserts as last item? .Insert(After/Before)Current - Inserts 1 index above or below the current index
        .InsertAlphabetically - Insert in alphabetical order
        '''
        self.dropDown.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        
        #Set max number of items to dropDown
        #self.dropDown.setMaxCount(7)
        self.setCentralWidget(self.dropDown)
        
        
    def indexChanged(self, i): #Provides index of item selected
        print("Current index:", i)
        
    def textChanged(self, s): #Contains text value of item selected
        print("Current text:", s)
        
        
#Main Script
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()
        