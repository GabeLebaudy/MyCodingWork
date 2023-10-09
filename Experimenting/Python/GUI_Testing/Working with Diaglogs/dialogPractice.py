#Import modules
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton

#Main Window Class
class MainWindow(QMainWindow):
    #Constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Testing out Dialogs!")
        
        self.testButton = QPushButton("Click Me!")
        self.testButton.clicked.connect(self.buttonClick)
        
        self.setCentralWidget(self.testButton)
        
    def buttonClick(self, s):
        print("Click!", s)
        
        self.testDialog = QDialog(self)
        self.testDialog.setWindowTitle("This is a test window!")
        
        self.testDialog.exec()
        
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()