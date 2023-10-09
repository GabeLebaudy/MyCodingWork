from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QToolBar, QStatusBar, QCheckBox, QPushButton
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt, QSize
import os

class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Working with toolbars!")

        self.label = QLabel("Oh shit lmao")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) #Create new label obj and center it

        self.setCentralWidget(self.label) 

        self.toolbar = QToolBar("Main ToolBar") #Create toolbar object
        self.toolbar.setIconSize((QSize(16, 16)))
        self.addToolBar(self.toolbar) #Add toolbar to window

        imgFilePath = os.path.join(os.path.dirname(__file__), 'application-search-result.png')
        buttonAction = QAction(QIcon(imgFilePath), "My Button", self) #Create button with text, self is the parent of the button, in this case the window (not always self)
        buttonAction.setStatusTip("This is my button.") #Text to be displayed on status bar
        buttonAction.triggered.connect(self.onMyToolBarButtonClick)#Send signal
        buttonAction.setCheckable(True) #Makes the button checked or uncheked when you click it
        #buttonAction.setShortcut(Qt.Key.Key_Control + Qt.Key.Key_P)
        buttonAction.setShortcut(QKeySequence("Ctrl+p"))
        self.toolbar.addAction(buttonAction) #Add action to toolbar
        
        self.toolbar.addSeparator() #Separates actions
        
        secondAction = QAction(QIcon(imgFilePath), "Your Button", self) #Second action is identical to first
        secondAction.setStatusTip("This is your button.")
        secondAction.triggered.connect(self.onMyToolBarButtonClick)
        secondAction.setCheckable(True)
        self.toolbar.addAction(secondAction)
        
        self.toolbar.addWidget(QLabel("Hello!")) #Adds widgets to tool bar
        self.toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))#We set the windows status bar to be a new QStatusBar object, passing the window(self) as the parent object
        
        self.menu = self.menuBar() #Create menu object and assign it to the window
        
        fileMenu = self.menu.addMenu("&File") #Add the menu category (What is always visible)
        fileMenu.addAction(buttonAction) #Add menu actions
        fileMenu.addSeparator()
        
        subMenu = fileMenu.addMenu("Sub Menu")
        subMenu.addAction(secondAction)

    def onMyToolBarButtonClick(self, s): #Event (When tool bar is clicked)
        print("Click!", s)


#Main method
if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()