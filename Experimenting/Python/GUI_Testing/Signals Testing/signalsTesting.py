
#Testing PyQt6 Signals
#Import Modules
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from random import choice

#Create subclass from QMainWindow
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.timesClicked = 0 #Sets toggle status of button to true (pressed)
        
        self.setWindowTitle("My App")
        
        self.testButton = QPushButton("Signals are cool!") #Added self so we can access the button itself
        
        self.testButton.clicked.connect(self.buttonClicked) #Sends signal out to call button clicked function
        self.windowTitleChanged.connect(self.windowChange) #Sends signal out when the window title changes
        
        self.setCentralWidget(self.testButton) #Button is widget
    
    #Functions for button updates
    
    def buttonClicked(self):
        print("Clicked") 
        newTitle = choice(window_titles) #Random val from array
        print("Setting title:", newTitle) 
        self.setWindowTitle(newTitle) 
        
                
    def windowChange(self, windowTitle): #Calls when the window itself is changed
        #Output change to console
        print("New Window:", windowTitle)
        
        if windowTitle == "Something went wrong":
            self.testButton.setEnabled(False) #Turn off button if the Title switches to something went wrong

    '''
    def buttonToggled(self, checked):
        #Storing Data into variables
        self.checkedStatus = checked
        
        print(self.checkedStatus)
    '''
    
    '''
    def buttonReleased(self):
        self.checkedStatus = self.testButton.isChecked() #Sets boolean variable based on status of button
        
        print(self.checkedStatus)
    '''

#Main Script
if __name__ == "__main__":
    window_titles = ['My App','My App','Still My App','Still My App','What on earth','What on earth','This is surprising','This is surprising','Something went wrong']
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
